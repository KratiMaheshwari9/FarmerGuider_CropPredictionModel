from flask import Flask, request, render_template
import joblib
import sqlite3
import pandas as pd

app = Flask(__name__)

# Load the machine learning model and scaler
model = joblib.load('./models/kmeans_model.lb')
scaler = joblib.load('./models/standardscalar.lb')

# Load the filtering.csv file
filtering_df = pd.read_csv('./models/filtering_data.csv')

# Dictionary mapping English crop names to their Hindi equivalents
crop_translations = {
    'maize': 'मक्का',
    'pigeonpeas': 'अरहर',
    'mothbeans': 'मटकी',
    'mungbean': 'मूंग',
    'blackgram': 'उड़द',
    'lentil': 'मसूर',
    'mango': 'आम',
    'orange': 'संतरा',
    'papaya': 'पपीता',
    'coconut': 'नारियल',
    'cotton': 'कपास',
    'jute': 'जूट',
    'coffee': 'कॉफी',
    'pomegranate': 'अनार',
    'banana': 'केला',
    'grapes': 'अंगूर',
    'watermelon': 'तरबूज',
    'muskmelon': 'खरबूजा',
    'apple': 'सेब',
    'chickpea': 'चना',
    'kidneybeans': 'राजमा',
    'mothbean': 'मटकी'
}

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route for the home page
@app.route('/')
def home():
    return render_template('home.html')

# Route for the project form page
@app.route('/project')
def project():
    return render_template('project.html')

# Route for handling the prediction and saving data
@app.route('/prediction', methods=['POST'])
def prediction():
    if request.method == 'POST':
        
        N = float(request.form['N'])
        P = float(request.form['P'])
        K = float(request.form['K'])
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])

        # Prepare data for prediction
        data = [[N, P, K, temperature, humidity, ph, rainfall]]
        data_transformed = scaler.transform(data)
        cluster_prediction = model.predict(data_transformed)[0]

        # Filter the CSV file based on the predicted cluster
        filtered_crops = filtering_df[filtering_df['cluster_no'] == cluster_prediction]['label'].unique().tolist()

        # Map the crops to their Hindi names
        translated_crops = [(crop, crop_translations.get(crop, crop)) for crop in filtered_crops]

        # Save data to SQLite database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO predictions (N, P, K, temperature, humidity, ph, rainfall, prediction)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
            (N, P, K, temperature, humidity, ph, rainfall, ', '.join(filtered_crops)))
        conn.commit()
        conn.close()

        return render_template('output.html', crops=translated_crops)

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
