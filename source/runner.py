import aggregation
import Configurations as configs
from aggregation import AggCategoricalData, AggTopicData
from preprocess import preprocess

def main():
  
  # preprocess
  preprocessor = preprocess.preprocessor(configs.PreprocessConfigration)
  preprocess.execute()

  return

if __name__ == "__main__":
  main()