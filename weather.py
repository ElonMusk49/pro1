import requests
import pandas as pd
from datetime import datetime, timedelta

# Define your API key and endpoint
API_KEY = '543e76ac486ba38f7363e47f1843ccb6'
LAT = '23.2599'  # Latitude for Madhya Pradesh (replace with specific location)
LON = '77.4126'  # Longitude for Madhya Pradesh (replace with specific location)
START_DATE = '2022-01-01'  # Updated start date (YYYY-MM-DD)
END_DATE = '2023-12-31'    # Updated end date (YYYY-MM-DD)

# Convert dates to UNIX timestamps
start_date = datetime.strptime(START_DATE, '%Y-%m-%d')
end_date = datetime.strptime(END_DATE, '%Y-%m-%d')

# Create a list to store all weather data
weather_records = []

# Loop through each day in the date range
current_date = start_date
while current_date <= end_date:
    timestamp = int(current_date.timestamp())
    
    # Construct the URL for historical data
    url = f"https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={LAT}&lon={LON}&dt={timestamp}&appid={API_KEY}&units=metric"
    
    # Make the request
    response = requests.get(url)
    data = response.json()
    
    # Extract relevant information
    for record in data.get('hourly', []):
        weather_records.append({
            'Date': datetime.utcfromtimestamp(record['dt']).strftime('%Y-%m-%d %H:%M:%S'),
            'Temperature': record['temp'],
            'Humidity': record['humidity'],
            'Precipitation': record.get('rain', {}).get('1h', 0),
            'Weather': record['weather'][0]['description']
        })
    
    # Move to the next day
    current_date += timedelta(days=1)

# Convert to DataFrame
weather_df = pd.DataFrame(weather_records)

# Save DataFrame to CSV
weather_df.to_csv('weather.csv', index=False)

print('Historical weather data saved to weather.csv')
