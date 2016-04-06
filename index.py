import struct

from docreader import DocumentStreamReader
import sys
import os
from collections import Counter, defaultdict
import re

from varbyteencoder import VarByteEncoder
from simple9encoder import Simple9Encoder



class Indexer:

    def __init__(self, encoder_class):
        self.encoder = encoder_class()

    def read_docs(self, pathlist):
        for path in pathlist:
            for doc in DocumentStreamReader(path):
                yield (doc.url, doc.text)

    word_re = re.compile(r'\w+', flags = re.UNICODE)
    def get_word_list(self, text):
        words = re.findall(self.word_re, text)
        words = map(lambda w: w.lower(), words)
        return Counter(words)


    def get_words(self, docs):
        urls = {}
        words_in_docs = []
        self.total_words = Counter()
        for url, text in docs:     
            urls[len(urls)] = url
            cur_words = self.get_word_list(text)
            words_in_docs.append(cur_words.keys()) 
            self.total_words.update(cur_words)

        urls_file = open("./data/urls.txt", "w")
        for idx, url in urls.iteritems():
                urls_file.write(u"{0} {1}\n".format(idx, url).encode("utf-8"))
        urls_file.close()

        self.words_in_docs = words_in_docs 

    def get_pairs(self):
        self.word_to_idx = {}
        self.idx_to_word = {}

        for idx, word in enumerate(self.total_words.keys()):
            self.idx_to_word[idx] = word
            self.word_to_idx[word] = idx

        tmp = []
        os.system("mkdir little")
        cnt = 0

        for doc_id, words in enumerate(self.words_in_docs):
            for word in words:
                if cnt % 1000000 == 0:
                    if cnt != 0:
                        tmp = sorted(tmp)
                        for it in tmp:
                            little.write("{0} {1}\n".format(it[0], it[1]))
                        del tmp
                        tmp = []
                        little.close()
                    little = open("./little/little_{0}.csv".format(cnt), "w")

                tmp.append((self.word_to_idx[word], doc_id))
                cnt += 1

        if tmp != []:
            tmp = sorted(tmp)
            for it in tmp:
                little.write("{0} {1}\n".format(it[0], it[1]))
            del tmp
            little.close()
                    

        os.system(" sort -m -k1,1n -k2,2n --buffer-size=1500000 --temporary-directory=./tmp --parallel=16 -o ./data/pairs.txt ./little/little_*.csv")

        os.system("rm -rf little")

        # return pairs


    def build_index(self, pairs):
        index_file = open("./data/index.txt", "w")
        # pairs = sorted(pairs)

        word_index = defaultdict(lambda: [])
        pair_file = open("data/pairs.txt", "r")
        
        line = pair_file.readline()
        prev = None
        while line != "":

            
            word, doc_id = map(int, line.split(' '))
            # doc_id = pair[1]
            # if prev is not None and prev != word:
            word_index[word].append(doc_id)

            prev = word
            line = pair_file.readline()


        # for pair in pairs:
        #     word = pair[0]
        #     doc_id = pair[1]
        #     word_index[word].append(doc_id)

        new_word_ids = {}

        _lens = {}
        # 
        for word, doc_ids in word_index.iteritems():
            new_word_ids[word] = index_file.tell()
            index_file.write(self.encoder.encode(sorted(doc_ids)))
            _lens[word] = index_file.tell() - new_word_ids[word]

        index_file.close()

        lens = {}
        for word in self.word_to_idx:
            word_id = self.word_to_idx[word]
            new_word_id = new_word_ids[word_id]
            lens[new_word_id] = _lens[word_id]
            self.word_to_idx[word] = new_word_id



        dict_file = open("./data/dict.txt", "w")
        dict_file.write("{0}\n".format(self.encoder.name))
        for word, idx in self.word_to_idx.iteritems():
                dict_file.write(u"{0} {1} {2}\n".format(word, idx, lens[self.word_to_idx[word]]).encode("utf-8"))
        dict_file.close()

        return new_word_ids, word_index



    def build_dict(self, docs):
        self.get_words(docs)
        pairs = self.get_pairs()
        self.build_index(pairs)



    
def main():
    os.system("mkdir tmp")
    os.system("mkdir data")
    if sys.argv[1] == "varbyte":
        encoder_class = VarByteEncoder
    else:
        encoder_class = Simple9Encoder
    indexer = Indexer(encoder_class)
    indexer.build_dict(indexer.read_docs(sys.argv[2:]))
    os.system("rm -rf tmp")


if __name__ == '__main__':
    main()




