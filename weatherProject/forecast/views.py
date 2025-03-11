from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings


# Import Libraries ---------------------------------------------------------------------
import requests # This library helps to fetch data from API
import pandas as pd # used for handling and analyzing data
import numpy as np # used for numerical operations
from sklearn.model_selection import train_test_split # used to split data into training and testing sets
from sklearn.preprocessing import LabelEncoder # used to convert categorical data into numerical values
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor # models for classification and regression tasks
from sklearn.metrics import mean_squared_error # to measure the accuracy of prediction
from datetime import datetime, timedelta # to handle date and time 
import pytz # for timezone
import os


API_KEY = settings.API_KEY # API key that was created using "OpenWeatherMap APIs"
BASE_URL = settings.BASE_URL # base url for making API requests, copied from "Postman" page


# 1. Fetch Current Weather Data ---------------------------------------------------------------------
def get_current_weather(city):
  url = f"{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric" # construct the API request URL
  response = requests.get(url) # send the get request to API
  data = response.json()
  return {
      'city': data['name'],
      'current_temp': round(data['main']['temp']),
      'feels_like': round(data['main']['feels_like']),
      'temp_min': round(data['main']['temp_min']),
      'temp_max': round(data['main']['temp_max']),
      'humidity': round(data['main']['humidity']),
      'description': data['weather'][0]['description'],
      'country': data['sys']['country'],
      'wind_gust_dir': data['wind']['deg'],
      'pressure': data['main']['pressure'],
      'Wind_Gust_Speed': data['wind']['speed'],
      
      'clouds': data['clouds']['all'],
      'visibility': data.get('visibility', 0),

  }
# 2. Read Historical Data ---------------------------------------------------------------------
def read_historical_data(filename):
  df = pd.read_csv(filename) # load csv file into DataFrame
  df = df.dropna() # remove rows with missing values
  df = df.drop_duplicates() # remove duplicate data
  return df


# 3. Prepare Data For Training ---------------------------------------------------------------------
def prepare_data(data):
  le = LabelEncoder() #create a LabelEncoder instance
  data['WindGustDir'] = le.fit_transform(data['WindGustDir'])
  data['RainTomorrow'] = le.fit_transform(data['RainTomorrow'])

  # define the feature variable and target variables
  X = data[['MinTemp', 'MaxTemp', 'WindGustDir', 'WindGustSpeed', 'Humidity', 'Pressure', 'Temp']] # feature variables
  y = data['RainTomorrow'] # target variable

  return X, y, le # return feature variable, target variable and the label encoder


# 4. Train Rain Prediction Model (random forest) ---------------------------------------------------------------------
def train_rain_model(X, y):
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
  model = RandomForestClassifier(n_estimators=100, random_state=42)
  model.fit(X_train, y_train)

  y_pred = model.predict(X_test) # to make predictions on test set

  # print("Mean Squared Error for Rain Model")

  # print(mean_squared_error(y_test, y_pred))

  return model


# 5. Prepare Regression Data ---------------------------------------------------------------------
def prepare_regression_data(data, feature):
  X, y = [], [] # initialize list for feature and target values

  for i in range(len(data) - 1):
    X.append(data[feature].iloc[i])

    y.append(data[feature].iloc[i+1])

  X = np.array(X).reshape(-1, 1)
  y = np.array(y)
  return X, y


# 6. Train Regression Model ---------------------------------------------------------------------
def train_regression_model(X, y):
  model = RandomForestRegressor(n_estimators=100, random_state=42)
  model.fit(X, y)
  return model


# 7. Predict Future ---------------------------------------------------------------------
def predict_future(model, current_value):
  predictions = [current_value]

  for i in range(7):
    next_value = model.predict(np.array([[predictions[-1]]]))

    predictions.append(next_value[0])

  return predictions[1:]


