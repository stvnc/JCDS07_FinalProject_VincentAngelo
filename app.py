from flask import Flask, abort, jsonify, render_template,url_for, request,send_from_directory,redirect
import numpy as np
import pandas as pd
import requests

import joblib

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

# print(recommendation)

@app.route('/prediction', methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        body = request.form
        backer = int(body["Backers"])
        pledged = int(body["Pledged"])
        goals = int(body["Goals"])
        year = int(body["Year"])
        duration = int(body["Duration"])
        categories = int(body["Categories"])
        lenCategories = 14 - categories
        categoriesList = ['Art', 'Comics', 'Crafts', 'Dance', 'Design', 'Fashion', 'Film & Video', 'Food',
            'Games', 'Journalism', 'Music', 'Photography', 'Publishing', 'Technology', 'Theater']
        valueCategories = list(np.zeros(categories, dtype=int)) + list(np.ones(1, dtype=int)) + list(np.zeros(lenCategories, dtype=int))
        month = int(body["Month"])
        monthList = ['April', 'August', 'December', 'February', 'January', 'July', 'June', 'March', 'May',
            'November', 'October', 'September']

        toPredict = []
        toPredict = [[backer] + [pledged]+ [goals] + [year] + [duration] + valueCategories + [month]]
        results = model.predict(toPredict)[0]
        resultProba = model.predict_proba(toPredict)[0][0] * 100
        print(results)
        if results == 0:
            strResult = 'Failed'
            resultProba = round(model.predict_proba(toPredict)[0][0] * 100, 2)
        elif results == 1:
            strResult = 'Successful'
            resultProba = round(model.predict_proba(toPredict)[0][1] * 100, 2)

        return render_template('prediction.html', back = backer, ple = pledged, goal = goals, years = year, durations = duration,
        months = monthList[month], category = categoriesList[categories], result = strResult, proba = resultProba)

#, months = month,result = strResult
#---------------------------------------------------------------------
@app.route('/NotFound')
def notFound():
    return render_template('/error.html')
#--------------------------------------------------------
if __name__ == '__main__':
    model = joblib.load('best_lore')
    app.run(debug=True, port=5000)