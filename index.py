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
    return Counter(words).keys()

def build_dict(docs):
    urls = {}
    words = defaultdict(lambda: [])
    for url, text in docs:     
        urls[len(urls)] = url
        words = get_word_list(text) 
        
        for word in words:
            print word
        break


def main():
    build_dict(read_docs(sys.argv[1:]))


if __name__ == '__main__':
    main()




