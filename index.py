import struct

from docreader import DocumentStreamReader
import sys
import os
from collections import Counter, defaultdict
import re

class VarByteEncoder:
        
    def encode(self, xs):
        res = ""
        for x in xs:
            res += self.encode_one(x)
        return res

    def encode_one(self, x):
        rem = 0
        res = ""

        i = 0
        while x >= 0:
            rem = x % 128
            if i == 0:
                rem += 128
            res = struct.pack('B', rem) + res
            x /= 128
            i += 1
            if x == 0:
                break
        return res
            
    def decode(self, blob):

        res = []
        i = len(blob) - 1
        while i >= 0:
            x = 0
            cur = struct.unpack('B', blob[i])[0]
            print bin(ord(blob[i]))
            x += cur - 128
            i -= 1
            cur = struct.unpack('B', blob[i])[0]
            if cur < 128:
                d = 128
                print x
                while cur < 128:
                    x += cur * d
                    i -= 1
                    cur = struct.unpack('B', blob[i])[0]
                    
                    d *= 128
                    print x

            res.append(x)

        return list(reversed(res))



def read_docs(pathlist):
    for path in pathlist:
        for doc in DocumentStreamReader(path):
            yield (doc.url, doc.text)

word_re = re.compile(r'\w+', flags = re.UNICODE)
def get_word_list(text):
    # words = Counter()
    words = re.findall(word_re, text)
    words = map(lambda w: w.lower(), words)
    return Counter(words)


def get_words(docs):
    urls = {}
    words_in_docs = []
    total_words = Counter()
    for url, text in docs:     
        urls[len(urls)] = url
        cur_words = get_word_list(text)
        words_in_docs.append(cur_words.keys()) 
        total_words.update(cur_words)

    return urls, words_in_docs, total_words

def get_pairs(words_in_docs, total_words):
    word_to_idx = {}
    idx_to_word = {}

    for idx, word in enumerate(total_words.keys()):
        idx_to_word[idx] = word
        word_to_idx[word] = idx

    pairs = []
    for doc_id, words in enumerate(words_in_docs):
        for word in words:
            pairs.append((word_to_idx[word], doc_id))

    return word_to_idx, idx_to_word, pairs


def build_index(pairs):
    index_file = open("index.txt", "w")
    pairs = sorted(pairs)

    # prev = None
    word_index = defaultdict(lambda: [])
    for pair in pairs:
        word = pair[0]
        doc_id = pair[1]
        # if word != prev and prev is not None:
            # index_file.write(str(index.iteritems()))
            # word_index = defaultdict(lambda: [])
        word_index[word].append(doc_id)
        # prev = word

    # index_file.write(str(index.iteritems()))

    for word, doc_ids in word_index.iteritems():
        index_file.write("{0} ".format(word))
        for doc_id in sorted(doc_ids):
            index_file.write("{0} ".format(doc_id))
        index_file.write("\n")
    index_file.close()



def build_dict(docs):
    idx_to_urls, words_in_docs, total_words = get_words(docs)
    word_to_idx, idx_to_word, pairs = get_pairs(words_in_docs, total_words)
    build_index(pairs)


    dict_file = open("dict.txt", "w")
    for word, idx in word_to_idx.iteritems():
            dict_file.write(u"{0} {1}\n".format(word, idx).encode("utf-8"))
    dict_file.close()


    urls_file = open("urls.txt", "w")
    for idx, url in idx_to_urls.iteritems():
            urls_file.write(u"{0} {1}\n".format(idx, url).encode("utf-8"))
    urls_file.close()

    
def main():
    build_dict(read_docs(sys.argv[1:]))


if __name__ == '__main__':
    main()




