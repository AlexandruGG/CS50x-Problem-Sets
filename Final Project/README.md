# CS50x 2019 - Final Project

**Title**: *Guardian News*

**Description**: A web app that uses [The Guardian's Open Platform]("https://open-platform.theguardian.com/")  to serve the latest news. Users can search for news stories, save them for later reading, and view stories based on saved preferences.

**Technology**: Python with Flask and Jinja2, SQLite3, HTML, CSS, Bootstrap, JavaScript + jQuery

**Pages**:
- *Login* - allows an existing user to log in
- *Register* - allows a new user to create an account
- *Home* - displays a list of news stories by querying The Guardian's API
- *Saved Stories* - displays a list of the current user's saved stories
- *Preferences* - allows the user to choose topics for the stories they see, e.g. Art, Music, Politics, Science

**Features**:
- Register:
    * Checks username availability once the user has finished their input (on blur)
    * Checks that password matches confirmation on blur and before submission
    * Uses Bootstrap form validation for the checks and to provide user feedback

- Home:
    * Fetches news stories and displays details about them in a table: Date, Section, Title, URL
    * If no user preferences are set, by default the newest articles are fetched. If topic preferences are set, randomly chooses one topic and queries the API based on it
    * Allows the user to *save* one or more stories - using the modern **fetch()** method an API call is made and the details stored in the **user_stories** table. The user receives instant feedback on whether the operation was successful or not
    * Allows the user to *search* news stories, which will fetch and display the items based on relevance

- Saved Stories:
    * Displays a list of the user's saved stories in a table similar to the one on the Home page
    * Allows the user to *delete* one or more stories, which removes them from the database and refreshes the page
    * The page notifies the user if they do not have any saved stories, and contains a button-link leading back to the Home page

- Preferences
    * Allows the user to choose different news topics via checkboxes, from a set list: Art, Business, Entertainment, Health, Music, Politics, Science, Sports
    * Allows the user to input a custom topic via an input field
    * Upon submission, if the user does not already have preferences, a new entry is created in the **user_preferences** table. If the user already has saved preferences, a new submission will update the database entry
    * Feedback after submission is given via a **flash message**

**Database Structure**:

*user*:
```
CREATE TABLE 'user' ('id' integer PRIMARY KEY AUTOINCREMENT NOT NULL, 'username' varchar(100) NOT NULL, 'password' varchar(255))
```

*user_stories*:
```
CREATE TABLE 'user_stories' ('id' integer PRIMARY KEY AUTOINCREMENT NOT NULL, 'user_id' integer NOT NULL, 'date' datetime NOT NULL, 'section' varchar(50) NOT NULL, 'title' varchar(255) NOT NULL, 'url' varchar(255) NOT NULL, FOREIGN KEY (user_id) REFERENCES user(id))
```

*user_preferences*:
```
CREATE TABLE 'user_preferences' ('id' integer PRIMARY KEY AUTOINCREMENT NOT NULL, 'user_id' integer NOT NULL, 'preferences' text NOT NULL, FOREIGN KEY (user_id) REFERENCES user(id))
```
