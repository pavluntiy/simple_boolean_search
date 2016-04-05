import struct

from docreader import DocumentStreamReader
import sys
import os
from collections import Counter, defaultdict
import re

from varbyteencoder import VarByteEncoder



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


def build_index(pairs, word_to_idx):
    index_file = open("./data/index.txt", "w")
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
    new_word_ids = {}

    lens = {}
    varbyte = VarByteEncoder()
    for word, doc_ids in word_index.iteritems():
        # index_file.write("{0} ".format(word))

        new_word_ids[word] = index_file.tell()
        index_file.write(varbyte.encode(sorted(doc_ids)))
        lens[word] = index_file.tell() - new_word_ids[word]
        # print new_word_ids[word]
        # for doc_id in sorted(doc_ids):
        #     index_file.write("{0} ".format(doc_id))
        # index_file.write("\n")
    index_file.close()

    # print lens

    dict_file = open("./data/dict.txt", "w")
    for word, idx in word_to_idx.iteritems():
            print lens[word_to_idx[word]]
            dict_file.write(u"{0} {1} {2}\n".format(word, idx, lens[word_to_idx[word]]).encode("utf-8"))
    dict_file.close()

    return new_word_ids, word_index



def build_dict(docs):
    idx_to_urls, words_in_docs, total_words = get_words(docs)
    word_to_idx, idx_to_word, pairs = get_pairs(words_in_docs, total_words)
    new_word_ids, word_index = build_index(pairs, word_to_idx)

    for word in word_to_idx:
        word_to_idx[word] = new_word_ids[word_to_idx[word]]




    urls_file = open("./data/urls.txt", "w")
    for idx, url in idx_to_urls.iteritems():
            urls_file.write(u"{0} {1}\n".format(idx, url).encode("utf-8"))
    urls_file.close()

    
def main():
    os.system("mkdir tmp")
    os.system("mkdir data")
    build_dict(read_docs(sys.argv[2:]))
    os.system("rm -rf tmp")


if __name__ == '__main__':
    main()




