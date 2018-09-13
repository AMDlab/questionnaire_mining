####################
# import files
####################
from gensim.models.keyedvectors import KeyedVectors
from gensim.models import word2vec
from collections import defaultdict
from sklearn.cluster import KMeans

# created module
import lib.questionnaire_mining as qm

####################
# const
####################

# directory which has target data
DIR_PATH = './resource/text_data/*'  
# learned model data 
LEARNED_MODEL_PATH = './resource/model/word2vec.gensim.model'
# madel data path 
MODEL_PATH = './tmp/word2vec.gensim.model'

# クラスター数
CLUSTER_NUM = 10            
# 解析前の文書から除外しておく言語(半角で入力)
DEFAULT_EXCEPT_KEYWORD = ['宇南山', '遠藤','剣太郎', 'ﾏﾂｳﾗ', 'A -', 'B -','A-', 'B-', '--']
# 解析前の文書から除外しておく正規表現(半角で入力)
DEFAULT_EXCEPT_REG = '\(.+@\d\d:\d\d:\d\d?\)' 
# 解析結果から除外させる単語
EXCEPT_KEYWORDS = []
# 除外する品詞1リスト
EXCEPT_MAIN_FEATURES = ['記号', '助詞', '助動詞', '感動詞', '接頭詞', '副詞', '連体詞', '接続詞']  
# 除外する品詞2リスト
EXCEPT_SUB_FEATURES = ['代名詞', '接尾','副詞可能', '自立', '非自立', '形容動詞語幹'] 
# 学習済みモデルデータに対するテストデータのバイアス
BIAS = 10

####################
# main 
####################

# reate wakachi data
mp = qm.morph.Morph(DEFAULT_EXCEPT_KEYWORD, DEFAULT_EXCEPT_REG, EXCEPT_KEYWORDS, EXCEPT_MAIN_FEATURES, EXCEPT_SUB_FEATURES)
mp.open_files(qm.util.get_file_list(DIR_PATH))
mp.extract()
mp.write_extracted_wakati(MODEL_PATH + '.txt')
sentences = word2vec.LineSentence(MODEL_PATH + '.txt')

# set learned model data
model = word2vec.Word2Vec.load(LEARNED_MODEL_PATH)

# add training data
model.build_vocab(sentences, update=True)  

# add bias for training data
for epoch in range(BIAS):
    model.train(sentences, epochs=model.epochs, total_examples=model.corpus_count)
    model.alpha -= 0.002 # decrease the learning rate
    model.min_alpha = model.alpha # fix the learning rate, no deca

# save model
model.save(MODEL_PATH)

# extract vector from trained data
vocab, vectors = qm.util.get_vectors(model, mp)

kmeans_model = KMeans(n_clusters=CLUSTER_NUM, verbose=1, random_state=42, n_jobs=-1)
kmeans_model.fit(vectors)

cluster_labels = kmeans_model.labels_
cluster_to_words = defaultdict(list)
for cluster_id, word in zip(cluster_labels, vocab):
    cluster_to_words[cluster_id].append(word)

for words in cluster_to_words.values():
    print(words)
print(mp.except_keywords)