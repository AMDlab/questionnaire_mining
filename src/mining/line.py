class Line(object):
    def __init__(self, line, cluster_number):
        self.line = line
        self.counters = []
        self.words = []
        for _i in range(0, cluster_number):
            self.counters.append(0)
            self.words.append([])

    def set_word(self, index, word):
        self.counters[index] += 1
        if not word in self.words[index]:
            self.words[index].append(word)