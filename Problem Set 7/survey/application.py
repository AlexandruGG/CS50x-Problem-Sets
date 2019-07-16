import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    # Get all form data submitted via POST
    formDetails = [request.form.get("name"), request.form.get("age"), request.form.get("language")]

    # If any of the details are missing show the error template
    if not all(formDetails):
        return render_template("error.html", message="Please submit all required form details!")

    # Open the csv file and write the formDetails inside as one row
    with open("survey.csv", "a") as csvFile:
        surveyWriter = csv.writer(csvFile, delimiter=",")
        surveyWriter.writerow(formDetails)

    return redirect("/sheet")


@app.route("/sheet", methods=["GET"])
def get_sheet():
    # Open the csv file and read the details into a list, after which pass the list onto the template
    with open("survey.csv", "r") as csvFile:
        surveyReader = csv.reader(csvFile, delimiter=",")
        engineers = list(surveyReader)

    return render_template("sheet.html", engineers=engineers)
