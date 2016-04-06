import struct

from docreader import DocumentStreamReader
import sys
import os
from collections import Counter, defaultdict
import re
from varbyteencoder import VarByteEncoder


class Query:
    def __init__(self, text):
        split_idx = text.rfind('&')
        self.term = None
        self.left = None
        self.right = None
        # print split_idx
        if split_idx != -1:
            text_l = text[:split_idx]
            text_r = text[split_idx + 1:]
            # print text_l
            # print text_r
            self.left = Query(text_l)
            self.right = Query(text_r)
        else:
            self.term = text.decode("utf-8").strip().lower()



class Searcher:

    def load_dict(self):
        dict_file = open("./data/dict.txt", "r")
        line = dict_file.readline()
        if line.strip() == "varbyte":
            self.encoder = VarByteEncoder()
        
        line = dict_file.readline()
        self.doc_id_count = {}
        while line != '':
            splitted = line.strip().split(' ')
            word = splitted[0].decode("utf-8")
            word_id = int(splitted[1])
            self.word_index[word] = int(word_id)

            # print word_id

            self.doc_id_count[word_id] = int(splitted[2])

            line = dict_file.readline()
        dict_file.close()

        # print "loaded dict:", len(self.word_index)
        # print max(self.doc_id_count)

    # def load_index(self):

    #     encoder = VarByteEncoder()

    #     index_file = open("./data/index.txt", "r")
    #     word = index_file.tell()
    #     byte_cnt = self.doc_id_count[word]
    #     # line = index_file.readline()
    #     blob  = index_file.read(byte_cnt)
    #     # print byte_cnt
    #     # print word

    #     while blob != '':
    #         # print map(lambda x: bin(ord(x)), blob)
    #         # splitted = line.strip().split(' ')
    #         # word = int(splitted[0)
    #         # print word
    #         # doc_ids = map(int, splitted[1:])
    #         doc_ids = encoder.decode(blob)


    #         self.index[word] = doc_ids
    #         word = index_file.tell()
    #         if word not in self.doc_id_count:
    #             break
    #         byte_cnt = self.doc_id_count[word]
    #         # print word
    #         blob  = index_file.read(byte_cnt)
    #         # print byte_cnt
    #         # line = index_file.readline()
    #     index_file.close()

        # print "loaded index:", len(self.index)
        # print self.index.keys()
        # print self.index

    def read_index_entry(self, word):
        if word not in self.index:
            byte_cnt = self.doc_id_count[word]
            self.index_file.seek(word)
            blob  = self.index_file.read(byte_cnt)
            doc_ids = self.encoder.decode(blob)
            self.index[word] = doc_ids

    def load_urls(self):
        url_file = open("./data/urls.txt", "r")
        line = url_file.readline()
        while line != '':
            splitted = line.strip().split(' ')
            idx = int(splitted[0])
            url = splitted[1]
            self.urls[idx] = url
            line = url_file.readline()

        url_file.close()
        # print "loaded urls:", len(self.urls)


    def __init__(self):
        self.urls = {}
        self.word_index = {}
        self.index = {}
        self.load_dict()
        self.load_urls()
        # self.load_index()
        self.index_file = open("./data/index.txt", "r")
        self.encoder = VarByteEncoder()
        # print "Ready to search"
        
    def get_doc_id_set(self, word):
        if word not in self.word_index:
            return set()
        windex = self.word_index[word]
        self.read_index_entry(windex)
        

        
        # print windex
        # print windex in self.index
        # print self.index[windex]
        return set(self.index[windex])


    def search(self, query):

        if query.term is not None:
            return self.get_doc_id_set(query.term)

        return self.search(query.left) & self.search(query.right)

    def get_document_list(self, query):
        docs = self.search(query)
        docs = sorted(docs)
        # print docs

        return [self.urls[it] for it in docs]



def main():
    searcher = Searcher()

    query_text = sys.stdin.readline()
    while query_text != '':        
        # print query
        query = Query(query_text)
        res = searcher.get_document_list(query)

        print query_text.strip()
        print len(res)
        for url in res:
            print url
        query_text = sys.stdin.readline()


if __name__ == '__main__':
    main()
