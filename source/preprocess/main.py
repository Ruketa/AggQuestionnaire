from numpy.core.arrayprint import printoptions
from Configuration import PreprocessConfigration
from preprocess import preprocessor

def main():

  # 前処理実行
  pp = preprocessor(PreprocessConfigration)
  pp.execute()

  return

if __name__ == "__main__":
  main()