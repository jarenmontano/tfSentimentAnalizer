import datetime
import textwrap

from flask import Flask, render_template, request
import requests
# https://requests.readthedocs.io/en/latest/
import json

from tfmodel import trainingmodel, RunTfModel
from sklearnmodel import trainmodel, run_sk_model

# global variables
results = ""
sk_results = ""

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def index():
    global results
    results = trainingmodel()
    trainmodel()
    return render_template("index.html" , accuracy = (results['Accuracy'] * 100) , loss = results['Loss'], r2 = results['r2_score'])

@app.route("/review", methods = ['POST'])
def return_response():
    global results
    user_prompt = request.form["user_prompt"]
    responce = RunTfModel(user_prompt)
    sk_response = run_sk_model(user_prompt)
    return render_template("index.html" , model_prediction = responce, sk_response = sk_response, user_prompt=user_prompt , accuracy = (results['Accuracy'] * 100) , loss = results['Loss'], r2 = results['r2_score'])



if __name__ == "__main__":
    app.run(debug=True)



    