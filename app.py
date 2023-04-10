import requests
import mysql.connector
from flask import Flask, render_template, request

# Create a Flask app
app = Flask(__name__)

# Define the API endpoint and parameters
url = 'http://api.openweathermap.org/data/2.5/weather'
params = {
    'q': 'New York',
    'units': 'metric',
    'appid': '2d308242690bf00f98b9b00d5af768aa',
}

# Define the MySQL connection
conn = mysql.connector.connect(
    host='sql7.freemysqlhosting.net',
    user='sql7612055',
    password='fF3vnHsKjy',
    database='sql7612055',
)

# Define the MySQL cursor
cursor = conn.cursor()

# Define a function to fetch the weather data and store it in the database
def fetch_and_store_data():
    # Make the API request
    response = requests.get(url, params=params)

    # Parse the JSON response
    data = response.json()

    # Extract the data
    city = data['name']
    temp = data['main']['temp']
    humidity = data['main']['humidity']
    pressure = data['main']['pressure']
    description = data['weather'][0]['description']

    # Insert the data into the database
    cursor.execute(
        'INSERT INTO weather (city, temp, humidity, pressure, description) VALUES (%s, %s, %s, %s, %s)',
        (city, temp, humidity, pressure, description)
    )

    # Commit the transaction
    conn.commit()

# Define a route to fetch and store the weather data
@app.route('/fetch-data', methods=['POST'])
def fetch_data():
    fetch_and_store_data()
    #return the most recent stored data in the above of the line, by using display_data() function
    return display_data()

# Define a route to display the weather data
@app.route('/')
def display_data():
    cursor.execute('SELECT * FROM weather ORDER BY timestamp DESC LIMIT 10')
    data = cursor.fetchall()
    return render_template('weather.html', data=data)

# Run the Flask app
if __name__ == '__main__':
    # Create the weather table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            id INT AUTO_INCREMENT PRIMARY KEY,
            city VARCHAR(255),
            temp FLOAT,
            humidity FLOAT,
            pressure FLOAT,
            description VARCHAR(255),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    # Run the app
    app.run(debug=True)
