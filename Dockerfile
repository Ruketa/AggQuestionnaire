FROM jupyter/datascience-notebook

USER root

RUN apt-get update \
  && apt-get install -y mecab \
  && apt-get install -y libmecab-dev \
  && apt-get install -y mecab-ipadic-utf8

WORKDIR /home/work

ADD requirements.txt /home/work

# パッケージのインストール
RUN pip install -r requirements.txt
