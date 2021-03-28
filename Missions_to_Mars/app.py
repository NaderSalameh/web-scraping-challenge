from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


# creating the flask app 
app = Flask(__name__)

# Using flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    mars_data = mongo.db.information.find_one()
    return render_template("index.html", mars_data=mars_data)


# rout to trigger the scrape function
@app.route("/scrape")
def scraper():
    information = mongo.db.information
    mars_information = scrape_mars.scrape()
    information.update({}, mars_information, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)