class Line(object):
    def __init__(self, line, cluster_number):
        self.line = line
        self.counters = []
        self.words = []
        self.vectors = []
        self.non_cat_vectors = []
        for _i in range(0, cluster_number):
            self.counters.append(0)
            self.words.append([])
            self.vectors.append([])

    def set_word(self, index, word, vector):
        self.counters[index] += 1
        if not word in self.words[index]:
            self.words[index].append(word)
            self.vectors[index].append(vector)
            self.non_cat_vectors.append(vector)


