import requests
from requests.api import request
from requests.sessions import default_headers

from typing import Dict, List

#url = "http://localhost:8000/api/questionnaire"

class AddQuestionnaireDataRequester(object):

  def __init__(self, url:str):
    self.__URL = url

    self.__default_data ={
      "id": "id",
      "satisfaction_level": 1,
      "recommendation_level": 1,
      "topics": "",
      "participation_level": 1,
      "presentation_level": 1,
      "free_comment": "",
      "holding_num": 0
    }

  def post_data(self, addData: Dict):

    # prepare the request parameter
    requestParameter = self.__default_data.copy()
    for val, key in addData.items():
      requestParameter[key] = val

    # post request
    with requests.post(self.__URL, json=requestParameter) as response:
      res = response.json()

    return res

  def post_multi_data(self, addDataList:List[Dict]):
    
    results = []

    # prepare the request parameter
    for addData in addDataList:
      requestParameter = self.__default_data.copy()
      for val, key in addData.items():
        requestParameter[key] = val

      # post request
      with requests.post(self.__URL, json=requestParameter) as response:
        results.append(response.json())

    return results