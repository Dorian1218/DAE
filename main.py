import requests

API_KEY = "e0e273ec69157acf236820e9973b3916"
cityname = "Stamford"
statecode = "CT"
countrycode = "US"
limit = 1
url = f"http://api.openweathermap.org/geo/1.0/direct?q={cityname},{statecode},{countrycode}&limit={limit}&appid={API_KEY}"
response = requests.get(url)
print(response.json())