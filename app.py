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
        categories = body["Categories"]
        print(categories)
        lenCategories = 14 - int(categories)
        valueCategories = list(np.zeros(int(categories), dtype=int)) + list(np.ones(1, dtype=int)) + list(np.zeros(lenCategories, dtype=int))
        month = int(body["Month"])
        monthValue = df[df['encoded_months'] == month]['launched_month'].values[0]
        toPredict = list(backer) + list(pledged) + list(goals) + list(year) + list(duration) + valueCategories + valueMonth
        results = model.predict(toPredict)
        if results == 0:
            strResult = 'Failed'
        elif results == 1:
            strResult = 'Successful'

        return render_template('prediction.html', back = backer, ple = pledged, goal = goals, years = year, durations = duration,
        months = monthValue, category = categories, result = strResult)

#, months = month,result = strResult
#---------------------------------------------------------------------
@app.route('/NotFound')
def notFound():
    return render_template('/error.html')
#--------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)
    model = joblib('best_lore')
    df = pd.read_csv('cleaned_kickstarter_dateset.csv')