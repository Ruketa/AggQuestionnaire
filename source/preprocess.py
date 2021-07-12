import pandas as pd
import Configurations as configs

def execute():
  # アンケート結果読込
  input_df = pd.read_excel(configs.PreprocessConfigration.InputDataPath, engine="openpyxl", sheet_name=0)
  base_df = pd.read_excel(configs.PreprocessConfigration.BaseDataPath, engine="openpyxl", sheet_name=2)
  base_df = base_df.drop(base_df.columns[[0]], axis=1)	

  # 年月日列を追加
  input_df["year"]  = input_df.iloc[:,1].apply(lambda x: x.year)
  input_df["month"] = input_df.iloc[:,1].apply(lambda x: x.month)
  input_df["day"]   = input_df.iloc[:,1].apply(lambda x: x.day)

  # 指定日付からのデータを抜き出す
  condition = f"month=={configs.PreprocessConfigration.Month} and day >= {configs.PreprocessConfigration.Day}"
  questionnaire_df = input_df.query(condition).reset_index()
  questionnaire_df = questionnaire_df.drop(["year", "month", "day"], axis=1)
  questionnaire_df = questionnaire_df.drop(questionnaire_df.columns[[0,1,2,3,4,5]], axis=1)

  # 開催回列を追加
  new_data_df = pd.DataFrame(columns=["開催回"], data=[configs.PreprocessConfigration.HoldingNum]*len(questionnaire_df))
  new_data_df = pd.concat([new_data_df, questionnaire_df], axis=1)

  # 指定開催回のデータを結合
  agg_df = pd.concat([base_df, new_data_df])

  # CSVで出力
  filename = configs.PreprocessConfigration.OutputDir + "Questionnaire.csv"
  agg_df.to_csv(filename, index=False, encoding="cp932")

  return