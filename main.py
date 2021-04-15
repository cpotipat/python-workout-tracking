import requests
import os
from datetime import datetime

APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")
TOKEN = os.environ.get("TOKEN")
GENDER = "female"
WEIGHT_KG = 52
HEIGHT_CM = 165
AGE = 25

sheet_endpoint = os.environ.get("YOUR_SHEET_ENDPOINT")
exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
exercise_type = input("Tell me which exercise you did?: ")

header = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

body = {
    "query": exercise_type,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

exercise_response = requests.post(url=exercise_endpoint, headers=header, json=body)
exercise_response.raise_for_status()
exercise_result = exercise_response.json()
print(exercise_result)

today = datetime.now().strftime("%d/%m/%Y")
time = datetime.now().strftime("%X")

for workout in exercise_result["exercises"]:

    bearer_token = {
        "Authorization": f"Bearer {TOKEN}"
    }

    sheet_body = {
        "workout": {
            "date": today,
            "time": time,
            "exercise": workout["name"].title(),
            "duration": workout["duration_min"],
            "calories": workout["nf_calories"]
        }
    }

    sheet_response = requests.post(sheet_endpoint, headers=bearer_token, json=sheet_body)
    sheet_response.raise_for_status()
    print(sheet_response.json())
