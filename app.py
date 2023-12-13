from flask import Flask, render_template, request
from weather import main as get_weather
import numpy as np
import pickle

app = Flask(__name__)

with open('RandomForest.pkl', 'rb') as file:
    model = pickle.load(file)

def make_prediction(input_data):
    
    input_data = np.array(input_data).reshape(1, -1) 
    
    predicted_class = model.predict(input_data)
    predicted_prob = model.predict_proba(input_data)
    
    if np.max(predicted_prob) >= 0.50:
        return predicted_class[0]
    else:
        return None

@app.route('/')
def home():
    return render_template('index1.html')

# @app.route('/weather_info', methods=['POST'])
# def weather_info():
#     if request.method == 'POST':
#         return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        features = [float(request.form['nitrogen']),
                    float(request.form['phosphorus']),
                    float(request.form['potassium']),
                    float(request.form['temperature']),
                    float(request.form['humidity']),
                    float(request.form['ph']),
                    float(request.form['rainfall']),
                    ]
        user_input = [float(request.form.get('nitrogen')), float(request.form.get('phosphorus')), float(request.form.get('potassium')),
                    float(request.form.get('temperature')), float(request.form.get('humidity')), float(request.form.get('ph')),
                    float(request.form.get('rainfall'))]
        prediction1 = make_prediction(user_input)
        url = f"static/images/{prediction1}.jpg"
        if prediction1== None:
            prediction1 = 'Cant grow any crops'

        return render_template('result.html', prediction1=prediction1, url = url)

@app.route('/weather', methods = ['GET', 'POST'])
def weather():
    data = None
    if request.method == 'POST':
        data = get_weather()
        temp = data.temperature
        humidity = data.humidity
    return render_template('index1.html', temp = temp, humidity = humidity)

if __name__ == '__main__':
    app.run(debug=True)