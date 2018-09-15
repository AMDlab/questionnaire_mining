import MeCab
import re
import mojimoji


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
        self.lines += sentence.replace('。', '。\n').split('\n')[:-1]
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
                        # if surface == 'めちゃめちゃ':
                        #     print(chunk)
                        yield {'surface': surface, 'yomi': yomi, 'origin': origin.lower(), 'feature': feature}
                yield {'surface': '\n', 'yomi': None, 'origin': None, 'feature': None}