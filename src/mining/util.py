import glob

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

def lines_to_txt(clusters, lines, file_path):
    f = open(file_path + '.txt', 'w')
    f.write('--------------------------------------------------------------------\n')
    f.write('### Clusters\n\n')
    for c_i, words in enumerate(clusters):
        f.write('cluster_' + str(c_i) + ' | ' + ','.join(words))
        f.write('\n')
    f.write('--------------------------------------------------------------------\n\n\n')
    f.write('### Analyzed Sentences\n\n')
    for line in lines:
        f.write(line.line)
        f.write('\n')
        for l_i, counter in enumerate(line.counters):
            f.write('cluster_' + str(l_i) + ':' + str(counter) + ' | ' + ','.join(line.words[l_i]))
            f.write('\n')
        f.write('\n')
    f.close()