import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import japanize_matplotlib
import MeCab

from typing import List

class AggCategoricalData():

  def __init__(self, input_data_path: str, holding_num: int, target_cols: List[int]):
    self.__input_data_path = input_data_path
    self.__holding_num = holding_num
    self.__target_cols = target_cols
    return

  def __bar_plot_5_grade_evaluation(self, left, right, title):
    # initialize 5 grades
    agg_target = {}
    for idx in range(5):
      agg_target[idx+1] = 0
  
    for k, v in zip(left, right):
      agg_target[k] = v

    # plot 
    fig = plt.figure(figsize=(5, 4))
    plt.title(title, fontsize=18)
    plt.xlabel("評価")
    plt.ylabel("投票数")
    plt.ylim(0, max(right) + 2)
    for i in range(len(agg_target)):
      plt.text(x=i+1, y=agg_target[i+1]+1, s=agg_target[i+1], ha="center", va="top", fontsize=14)
    plt.bar(agg_target.keys(), agg_target.values(), color="b", alpha=0.5)
    plt.savefig("./output/" + title + ".png")

  def execute(self):
    # データ読込
    input_df = pd.read_csv(self.__input_data_path, encoding="cp932")
    for agg_target_col_index in self.__target_cols:
      # 結果集計
      query = '開催回 == ' + str(self.__holding_num)
      agg_df = input_df.query(query).iloc[:, [agg_target_col_index]]
      title = agg_df.columns[0]
      vc = agg_df.value_counts()
      index = [x[0] for x in  vc.index.values]

      # 5段階評価の集計結果プロット
      self.__bar_plot_5_grade_evaluation(index, vc.values, title)

class AggTopicData():
  def __init__(self, data_path, topic_col):
    self.__data_path = data_path
    self.__topic_col = topic_col
    return
  
  # 名詞抽出
  def __extract_nouns_from_parsednode(self, node):
    target_word_types = ["名詞"]
    nouns = []
    while node:
      feature_items = node.feature.split(",")
      word_type = feature_items[0]
      if word_type in target_word_types:
        nouns.append(node.surface)
      node = node.next
    return nouns

  # 形態素解析結果から名詞リスト抽出
  def __extract_nouns(self, descriptions):
    tagger = MeCab.Tagger()
    tagger.parse('')
    all_nouns = []
    for description in descriptions:
      node = tagger.parseToNode(description)
      nouns = self.__extract_nouns_from_parsednode(node)
      all_nouns = all_nouns + nouns
    return all_nouns

  # Topicの単語リストを出力
  def output_topic_list(self, q_data_df: pd.DataFrame):
    # 4列目の項目
    descriptions = q_data_df.iloc[:,self.__topic_col].dropna().values
    all_nouns = self.__extract_nouns(descriptions)
    word_df = pd.DataFrame(all_nouns, columns=["word"])
    word_df.value_counts().to_csv("./output/words.csv", index=True, header=False, encoding="cp932")
    return word_df
    
  # トピック一覧を出力
  def out_topic_list(self, input_df):
    desc_df = input_df.iloc[:,self.__topic_col].dropna()
    desc_df.to_csv("./output/topics.csv", index=True, header=False, encoding="cp932")

  # 自由記入コメント一覧を出力
  def out_free_comments_list(self, input_df):
    # 適当にやりました
    desc_df = input_df.iloc[:,self.__topic_col+3].dropna()
    desc_df.to_csv("./output/freecomments.csv", index=True, header=False, encoding="cp932")

  # バーグラフで出力 
  def plot_bar_hist_topics(self, indexes: List[int], topics: List[str]):
  	plt.figure(figsize=(30, 6))
  	plt.xticks(rotation=90)
  	title = "取り上げて欲しいトピックに書かれた単語"
  	plt.title(title, fontsize=18)
  	plt.ylabel("回数")
  	plt.xlabel("単語")
  	plt.bar(indexes, topics, color="b", alpha=0.5)
  	plt.savefig("./output/" + title + ".png")	

  def execute(self):
    # データ取得
    input_df = pd.read_csv(self.__data_path, encoding="cp932")

    # 出力
    ## リスト
    self.out_topic_list(input_df)
    self.out_free_comments_list(input_df)


    word_df = self.output_topic_list(input_df)

    ## グラフ
    vc = word_df.value_counts()
    indexes = [x[0] for x in  vc.index.values]
    value = vc.values
    self.plot_bar_hist_topics(indexes, value)
