import requests
import json
from flask import Flask, request, jsonify, render_template, url_for

app = Flask(__name__)
app.static_folder='static'
url = "https://facemaskprediction-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/1edb5a7d-1cc0-40e1-92d6-312a0c90e4a5/detect/iterations/Iteration2/url"


@app.route('/')
def home():
    #return 'Hello World'
    return render_template('home.html')

global result
result=""


@app.route('/predict',methods = ['POST'])
def predict():
    int_features =request.form.get('experience')
    payload = json.dumps(
        {
            "Url": "{}".format(int_features)
        }
    )
    headers = {
    'Prediction-Key': '1b32aafd5a3d44b898c69e105b5f8294',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    out=json.loads(response.text)
    predictions=out['predictions']
    max_prob=0.000001
    num=0
    for n,i in enumerate(predictions):
        if i['probability']>max_prob:
            max_prob=i['probability']
            num=n
    tag="Predicted Image Tag : {}".format(predictions[num]['tagName'])
    prob="Prediction Probability : {}".format(predictions[num]['probability']*100)
    return render_template('result.html',user_image=int_features,imgtag=tag,imgprob=prob)



@app.route('/predict_api',methods=['POST'])
def predict_api():
    data = request.get_json(force=True)
    payload = json.dumps(
        {
            "Url": "{}".format(data.values())
        }
    )
    headers = {
    'Prediction-Key': '1b32aafd5a3d44b898c69e105b5f8294',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    output = response
    return jsonify(output)



if __name__ == '__main__':
    app.static_folder='static'
    app.run(debug=True)
