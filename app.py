import pickle
from flask import Flask, request,app,jsonify,render_template
import numpy as np
import pandas as pd


scaler = pickle.load(open('./models/scaler.pkl','rb'))
pickled_model = pickle.load(open('./models/SVModel.pkl','rb'))


app = Flask(__name__)

#load the model
scaler = pickle.load(open('./models/scaler.pkl','rb'))
svmodel = pickle.load(open('./models/SVModel.pkl','rb'))

@app.route('/', methods = ['GET'])
def home():
    age=request.form.get('age')
    print(age)
    return render_template('home.html',age=age)

# create API for testing
@app.route('/predict_api',methods=['POST'])
def predict_api():
    data = request.json
    print(data)
    dataframe = pd.DataFrame.from_dict(data)
    scaler_result = scaler.transform(dataframe)
    prediction = pickled_model.predict(scaler_result)
    print(prediction)
    return jsonify("dead" if str(prediction[0]) else "still alive")


@app.route('/predict',methods=['POST','GET'])
def predict():
    if request.method == 'POST':
        age= request.form.get('age')
        anemia = 1 if  request.form.get('anemia') =="yes" else 0
        cpk = request.form.get('cpk')
        diabetes = 1 if  request.form.get('diabetes') =="yes" else 0
        bp = 1 if  request.form.get('bp') =="yes" else 0
        ef = request.form.get('ef')
        platelets = request.form.get('platelets')
        creatinine = request.form.get('creatinine')
        sodium = request.form.get('sodium')
        gender = 1 if request.form.get('gender') == 'male' else 0 
        smoking = 1 if  request.form.get('smoking') =="yes" else 0
        time = request.form.get('time')

    data = {
        'age' : age,
        'anemia': "Yes" if anemia == 1 else "No",
        'cpk' : cpk ,
        'diabetes' : "Yes" if diabetes == 1 else "No",
        'bp' : "Yes" if bp == 1 else "No",
        'ef':ef,
        'platelets':platelets,
        'creatinine':creatinine,
        'sodium':sodium,
        'gender':"Male" if gender == "male" else "Female",
        'smoking': "Yes" if smoking == 1 else "No",
        'time': time


    }
    print(age,anemia,cpk,diabetes,bp,ef,platelets,creatinine,sodium,gender,smoking,time)

    dataframe = pd.DataFrame({
	    'age': int(age),
	    'anaemia': int(anemia),
	    'creatinine_phosphokinase': int(cpk),
	    'diabetes': int(diabetes),
	    'ejection_fraction': int(ef),
	    'high_blood_pressure': int(bp),
	    'platelets': int(platelets),
	    'serum_creatinine': int(creatinine),
	    'serum_sodium': int(sodium),
	    'sex': int(gender),
	    'smoking': int(smoking),
	    'time': int(time),
        },index=[0])

    #print("scaler result -------------:", data_to_predict)
    print(dataframe)
    scaler_result = scaler.transform(dataframe)
    print(scaler_result)
    prediction = pickled_model.predict(scaler_result)
    print("the prediction------", prediction[0])
    result = "there is dying possibility" if prediction[0] == 1 else "there is no dying possibility"

    
    return render_template("modal.html",data = data, result = result)  


if __name__ == "__main__":
    app.run(debug=True,port=8000,host="0.0.0.0")


