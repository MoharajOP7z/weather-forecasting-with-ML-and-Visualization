# 🌦 Weather Forecasting App

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-239120?&style=for-the-badge&logo=css3&logoColor=white)
![JS](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Python](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![OpenWeatherMap](https://img.shields.io/badge/OpenWeatherMap.org-API-008CC1?style=for-the-badge&logo=openweathermap.org&logoColor=white)
![Chart](https://img.shields.io/badge/Chart.js-Visualization-008CC1?style=for-the-badge&logo=openweathermap&logoColor=white)



The Weather Forecast App is an advanced and user-friendly Django-based web 
application designed to provide accurate and real-time weather updates for 
users across the globe. By leveraging cutting-edge technology and integrating 
with reliable weather APIs, the app delivers current weather conditions, 
including temperature, humidity, and descriptive summaries, tailored to the 
user’s preferred locations. 
This app is designed with simplicity and scalability in mind. It offers users the 
ability to search for weather information by city name and country, making it an 
excellent tool for travelers, professionals, or anyone planning daily activities. 
The Weather Forecast App ensures a seamless and engaging user experience by 
incorporating a responsive front-end that adapts to various devices, from 
desktops to smartphones. 
Beyond its primary features, the app’s backend architecture is robust and 
flexible, using Django’s Model-View-Template (MVT) pattern to ensure 
efficient data handling and rendering. With caching mechanisms in place, it 
optimizes API calls and improves performance, reducing the need for repetitive 
data retrieval. Furthermore, the app can be easily extended to include additional 
functionalities like multi-language support, severe weather alerts, and 7-day 
forecasts. 
Built with developers in mind, the project comes with clear and structured 
documentation, making it easy to set up locally or deploy on production 
servers. Its modular design allows for smooth integration with other services, 
ensuring adaptability for future enhancements and scalability for larger 
audiences.Technical Stack and Library Packages.

## 🌟 Features
- 🌍 Real-time weather data from OpenWeatherMap API.
- :sun_behind_rain_cloud:  temperature, humidity, etc. and weather condition forecasts.
- 📊 Machine learning-based rain prediction.
- 📅 7-day weather forecast with detailed analytics.
- 📌 User-friendly web interface.

##  :large_blue_diamond:  ScreenShots

![App Screenshot](https://github.com/MoharajOP7z/weather-forecasting-with-ML-and-Visualization/blob/b47dee6f699f2d7e663fd4528e18db2ce0d87495/screenshot/Screenshot%202025-03-11%20174643.png)


## 🚀 Live Demo
Check out the live demo 👉 [Click Here](https://your-demo-link.com)

### 📃 Folder Structure
```bash
C:.
├───forecast
│   ├───migrations
│   │   └───__pycache__
│   ├───static
│   │   ├───css
│   │   ├───img
│   │   │    └───[weather-related images] 
│   │   └───js
│   │       └───chartSetup.js
│   ├───templates
│   │   └───Weather.html
│   └───__pycache__
└───weatherProject
    └───__pycache__
```

### 📥 1️⃣ Create a Virtual Environment
```bash
python -m venv env
# On linux or mac user
source env/bin/activate  
# On Windows user
.\env\Scripts\activate # samething env\Scripts\activate
```
### 📥 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt 
# If you get permission errors, try:
pip install --user -r requirements.txt
# Or
python3 -m pip install -r requirements.txt
```
```
asgiref==3.8.1
certifi==2024.12.14
charset-normalizer==3.4.1
Django==5.1.5
idna==3.10
joblib==1.4.2
numpy==2.2.2
pandas==2.2.3
python-dateutil==2.9.0.post0
python-dotenv==1.0.1
pytz==2024.2
requests==2.32.3
scikit-learn==1.6.1
scipy==1.15.1
six==1.17.0
sqlparse==0.5.3
threadpoolctl==3.5.0
tzdata==2025.1
urllib3==2.3.0

```

## 📥 :three: Install Project
Follow these steps to set up the project locally:

###  :small_blue_diamond: Clone the Repository
```bash
git clone https://github.com/MoharajOP7z/weather-forecasting-with-ML-and-Visualization.git
```
###  :small_blue_diamond: Go to Project directory

```bash
cd weatherProject
```
###  :small_blue_diamond: Set Up Environment Variables
Rename ```.env-example``` to ```.env``` file in the project :

```bash
API_KEY=Your-Secret-API-KEY # take it from OpenWeatherMap
BASE_URL=https://api.openweathermap.org/data/2.5/
```

###  :pushpin: If You get a problem about csv file 
copy the ```path``` of ```weather.csv``` file , after that ```paste``` the path ```csv_path = os.path.join('HERE')```
the path look like this
```C:/Users/Desktop/Django/csv/weather.csv```
change ```/``` to ```\\```
```bash
# load historical data  
        csv_path = os.path.join('C:\\Users\\Desktop\\Django\\csv\\weather.csv')
        historical_data = read_historical_data(csv_path)
```

###  :pushpin: If You don't know How to get the OpenWeatherMap API Key
Follow these steps:
###### :one: Go to [OpenWeatherMap](https://openweathermap.org/)
###### :two: Sign up for an account
###### :three: Go to your dashboard and click on API keys
###### :four: Click on "Generate API key" And Name it
###### :five: Copy the API key and paste it in the .env file
in this Context ```Your-Secret-API-KEY``` No Gap
```bash
API_KEY=Your-Secret-API-KEY # take it from OpenWeatherMap
BASE_URL=https://api.openweathermap.org/data/2.5/
```
##### ❗🚫 Sharing an ```API KEY``` is generally considered a security risk as it allows unauthorized access to your application or service, potentially leading to data breaches, excessive usage, or even account compromise 🚫❗

### 📥  Run app

Runs the app in the development mode.

Open http://127.0.0.1:8000/ to view it in your browser.

The page will reload when you make changes. You may also see any lint errors in the console
