from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)

@app.route("/")
def index():
    information = mongo.db.information.find_one()
    return render_template("index.html", information=information)

@app.route("/scrape")
def scraper():
    information = mongo.db.information
    information_data = scrape_mars.scrape()
    information.update({}, information_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
