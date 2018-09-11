import sys
import traceback
import glob
import MeCab
from gensim.models.keyedvectors import KeyedVectors
from gensim.models import word2vec
from collections import defaultdict
from sklearn.cluster import KMeans
# import CaboCha
# from cabocha.analyzer import CaboChaAnalyzer

DIR_PATH = './text_data/*'  # 解析するテキストデータが保存されているディレクトリ
MODEL_PATH = './tmp/word2vec.gensim.model'
MAX_VOCAB = 30000           # 単語制限数 : メモリ消費量に応じて変更する
CLUSTER_NUM = 10       # クラスタ数
EXCEPT_KEYWORDS = []        # 除外する単語リスト
EXCEPT_FEATURES = []        # 除外する品詞リスト

def get_file_list(dir_path):
    return glob.glob(dir_path)

def get_keyword_data(dir_path):
    keywords = []
    mp = Morph()
    for _idx, file_path in enumerate(get_file_list(dir_path)):
        mp.open_file(file_path)

    return '\n'.join(keywords)

class Morph(object):
    lines = []
    extracted = []
    kinds = None

    def __init__(self,except_keywords = [], except_features = []):
        self.chasen = MeCab.Tagger('-Ochasen -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/')
        self.wakati = MeCab.Tagger('-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/')
        self.except_k = except_keywords
        self.except_f = except_features

    def open_files(self, file_paths):
        for _fi, file_path in enumerate(file_paths):
            self.open_file(file_path)
        return self

    def open_file(self, file_path):
        # f = open(file_path, 'r', 'utf-8', 'ignore')
        f = open(file_path)
        self.set_sentence(f.read())
        f.close
        return self

    def set_sentence(self, sentence):
        self.lines += sentence.split('\n')[:-1]
        return self

    def clear_sentence(self):
        self.lines.clear()
        return self

    def get_chunks(self, s):
        raw = self.get_chasen(s)
        return raw.splitlines()[:-1]

    def get_chasen(self, s):
        return self.chasen.parse(s)

    def get_wakati(self, s):
        return self.wakati.parse(s)

    def get_extracted_wakati(self):
        return ' '.join(self.get_surface())

    def write_extracted_wakati(self, file_path):
        f = open(file_path, 'w') 
        f.write(self.get_extracted_wakati())
        f.close() 
        return self

    def get_surface_as_line(self):
        for chunks in self.extracted:
            yield chunks['surface']

    def get_surface(self):
        for chunks in self.extracted:
            if chunks['origin'] is not None:
                yield chunks['surface']

    def get_yomi(self):
        for chunks in self.extracted:
            if chunks['origin'] is not None:
                yield chunks['yomi']

    def get_origin(self):
        for chunks in self.extracted:
            if chunks['origin'] is not None:
                yield chunks['origin']

    def get_feature(self):
        for chunks in self.extracted:
            if chunks['origin'] is not None:
                yield chunks['feature']

    def extract(self):
        self.extracted = self.__extract()
        return self

    def __extract(self):
        for _li, line in enumerate(self.lines):
            chunks = self.get_chunks(line.strip())
            for _ci, chunk in enumerate(chunks):
                try:
                    surface, yomi, origin, feature = chunk.split('\t')[:4]
                except:
                    traceback.print_exc()
                    continue
                yield  {'surface': surface, 'yomi': yomi, 'origin': origin.lower(), 'feature': feature}
            yield {'surface': '\n', 'yomi': None, 'origin': None, 'feature': None}


mp = Morph()
mp.open_files(get_file_list(DIR_PATH))
mp.extract()
mp.write_extracted_wakati(MODEL_PATH)

sentences = word2vec.LineSentence(MODEL_PATH)
model = word2vec.Word2Vec(sentences,
                          sg=1,
                          size=200,
                          min_count=5,
                          window=10,
                          hs=1,
                          negative=0)
model.save(MODEL_PATH)

model = KeyedVectors.load(MODEL_PATH)
vocab = list(model.wv.vocab.keys())[:MAX_VOCAB]
vectors = [model.wv[word] for word in vocab]

kmeans_model = KMeans(n_clusters=CLUSTER_NUM, verbose=1, random_state=42, n_jobs=-1)
kmeans_model.fit(vectors)

cluster_labels = kmeans_model.labels_
cluster_to_words = defaultdict(list)
for cluster_id, word in zip(cluster_labels, vocab):
    cluster_to_words[cluster_id].append(word)

for words in cluster_to_words.values():
    print(words[:10])


# model   = word2vec.Word2Vec.load('matsui_data.model')
# results = model.wv.most_similar(positive=[u'人生'],negative=[], topn=10)
# pd.DataFrame(results,columns=('ワード','関連度'))