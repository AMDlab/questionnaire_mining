import sys
import re
import traceback
import glob
import mojimoji
import MeCab
from gensim.models.keyedvectors import KeyedVectors
from gensim.models import word2vec
from collections import defaultdict
from sklearn.cluster import KMeans
# import CaboCha
# from cabocha.analyzer import CaboChaAnalyzer

DIR_PATH = './text_data/*'  # 解析するテキストデータが保存されているディレクトリ
LEARNED_MODEL_PATH = './model/word2vec.gensim.model'
MODEL_PATH = './tmp/word2vec.gensim.model'
MAX_VOCAB = 30000           # 単語制限数 : メモリ消費量に応じて変更する
CLUSTER_NUM = 10            # クラスタ数
DEFAULT_EXCEPT_KEYWORD = ['宇南山', '遠藤','剣太郎', 'ﾏﾂｳﾗ', 'A -', 'B -','A-', 'B-', '--'] # 解析前の文書から除外しておく言語(半角で入力)
DEFAULT_EXCEPT_REG = '\(.+@\d\d:\d\d:\d\d?\)' # 解析前の文書から除外しておく正規表現(半角で入力)
EXCEPT_KEYWORDS = []        # 解析結果から除外させる単語
EXCEPT_MAIN_FEATURES = ['記号', '助詞', '助動詞', '感動詞', '接頭詞', '副詞', '連体詞', '接続詞']  # 除外する品詞1リスト
EXCEPT_SUB_FEATURES = ['代名詞', '接尾','副詞可能', '自立', '非自立']  # 除外する品詞2リスト


def get_file_list(dir_path):
    return glob.glob(dir_path)

def get_keyword_data(dir_path):
    keywords = []
    mp = Morph()
    for _idx, file_path in enumerate(get_file_list(dir_path)):
        mp.open_file(file_path)
    return '\n'.join(keywords)

def get_vectors(model, morph):
    keywords = list(model.wv.vocab.keys())
    vocab = []
    vectors = []
    for word in keywords:
        if word in morph.keywords and not word in morph.except_keywords:
            vocab.append(word)
            vectors.append(model.wv[word])
    return vocab, vectors

class Morph(object):
    lines = []
    extracted = []
    kinds = None

    def __init__(self, default_except_keyword = [], default_except_reg = '', except_keywords=[], except_main_features=[], except_sub_features=[]):
        self.chasen = MeCab.Tagger(
            '-Ochasen -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/')
        self.wakati = MeCab.Tagger(
            '-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/')
        self.default_except_keyword = default_except_keyword
        self.default_except_reg = default_except_reg
        self.except_keywords = except_keywords
        self.except_main_features = except_main_features
        self.except_sub_features = except_sub_features
        self.keywords = []

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
        return ' '.join(self.get_surface_as_line())

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
            if line:
                processed = re.sub('(' + '|'.join(self.default_except_keyword) + ')|', '', mojimoji.zen_to_han(line.strip()))
                processed = re.sub(self.default_except_reg, '', processed)
                chunks = self.get_chunks(processed.strip())
                for _ci, chunk in enumerate(chunks):
                    try:
                        surface, yomi, origin, feature = chunk.split('\t')[:4]
                    except:
                        traceback.print_exc()
                        continue
                    if surface != '\ufeff':
                        if not surface in self.except_keywords:
                            split = feature.split('-')
                            if len(split) == 1:
                                if split[0] in self.except_main_features:
                                    self.except_keywords.append(surface)
                            elif len(split) > 1:
                                if split[0] in self.except_main_features or split[1] in self.except_sub_features:
                                    self.except_keywords.append(surface)
                        if not surface in self.keywords:
                            self.keywords.append(surface)
                        if surface == 'そうだ':
                            print(chunk)
                        yield {'surface': surface, 'yomi': yomi, 'origin': origin.lower(), 'feature': feature}
                yield {'surface': '\n', 'yomi': None, 'origin': None, 'feature': None}


# create wakachi data
mp = Morph(DEFAULT_EXCEPT_KEYWORD, DEFAULT_EXCEPT_REG, EXCEPT_KEYWORDS, EXCEPT_MAIN_FEATURES, EXCEPT_SUB_FEATURES)
mp.open_files(get_file_list(DIR_PATH))
mp.extract()
mp.write_extracted_wakati(MODEL_PATH + '.txt')
sentences = word2vec.LineSentence(MODEL_PATH + '.txt')

# set learned model data
model = word2vec.Word2Vec.load(LEARNED_MODEL_PATH)

# add training data
model.build_vocab(sentences, update=True) # 単語リストのアップデート
model.train(sentences, epochs=model.epochs, total_examples=model.corpus_count)



model.save(MODEL_PATH)

# extract vector from trained data
vocab, vectors = get_vectors(model, mp)

kmeans_model = KMeans(n_clusters=CLUSTER_NUM, verbose=1, random_state=42, n_jobs=-1)
kmeans_model.fit(vectors)

cluster_labels = kmeans_model.labels_
cluster_to_words = defaultdict(list)
for cluster_id, word in zip(cluster_labels, vocab):
    cluster_to_words[cluster_id].append(word)

for words in cluster_to_words.values():
    print(words)
print(mp.except_keywords)

# model   = word2vec.Word2Vec.load('matsui_data.model')
# results = model.wv.most_similar(positive=[u'人生'],negative=[], topn=10)
# pd.DataFrame(results,columns=('ワード','関連度'))
