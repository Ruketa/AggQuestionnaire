from source.Configurations import PreprocessConfigration
import pandas as pd
from typing import List

from requester import AddQuestionnaireDataRequester

class preprocessor(object):

  def __init__(self, configuration):
    self.__configuration = configuration
    return

  # 指定日付からのデータを抜き出す
  def __extract_new_data(self, input_df: pd.DataFrame)->pd.DataFrame:
    # 年月日列を追加
    input_df["year"]  = input_df.iloc[:,1].apply(lambda x: x.year)
    input_df["month"] = input_df.iloc[:,1].apply(lambda x: x.month)
    input_df["day"]   = input_df.iloc[:,1].apply(lambda x: x.day)

    # 指定日付からのデータを抜き出す
    condition = f"month=={self.__configuration.Month} and day >= {self.__configuration.Day}"
    questionnaire_df = input_df.query(condition).reset_index()
    questionnaire_df = questionnaire_df.drop(["year", "month", "day"], axis=1)
    questionnaire_df = questionnaire_df.drop(questionnaire_df.columns[[0,1,2,3,4,5]], axis=1)

    # 開催回列を追加
    new_data_df = pd.DataFrame(columns=["開催回"], data=[self.__configuration.HoldingNum]*len(questionnaire_df))
    new_data_df = pd.concat([new_data_df, questionnaire_df], axis=1)

    return new_data_df

  # アンケート結果読込
  def execute(self):

    # アンケート結果読込
    input_df = pd.read_excel(self.__configuration.InputDataPath, engine="openpyxl", sheet_name=0)

    # 指定日付からの新規データを抜き出す
    new_data_df = self.__extract_new_data(input_df)

    # データ追加リクエスト
    requester = AddQuestionnaireDataRequester(url=PreprocessConfigration.DbServiceUrl)

    for row in new_data_df.values:
      addData = {}
       
      addData["holding_num"]          = row[0]
      addData["satisfaction_level"]   = row[1]
      addData["recommendation_level"] = row[2]
      addData["topics"]               = row[3]
      addData["participation_level"]  = row[4]
      addData["presentation_level"]   = row[5]
      addData["free_comment"]         = row[6]

      requester.post_data(addData)
