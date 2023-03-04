# -*- coding: utf-8 -*-
"""Travel-Text dataset generator for Natural Language Training.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1P0ZBVu9zQ6Di8kRAA1b8X0egYY3i0x9U
"""

import pandas as pd
import numpy as np

from google.colab import drive
drive.mount('/content/drive')

fpath = 'drive/MyDrive/tripbuilder_data/'

outpath = 'drive/MyDrive/tripbuilder_data/TLD/'

"""# TLD-sentence"""

PLA001i = pd.read_json(fpath+"PLA001i/Busan_PLA001i.json")

pd.read_json(fpath+"PLA001i/Seoul_PLA001i.json")

pd.read_json(fpath+"PLA001i/Ulsan_PLA001i.json")

import re

np.shape(PLA001i)

sentencelst = []
for i in range(len(PLA001i)):
  txtlst = PLA001i[['contents']].iloc[i].tolist()[0]
  for j in txtlst:
    splited_lst = j.split('.')
    for sentence in splited_lst:
      new_stc = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", sentence)
      sentencelst.append(new_stc)

sentencelst

len(sentencelst)

!pip install -U easynmt

from easynmt import EasyNMT
model = EasyNMT('opus-mt')

sentencelst = [v for v in sentencelst if v]

len(sentencelst)

target_num = 1000000

import time

en_stc_list = model.translate(sentencelst[:target_num], target_lang='en')

out_data = pd.DataFrame({"sentence": en_stc_list})

out_data.to_json(outpath+"TLD_sentence.json")

out_data_kor = pd.DataFrame({"sentence": sentencelst})

out_data_kor.to_json(outpath+"TLD_sentence_kor.json")

"""# TLD-wv"""

from gensim.models import Word2Vec

TLD_sentence = pd.read_json(outpath+'TLD_sentence_kor.json')

data = TLD_sentence['sentence'].values.tolist()

data_use = []
for i in data[:1000000]:
  if(len(i)<=300):
    data_use.append(i)

!pip install konlpy

from konlpy.tag import Okt

okt = Okt()

import time
import datetime

from multiprocessing import Process
from multiprocessing import Pool

def morphize(data):
  morphs = []
  for i in range(len(data)):
    morphs.append(okt.morphs(data[i], norm=True, stem=True))
  print('morphize is done')
  return morphs

if __name__=="__main__":
  sentence_list = [data_use[:250000], data_use[250000:500000], data_use[500000:750000], data_use[750000:]]
  pool = Pool()
  returnv = pool.map(morphize, sentence_list)
  pool.close()
  pool.join()

returnv

morphs_data = returnv[0]+returnv[1]+returnv[2]+returnv[3]

w2v_model = Word2Vec(sentences = morphs_data, size=100, window=5, min_count = 3, workers=4, sg=1)

w2v_model.save(outpath+'model_w2v')

!pip install glove_python_binary

from glove import Corpus, Glove

corpus = Corpus() 

corpus.fit(morphs_data, window=5)
glove = Glove(no_components=100, learning_rate=0.05)

glove.fit(corpus.matrix, epochs=20, no_threads=4, verbose=True)
glove.add_dictionary(corpus.dictionary)

"""# Travel-Sentimental word extractor"""

from gensim.models import Word2Vec

w2v_model = Word2Vec.load(outpath+'model_w2v')

list(w2v_model.wv.vocab)

