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
        goals = int(body["Goals"])
        duration = int(body["Duration"])
        name = body["Name"]
        lenName = len(name)
        categories = int(body["Categories"])
        lenCategories = 14 - categories
        categoriesList = ['Art', 'Comics', 'Crafts', 'Dance', 'Design', 'Fashion', 'Film & Video', 'Food',
            'Games', 'Journalism', 'Music', 'Photography', 'Publishing', 'Technology', 'Theater']
        valueCategories = list(np.zeros(categories, dtype=int)) + list(np.ones(1, dtype=int)) + list(np.zeros(lenCategories, dtype=int))
        month = int(body["Month"])
        lenMonth = 11 - month
        monthList = ['April', 'August', 'December', 'February', 'January', 'July', 'June', 'March', 'May',
            'November', 'October', 'September']
        valueMonth = list(np.zeros(month, dtype=int)) + list(np.ones(1, dtype=int)) + list(np.zeros(lenMonth, dtype=int))
        countries = int(body["Country"])
        lenCountries = 21 - countries
        valueCountries = list(np.zeros(countries, dtype=int)) + list(np.ones(1, dtype=int)) + list(np.zeros(lenCountries, dtype=int))

        
        countryList = ['AT','AU', 'BE', 'CA', 'CH', 'DE', 'DK', 'ES', 'FR', 'GB', 'HK', 'IE', 'IT', 'JP',
        'LU', 'MX', 'NL', 'NO', 'NZ', 'SE', 'SG', 'US']
        

        toPredict = []
        toPredict = [[duration] + [goals] + [lenName] + valueCategories + valueMonth + valueCountries]
        print(valueCountries)
        results = model.predict(toPredict)[0]
        resultProba = model.predict_proba(toPredict)[0][0] * 100
        print(toPredict)
        if results == 0:
            strResult = 'Failed'
            resultProba = round(model.predict_proba(toPredict)[0][0] * 100, 2)
        elif results == 1:
            strResult = 'Successful'
            resultProba = round(model.predict_proba(toPredict)[0][1] * 100, 2)

        return render_template('prediction.html',names = name, goal = goals, durations = duration, country = countryList[countries],
        months = monthList[month], category = categoriesList[categories], result = strResult, proba = resultProba)

#, months = month,result = strResult
#---------------------------------------------------------------------
@app.route('/NotFound')
def notFound():
    return render_template('/error.html')
#--------------------------------------------------------
if __name__ == '__main__':
    model = joblib.load('best_RFC')
    app.run(debug=True, port=5000)