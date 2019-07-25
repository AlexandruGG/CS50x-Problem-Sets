import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd
app.jinja_env.globals.update(usd=usd)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Find the user's record and get the cash amount
    userResults = db.execute("SELECT id, cash FROM users WHERE id = :user_id", user_id=session["user_id"])

    if not userResults:
        return apology("user doesn't exist", 400)

    # Get the user's current stock portfolio based on past transactions
    stocksResults = db.execute("SELECT symbol, SUM(share_number) as shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING shares > 0",
                               user_id=userResults[0]["id"])

    totalValue = 0
    cash = userResults[0]["cash"]

    # Get and store quotes for each of the stocks in the portfolio, and prepare data to be passed into the portfolio template
    for stock in stocksResults:
        quote = lookup(stock["symbol"])

        stock["symbol"] = quote["symbol"]
        stock["name"] = quote["name"]
        stock["price"] = usd(quote["price"])
        stock["value"] = usd(quote["price"] * stock["shares"])

        totalValue += quote["price"] * stock["shares"]

    return render_template("portfolio.html", stocks=stocksResults, total=usd(totalValue + cash), cash=usd(cash))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))

        # Show apology if the symbol cannot be found
        if not quote:
            return apology("stock symbol doesn't exist", 400)

        # Convert the number of shares to int and show apology if it fails
        try:
            shareNumber = int(request.form.get("shares"))
        except:
            return apology("number of shares must be an integer", 400)

        # Show apology if the number of shares is not positive
        if shareNumber <= 0:
            return apology("number of shares must be positive", 400)

        # Find how much cash the user has and whether he can afford the purchase
        cashRows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

        totalCash = cashRows[0]["cash"]
        totalPurchasePrice = quote["price"] * shareNumber

        if totalCash < totalPurchasePrice:
            return apology("insufficient cash")

        # Insert the buy record in the "transactions" table
        transactionResult = db.execute("INSERT INTO transactions (user_id, type, symbol, share_number, share_price) VALUES (:user_id, :type, :symbol, :share_number, :share_price)",
                                       user_id=session["user_id"], type="buy", symbol=quote["symbol"], share_number=shareNumber, share_price=quote["price"])

        if not transactionResult:
            return apology("could not record buy transaction")

        # Update user's cash record
        cashResult = db.execute("UPDATE users SET cash = cash - :price WHERE id = :user_id",
                                price=totalPurchasePrice, user_id=session["user_id"])

        if not cashResult:
            return apology("could not update available cash record")

        flash("Stock Bought!")

        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""

    usernameInput = request.args.get("username")

    # Query the db for the username inputted by the user
    userRecord = db.execute("SELECT * FROM users WHERE username = :usernameInput", usernameInput=usernameInput)

    # Determine if the username is valid
    usernameIsValid = userRecord == [] and len(usernameInput) >= 1

    return jsonify(usernameIsValid)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Get the user past stock transactions
    stocksResults = db.execute("SELECT symbol, type, share_number as shares, share_price as price, transacted FROM transactions WHERE user_id = :user_id ORDER BY symbol ASC, transacted DESC",
                               user_id=session["user_id"])

    return render_template("history.html", stocks=stocksResults)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))

        # Show apology if the symbol cannot be found
        if not quote:
            return apology("stock symbol doesn't exist", 400)

        # Render new template with the quote details
        return render_template("quoted.html", name=quote["name"], symbol=quote["symbol"], price=usd(quote["price"]))
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register new user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        registrationDetails = [request.form.get("username"), request.form.get("password"), request.form.get("confirmation")]

        # Ensure username was submitted
        if not registrationDetails[0]:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not registrationDetails[1]:
            return apology("must provide password", 400)

        # Ensure password confirmation was submitted
        elif not registrationDetails[2]:
            return apology("must provide password confirmation", 400)

        # Ensure passwords match
        elif registrationDetails[1] != registrationDetails[2]:
            return apology("password must match confirmation", 400)

        # Insert new user into the database
        result = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                            username=registrationDetails[0], hash=generate_password_hash(registrationDetails[1]))

        # If the operation was not a success, apologise
        if not result:
            return apology("user is already registered", 400)

        # Display a flash message
        flash("User Registered!")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))

        # Show apology if the symbol cannot be found
        if not quote:
            return apology("stock symbol doesn't exist", 400)

        # Convert the number of shares to int and show apology if it fails
        try:
            shareNumber = int(request.form.get("shares"))
        except:
            return apology("number of shares must be an integer", 400)

        # Show apology if the number of shares is not positive
        if shareNumber <= 0:
            return apology("number of shares must be positive", 400)

        # Find how many shares the user has and whether he can sell the desired amount
        shareResults = db.execute("SELECT SUM(share_number) as shares FROM transactions WHERE user_id = :user_id and symbol = :symbol",
                                  user_id=session["user_id"], symbol=quote["symbol"])

        if not shareResults or shareResults[0]["shares"] < shareNumber:
            return apology("cannot sell more shares than owned")

        totalSaleValue = quote["price"] * shareNumber

        # Insert the sell record in the "transactions" table
        transactionResult = db.execute("INSERT INTO transactions (user_id, type, symbol, share_number, share_price) VALUES (:user_id, :type, :symbol, :share_number, :share_price)",
                                       user_id=session["user_id"], type="sell", symbol=quote["symbol"], share_number=-shareNumber, share_price=quote["price"])

        if not transactionResult:
            return apology("could not record sell transaction")

        # Update user's cash record
        cashResult = db.execute("UPDATE users SET cash = cash + :value WHERE id = :user_id",
                                value=totalSaleValue, user_id=session["user_id"])

        if not cashResult:
            return apology("could not update available cash record")

        flash("Stock Sold!")

        return redirect("/")
    else:
        # Retrieve all stocks the user owns
        stocks = db.execute(
            "SELECT symbol, SUM(share_number) as shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING shares > 0", user_id=session["user_id"])
        return render_template("sell.html", stocks=stocks)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
