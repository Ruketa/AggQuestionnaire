import requests

def request_add_questionnaire(url: str):

  req ={
    "id": "id",
    "satisfaction_level": 1,
    "recommendation_level": 2,
    "topics": "takoyaki",
    "participation_level": 3,
    "presentation_level": 4,
    "free_comment": "free comment",
    "holding_num": 2
  }

  with requests.post(url, json=req) as response:
    res = response.json()
    print(res)

url = "http://localhost:8000/api/questionnaire"

request_add_questionnaire(url)