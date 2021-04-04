from flask import Flask, app, request, jsonify, render_template, redirect
from pymongo import MongoClient
import os, json, redis, logging

# App
application = Flask(__name__)

# connect to MongoDB
mongoClient = MongoClient('mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_AUTHDB'])
db = mongoClient[os.environ['MONGODB_DATABASE']]

# connect to Redis
redisClient = redis.Redis(host=os.environ.get("REDIS_HOST", "localhost"), port=os.environ.get("REDIS_PORT", 6379), db=os.environ.get("REDIS_DB", 0))

@application.route('/')
def index():

    return render_template("index.html", doc=db.GuessingGame.find_one())

@application.route("/question", methods=["GET","POST"])
def question():
    if not db.GuessingGame.find_one():
        initData = {
        "_id": 1,
        "countWrong": 0,
        "answered":["","","",""],
        "isFinished": False,
        "alphabets":[
            {
            "_id": 0,
            "value": "",
            }
        ],
        "question": ""
        }
        db.GuessingGame.insert_one(initData)

    doc = db.GuessingGame.find_one()
    application.logger.info(doc)
    question = request.form.get("question")
    if(question):
        db.GuessingGame.update_one(
        {},
        {"$set": {
            "question": question,
            }
        }
    )

    return render_template("index.html", doc=doc, text="*" * len(question))

@application.route("/guess", methods=["GET","POST"])
def guess():
    doc = db.GuessingGame.find_one()
    if not doc :
        return redirect("/")

    question = doc["question"]
    step = len("".join(doc["answered"]))
    letter = request.form.get("letter")

    if doc["isFinished"]:
        return redirect("/")

    application.logger.info(doc)
    application.logger.info(f"Ans is {question[step]}")

    if letter == question[step]:
        db.GuessingGame.update_one({"_id":1, "answered": ""},
                {"$set": 
                    {
                        "answered.$":letter
                    }
                })

    else:
        db.GuessingGame.update_one(doc, {"$inc":{"countWrong": 1}})
    
    doc = db.GuessingGame.find_one()
    last = doc["answered"]
    count = doc["countWrong"]
    count = 0
    for i in last:
        if i == "":
            count+=1

    if last[-1] != "":
        db.GuessingGame.update_one(doc, {"$set": {"isFinished": True}})
    doc = db.GuessingGame.find_one()
    return render_template("index.html", doc=doc, text="*" * count)

@application.route("/reset", methods=["POST"])
def reset():
    db.GuessingGame.delete_one({"_id":1})
    return redirect("/")

if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("FLASK_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("FLASK_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
