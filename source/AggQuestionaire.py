import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import japanize_matplotlib
import MeCab

# my packages
from AggConfigurations import AggConfiguration

def bar_plot(left, right, title):
    agg_target = {}
    for idx in range(5):
        agg_target[idx+1] = 0
    
    for k, v in zip(left, right):
        agg_target[k] = v
    
    fig = plt.figure(figsize=(5, 3))
    
    plt.title(title, fontsize=18)
    plt.xlabel("評価")
    plt.ylabel("投票数")
    plt.ylim(0, max(right) + 2)
    for i in range(len(agg_target)):
        plt.text(x=i+1, y=agg_target[i+1]+1, s=agg_target[i+1], ha="center", va="top", fontsize=14)
    plt.bar(agg_target.keys(), agg_target.values(), color="b", alpha=0.5)
    plt.savefig(title + ".png")

def AggCategoricalColumns():
    for agg_target_col_index in AggConfiguration.AggTargetCols:
        query = '開催回 == ' + str(AggConfiguration.HoldingNum)
        col = excel.query(query).iloc[:, [agg_target_col_index]]
        vc = col.value_counts()
        index = [x[0] for x in  vc.index.values]
        value = vc.values
        title = col.columns[0]
    
        bar_plot(index, value, title)

# 名詞抽出
def extract_nouns_from_parsednode(node):
    nouns = []
    while node:
        feature_items = node.feature.split(",")
        word_type = feature_items[0]
        if word_type == "名詞":
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

def AggTopicCol():
    # 4列目の項目
    descriptions = excel.iloc[:,AggConfiguration.AggTopicCol].dropna().values
    all_nouns = ExtractNounsFromTopics(descriptions)
    word_df = pd.DataFrame(all_nouns, columns=["word"])
    word_df.value_counts().to_csv("desc.csv", index=True, header=False, encoding="cp932")


