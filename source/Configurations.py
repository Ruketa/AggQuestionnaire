class AggConfiguration:
	QuestionairePath = "./data/Questionnaire_new.xlsx"
	DataPath = "./output/Questionnaire.csv"
	HoldingNum = 11 
	AggTargetCols = [1, 2, 4, 5]
	AggTopicCol = 3

class PreprocessConfigration:
	OutputDir = "./output/"
	BaseDataPath = "./data/Questionnaire.xlsx"
	InputDataPath = "./data/Questionnaire_new.xlsx"
	Month = 7
	Day = 7
	HoldingNum = 11