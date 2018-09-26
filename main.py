####################
# import files
####################
from collections import defaultdict
from sklearn.cluster import KMeans
from lib.gensim.models.keyedvectors import KeyedVectors
from lib.gensim.models import word2vec
import src.mining as qm
import yaml

# created module

####################
# const
####################
yf = open("setting.yml", "r+")
data = yaml.load(yf)

DIR_PATH = data['dir_path']
LEARNED_MODEL_PATH = data['learned_model_path']
MODEL_PATH = data['model_path']
OUTPUT_PATH = data['output_path']
CLUSTER_NUM = data['cluster_num']
DEFAULT_EXCEPT_KEYWORD = data['default_except_keyword']
DEFAULT_EXCEPT_REG = data['default_except_reg']
EXCEPT_KEYWORDS = data['except_keywords']
EXCEPT_MAIN_FEATURES = data['except_main_features']
EXCEPT_SUB_FEATURES = data['except_sub_features']
BIAS = data['bias']

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
cluster_to_vectors = defaultdict(list)
for cluster_id, word, vector in zip(cluster_labels, vocab, vectors):
    cluster_to_words[cluster_id].append(word)
    cluster_to_vectors[cluster_id].append(vector)

lines = []
for s_i, sen in enumerate(sentences):
    line = qm.line.Line(''.join(sen), CLUSTER_NUM)
    for cluster_key in cluster_to_words.keys():
        for w_i, word in enumerate(cluster_to_words[cluster_key]):
            if word in sen:
                line.set_word(cluster_key, word, cluster_to_vectors[cluster_key][w_i])
    lines.append(line)

qm.util.lines_to_txt(cluster_to_words, cluster_to_vectors, lines, OUTPUT_PATH)
qm.util.lines_to_csv(cluster_to_words, cluster_to_vectors, lines, OUTPUT_PATH)