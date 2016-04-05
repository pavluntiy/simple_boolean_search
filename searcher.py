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
            self.term = text.strip()
            print self.term



class Searcher:

    def load_dict(self):
        dict_file = open("dict.txt", "r")
        line = dict_file.readline()
        while line != '':
            splitted = line.strip().split(' ')
            word = splitted[0]
            word_id = int(splitted[1])
            self.word_index[word] = word_id

            line = dict_file.readline()
        dict_file.close()
        print "loaded dict:", len(self.word_index)

    def load_index(self):
        index_file = open("index.txt", "r")
        line = index_file.readline()
        while line != '':
            splitted = line.strip().split(' ')
            word = splitted[0]
            doc_ids = map(int, splitted[1:])

            self.index[word] = doc_ids
            line = index_file.readline()
        index_file.close()
        print "loaded index:", len(self.index)

    def load_urls(self):
        url_file = open("urls.txt", "r")
        line = url_file.readline()
        while line != '':
            splitted = line.strip().split(' ')
            idx = splitted[0]
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
        
        

    def search(self, query):
        # if query is None:
        return self.search(query.left) & self.search(query.right)

    def get_document_list(self, query):
        pass



def main():
    searcher = Searcher()

    query = sys.stdin.readline()
    while query != '':        
        # print query
        query = Query(query)
        query = sys.stdin.readline()

if __name__ == '__main__':
    main()
