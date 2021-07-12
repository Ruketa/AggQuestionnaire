import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import japanize_matplotlib
import Configurations as configs
import MeCab

def bar_plot_5_grade_evaluation(left, right, title):
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

def bar_plot_vc(vc, title):
  index = [x[0] for x in  vc.index.values]
  bar_plot(index, vc.values, title)

def AggCategoricalColumns(q_data_df):
  for agg_target_col_index in configs.AggConfiguration.AggTargetCols:
    query = '開催回 == ' + str(configs.AggConfiguration.HoldingNum)
    col = q_data_df.query(query).iloc[:, [agg_target_col_index]]
    bar_plot_vc(col.value_counts(), col.columns[0])

def aggrigate():
  input_df = pd.read_csv(configs.AggConfiguration.DataPath, encoding="cp932")
  for agg_target_col_index in configs.AggConfiguration.AggTargetCols:
    query = '開催回 == ' + str(configs.AggConfiguration.HoldingNum)
    col = input_df.query(query).iloc[:, [agg_target_col_index]]
    title = col.columns[0]
    bar_plot_vc(col.value_counts(), title)


# 名詞抽出
def extract_nouns_from_parsednode(node):
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
def ExtractNounsFromTopics(descriptions):
  tagger = MeCab.Tagger()
  tagger.parse('')
  all_nouns = []
  for description in descriptions:
    node = tagger.parseToNode(description)
    nouns = extract_nouns_from_parsednode(node)
    all_nouns = all_nouns + nouns
  return all_nouns

def AggTopicCol(q_data_df):
  # 4列目の項目
  descriptions = q_data_df.iloc[:,configs.AggConfiguration.AggTopicCol].dropna().values
  all_nouns = ExtractNounsFromTopics(descriptions)
  word_df = pd.DataFrame(all_nouns, columns=["word"])
  word_df.value_counts().to_csv("./output/words.csv", index=True, header=False, encoding="cp932")
  return word_df

def aggrigateTopic():
	input_df = pd.read_csv(configs.AggConfiguration.DataPath, encoding="cp932")
	word_df = AggTopicCol(input_df)
	vc = word_df.value_counts()
	indexs = [x[0] for x in  vc.index.values]
	value = vc.values
	plt.figure(figsize=(30, 6))
	plt.xticks(rotation=90)
	title = "取り上げて欲しいトピックに書かれた単語"
	plt.title(title, fontsize=18)
	plt.ylabel("回数")
	plt.xlabel("単語")
	plt.bar(indexs, value, color="b", alpha=0.5)
	plt.savefig("./output/" + title + ".png")	

if __name__ == "__main__":
	preprocess()

	aggrigate()

	aggrigateTopic()
