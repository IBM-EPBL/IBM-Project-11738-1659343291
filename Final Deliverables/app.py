from flask import Flask, render_template, request
import numpy as np

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "648tNOQBKDDhov8wI4xnas4l_BZtvHGiQ3vBKpJaXKf4"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


app = Flask(__name__)


@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        sg = float(request.form['sg'])
        htn = float(request.form['htn'])
        hemo = float(request.form['hemo'])
        dm = float(request.form['dm'])
        al = float(request.form['al'])
        appet = float(request.form['appet'])
        rc = float(request.form['rc'])
        pc = float(request.form['pc'])

        values = [[sg, htn, hemo, dm, al, appet, rc, pc]]
 
        # NOTE: manually define and pass the array(s) of values to be scored in the next line
        payload_scoring = {"input_data": [{"fields": [['sg','htn','hemo','dm','al','appet','rc','pc']], "values": values}]}

        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/6f9799c9-0173-44c4-9262-43fa3d05ec84/predictions?version=2022-11-19', json=payload_scoring,
          headers={'Authorization': 'Bearer ' + mltoken})
        print("Scoring response")
        print(response_scoring.json())
        prediction = response_scoring.json()
        predicted=prediction['predictions'][0]['values'][0][0]
        return render_template('result.html', prediction=predicted)


if __name__ == "__main__":
    app.run(debug=True)