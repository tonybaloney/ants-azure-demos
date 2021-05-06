from flask import Flask, render_template
from flask_pymongo import PyMongo
import os

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)


@app.route("/")
def home_page():
    online_users = mongo.cx["flask-cosmos"].users.find({"online": True})
    return render_template("index.html",
        users=online_users)