# 8. Weather Analysis Function ---------------------------------------------------------------------
def weather_view(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        current_weather = get_current_weather(city)

        # load historical data
        
        csv_path = os.path.join('../csv/weather.csv')
        historical_data = read_historical_data(csv_path) 

        # prepare and train the rain prediction model

        X, y, le = prepare_data(historical_data)

        rain_model = train_rain_model(X, y)

        # map wind direction to compass points
        wind_deg = current_weather['wind_gust_dir'] % 360
        compass_points = [
            ("Ν", 0, 11.25), ("NNE", 11.25, 33.75), ("NE", 33.75, 56.25),
            ("ENE", 56.25, 78.75), ("E", 78.75, 101.25), ("ESE", 101.25, 123.75),
            ("SE", 123.75, 146.25), ("SSE", 146.25, 168.75), ("S", 168.75, 191.25),
            ("SSW", 191.25, 213.75), ("SW", 213.75, 236.25), ("WSW", 236.25, 258.75),
            ("W", 258.75, 281.25), ("WNW", 281.25, 303.75), ("MW", 303.75, 326.25),
            ("NNW", 326.25, 348.75)
        ]
        
        compass_direction = next(point for point, start, end in compass_points if start <= wind_deg < end)

        compass_direction_encoded = le.transform([compass_direction])[0] if compass_direction in le.classes_ else -1

        current_data = {
            'MinTemp': current_weather['temp_min'],
            'MaxTemp': current_weather['temp_max'],
            'WindGustDir': compass_direction_encoded,
            'WindGustSpeed': current_weather['Wind_Gust_Speed'],
            'Humidity': current_weather['humidity'],
            'Pressure': current_weather['pressure'],
            'Temp': current_weather['current_temp'],
        }

        current_df = pd.DataFrame([current_data])

        # rain prediction

        rain_prediction = rain_model.predict(current_df)[0]

        # prepare regression model for temperature and humidity

        X_temp, y_temp = prepare_regression_data(historical_data, 'Temp')

        X_hum, y_hum = prepare_regression_data(historical_data, 'Humidity')

        temp_model = train_regression_model(X_temp, y_temp)

        hum_model = train_regression_model(X_hum, y_hum)

        # predict future temperature and humidity

        future_temp = predict_future(temp_model, current_weather['temp_min'])

        future_humidity = predict_future(temp_model, current_weather['humidity'])

        # prepare time for future predictions

        timezone = pytz.timezone('Asia/Kolkata')
        now = datetime.now(timezone)
        next_hour = now + timedelta(hours=1)
        next_hour = next_hour.replace(minute=0, second=0, microsecond=0)

        future_times = [(next_hour + timedelta(hours=i)).strftime("%H:00") for i in range(7)]
        
        # store each value separately
        
        time1, time2, time3, time4, time5, time6, time7 = future_times
        temp1, temp2, temp3, temp4, temp5, temp6, temp7 = future_temp
        hum1, hum2, hum3, hum4, hum5, hum6, hum7 = future_humidity
        
        # Pass data to template
        
        context = {
            'location': city,
            'current_temp': current_weather['current_temp'],
            'MinTemp': current_weather['temp_min'],
            'MaxTemp': current_weather['temp_max'],
            'feels_like': current_weather['feels_like'],
            'humidity': current_weather['humidity'],
            'clouds': current_weather['clouds'],
            'description': current_weather['description'],
            'city': current_weather['city'],
            'country': current_weather['country'],
            
            'time': datetime.now(),
            'date': datetime.now().strftime("%B %d, %Y"),
            
            'wind': current_weather['Wind_Gust_Speed'],
            'pressure': current_weather['pressure'],
            
            'Visibility': current_weather.get('visibility', 0 ),

            'time1': time1,
            'time2': time2,
            'time3': time3,
            'time4': time4,
            'time5': time5,
            'time6': time6,
            'time7': time7,
            
            'temp1': f"{round(temp1, 1)}",
            'temp2': f"{round(temp2, 1)}",
            'temp3': f"{round(temp3, 1)}",
            'temp4': f"{round(temp4, 1)}",
            'temp5': f"{round(temp5, 1)}",
            'temp6': f"{round(temp6, 1)}",
            'temp7': f"{round(temp7, 1)}",
            
            'hum1': f"{round(hum1, 1)}",
            'hum2': f"{round(hum2, 1)}",
            'hum3': f"{round(hum3, 1)}",
            'hum4': f"{round(hum4, 1)}",
            'hum5': f"{round(hum5, 1)}",
            'hum6': f"{round(hum6, 1)}",
            'hum7': f"{round(hum7, 1)}",
        }
        
        return render(request, 'weather.html', context)
    
    return render(request, 'weather.html')


  