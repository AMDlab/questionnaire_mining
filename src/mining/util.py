import glob
import numpy as np

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

def lines_to_txt(clusters, clusters_vector, lines, file_path):
    f = open(file_path + '.txt', 'w')
    f.write('--------------------------------------------------------------------\n')
    f.write('### Clusters\n\n')
    keys = list(clusters.keys())
    keys.sort()
    for key in keys:
        words = clusters[key]
        f.write('cluster_' + str(key) + ' | ' + ','.join(words))
        f.write('\n')
        f.write('cluster_' + str(key) + '_avarage_vector | ' + '[' + ','.join([str(val) for val in avarage_arr(clusters_vector[key])]) + ']')
        f.write('\n')
    f.write('--------------------------------------------------------------------\n\n\n')
    print('--------------------------------------------------------------------\n\n\n')
    f.write('### Analyzed Sentences\n\n')
    for line in lines:
        f.write(line.line)
        f.write('\n')
        f.write('avarage_vector: ' + '[' + ','.join([str(val) for val in avarage_arr(line.non_cat_vectors)]) + ']')
        f.write('\n')
        for l_i, counter in enumerate(line.counters):
            f.write('cluster_' + str(l_i) + ':' + str(counter) + ' | ' + ','.join(line.words[l_i]))
            f.write('\n')
        f.write('\n')
    f.close()

def lines_to_csv(clusters, clusters_vector, lines, file_path):
    fw = open(file_path + '_cluster_vector.csv', 'w')
    keys = list(clusters.keys())
    keys.sort()

    fw.write('cluster name, vector\n')
    for key in keys:
        words = clusters[key]
        fw.write('cluster_' + str(key) + '_avarage_vector' + ',' + ','.join([str(val) for val in avarage_arr(clusters_vector[key])]))
        fw.write('\n')
    fw.close()
    fv = open(file_path + '_cluster.csv', 'w')

    fv.write('cluster name, words\n')
    for key in keys:
        words = clusters[key]
        fv.write('cluster_' + str(key) + ',' + ','.join(words))
        fv.write('\n')
    fv.close()

    f = open(file_path + '.csv', 'w')
    f.write('cluster name,number of terms,words\n')
    for line in lines:
        f.write(line.line)
        f.write('\n')
        for l_i, counter in enumerate(line.counters):
            f.write('cluster_' + str(l_i) + ',' + str(counter) + ',' + ','.join(line.words[l_i]))
            f.write('\n')
        f.write('\n')
    f.close()

    frv = open(file_path + '_vector.csv', 'w')
    frv.write('text,vector\n')
    for line in lines:
        frv.write(line.line + ',' + ','.join([str(val) for val in avarage_arr(line.non_cat_vectors)]))
        frv.write('\n')
    f.close()


def avarage_arr(arr):
    nparr = to_numpy(arr)
    sum = np.asarray([])
    count = 0
    for i, vec in enumerate(nparr):
        if len(vec) == 0:
            continue
        if len(sum) == 0:
            sum = vec
        else:
            sum = sum + vec
        count += 1
    return (sum/count).tolist()

def to_numpy(arr):
    nparr = []
    for item in arr:
        nparr.append(np.asarray(item))
    return nparr
