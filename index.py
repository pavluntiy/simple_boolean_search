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

def build_dict(docs):
    urls = {}
    words_in_docs = []
    total_words = Counter()
    for url, text in docs:     
        urls[len(urls)] = url
        cur_words = get_word_list(text)
        words_in_docs.append(cur_words.keys()) 
        total_words.update(cur_words)
        
    
    word_to_idx = {}
    idx_to_word = {}

    for idx, word in enumerate(total_words.keys()):
        idx_to_word[idx] = word
        word_to_idx[word] = idx

    pairs = []
    for doc_id, words in enumerate(words_in_docs):
        for word in words:
            pairs.append((word_to_idx[word], doc_id))


    # print len(pairs)



def main():
    build_dict(read_docs(sys.argv[1:]))


if __name__ == '__main__':
    main()




