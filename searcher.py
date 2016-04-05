import struct

from docreader import DocumentStreamReader
import sys
import os
from collections import Counter, defaultdict
import re

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
        dict_file = open("dict.txt", "r")
        line = dict_file.readline()
        while line != '':
            splitted = line.strip().split(' ')
            word = splitted[0].decode("utf-8")
            word_id = int(splitted[1])
            self.word_index[word] = int(word_id)

            line = dict_file.readline()
        dict_file.close()
        print "loaded dict:", len(self.word_index)

    def load_index(self):
        index_file = open("index.txt", "r")
        line = index_file.readline()
        while line != '':
            splitted = line.strip().split(' ')
            word = int(splitted[0])
            doc_ids = map(int, splitted[1:])

            self.index[word] = doc_ids
            line = index_file.readline()
        index_file.close()
        print "loaded index:", len(self.index)
        # print self.index.keys()

    def load_urls(self):
        url_file = open("urls.txt", "r")
        line = url_file.readline()
        while line != '':
            splitted = line.strip().split(' ')
            idx = int(splitted[0])
            url = splitted[1]
            self.urls[idx] = url
            line = url_file.readline()

        url_file.close()
        print "loaded urls:", len(self.urls)


    def __init__(self):
        self.urls = {}
        self.word_index = {}
        self.index = {}
        self.load_dict()
        self.load_urls()
        self.load_index()
        print "Ready to search"
        
    def get_doc_id_set(self, word):
        if word not in self.word_index:
            return set()

        windex = self.word_index[word]
        # print windex
        # print windex in self.index
        return set(self.index[windex])


    def search(self, query):
        if query.term is not None:
            return self.get_doc_id_set(query.term)

        return self.search(query.left) & self.search(query.right)

    def get_document_list(self, query):
        docs = self.search(query)

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
