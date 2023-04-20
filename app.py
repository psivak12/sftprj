# -*- coding: utf-8 -*-
"""
Sentiment Analysis
"""

from flask import Flask
from flask import request
from flask import jsonify
from textblob import TextBlob
from pymongo import MongoClient


app = Flask(__name__)
client = MongoClient("mongodb+srv://bitdigitsurveys:bitdigitsurveys@cluster0.dzcak.mongodb.net/")
db = client["test"]
collection = db["surveysResponses"]


@app.route('/data')
def get_data():
    data = list(collection.find())
    for item in data:
        item['_id'] = str(item['_id'])  # Convert ObjectId to string
    return jsonify(data)


@app.route('/add_sentiment')
def add_sentiment():
    for doc in collection.find():
        review = doc['Response']
        polarity = TextBlob(review).sentiment.polarity
        collection.update_one(
            {'_id': doc['_id']},
            {'$set': {'sentiment_polarity': polarity}}
        )
    return 'Sentiment added to all records.'


if __name__ == '__main__':
    app.run(debug=False)
    #app.run(debug=False,Host='0.0.0.0')


