from flask import Flask, request, jsonify
import requests
from datetime import datetime
import pytz
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def fetch_data(ticker):
    try:
        # Make a GET request to the Alpha Vantage API
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=60min&apikey=C19QLKFC1V8L8WRI'
        headers = {'User-Agent': 'python-requests'}
        response = requests.get(url, headers=headers)
        
        # Check if the response status is 200 (OK)
        if response.status_code == 200:
            print("Data is successfully received as a JSON object:")
            
            # Modify the JSON object 
            data = response.json()
            time_series_key = 'Time Series (60min)'
            
            if time_series_key in data:
                chart_data = []
                
                # Convert the JSON object to a list of data points
                for time_key, item in data[time_series_key].items():
                    # Convert timeKey to timestamp
                    date = datetime.strptime(time_key, '%Y-%m-%d %H:%M:%S')
                    unix_timestamp = int(date.timestamp())
                    
                    # Append the formatted data
                    chart_data.append({
                        'time': unix_timestamp,
                        'open': float(item['1. open']),
                        'high': float(item['2. high']),
                        'low': float(item['3. low']),
                        'close': float(item['4. close']),
                    })
                
                # Log the format of unsorted chartData
                print(chart_data)
                return chart_data
            else:
                print('Data format error: Time Series not found in response.')
                return []
        else:
            print('Status:', response.status_code)
            return []
    except Exception as err:
        print('Error:', str(err))
        return []

# Handle GET request for time series data
@app.route('/', methods=['GET'])
def get_time_series_data():
    try:
        ticker = request.args.get('ticker')
        data = fetch_data(ticker)
        return jsonify(data)
    except Exception as error:
        print("An error occurred when handling user request:", str(error))
        return jsonify({'error': str(error)}), 500

if __name__ == '__main__':
    app.run(port=3000)

