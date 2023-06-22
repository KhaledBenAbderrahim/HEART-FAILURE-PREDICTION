import pickle
from flask import Flask, request,app,jsonify,render_template
import numpy as np
import pandas as pd
import json

scaler = pickle.load(open('./models/scaler.pkl','rb'))
pickled_model = pickle.load(open('./models/SVModel.pkl','rb'))


app = Flask(__name__)

#load the model
scaler = pickle.load(open('./models/scaler.pkl','rb'))
svmodel = pickle.load(open('./models/SVModel.pkl','rb'))

@app.route('/')
def home():
    return render_template('home.html',prediction_text="The House price prediction is {}".format(1))

# create API for testing
@app.route('/predict_api',methods=['POST'])
def predict_api():
    data = request.json
    print(data)
    dataframe = pd.DataFrame.from_dict(data)
    scaler_result = scaler.transform(dataframe)
    prediction = pickled_model.predict(scaler_result)
    print(prediction)
    return jsonify(str(prediction[0]))


@app.route('/predict',methods=['POST'])
def predict():
    data=[str(x) for x in request.form.values()]
    print(data)
    return render_template("home.html",prediction_text="The House price prediction is {}".format(1))  


if __name__ == "__main__":
    app.run(debug=True)


