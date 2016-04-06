import struct

import math

class BitstreamWriter:
    def __init__(self):
        self.nbits  = 0
        self.curbyte = 0
        self.vbytes = []

    def add(self, x):
        self.curbyte |= x << (8-1 - (self.nbits % 8))
        self.nbits += 1

        if self.nbits % 8 == 0:
            self.vbytes.append(chr(self.curbyte))
            self.curbyte = 0

    def getbytes(self):
        if self.nbits & 7 == 0:
            return "".join(self.vbytes)

        return "".join(self.vbytes) + chr(self.curbyte)


class BitstreamReader:
    def __init__(self, blob):
        self.blob = blob
        self.pos  = 0

    def get(self):
        ibyte = self.pos / 8
        ibit  = self.pos & 7

        self.pos += 1
        return (ord(self.blob[ibyte]) & (1 << (7 - ibit))) >> (7 - ibit)

    def finished(self):
        return self.pos >= len(self.blob) * 8



class Simple9Encoder:
    name = "simple9"

    values = [28, 14, 9, 7, 5, 4, 3, 2, 1]

    def can_pack(self, xs, n):
        if len(xs) != n:
            return False

        max_log = 0
        for x in xs:
            max_log = max(max_log, math.ceil(math.log(x, 2)))

        # print max_log
        if n * max_log <= 28:
            return True

        return False

    def get_signature(self, n):
        return bin(self.values.index(n))[2:].zfill(4)

    def get_n(self, signature):
        return self.values[int(signature, 2)]

    def get_fill_len(self, n):
        return 28/n

    def encode_batch(self, xs):
        # print len(xs)
        resstr = self.get_signature(len(xs))
        fill_len = self.get_fill_len(len(xs))

        for x in xs:
            resstr += bin(x)[2:].zfill(fill_len)
            # print resstr

        while len(resstr) < 32:
            resstr += '0'

        # print resstr

        return resstr

    def write_str(self, s): 
        for c in s:
            if c == '1':
                self.writer.add(1)
            else:
                self.writer.add(0)
                  

    def encode(self, xs):

        self.writer = BitstreamWriter()
    
        while len(xs) > 0:
            for n in self.values:
                if self.can_pack(xs[:n], n):
                    break

            resstr = self.encode_batch(xs[:n])
            print resstr
            self.write_str(resstr)

            xs = xs[n:]


        return self.writer.getbytes()


            
    def decode(self, blob):
        raise ValueError()

def main():
    encoder = Simple9Encoder()
    # for it in encoder.values:
    #     print encoder.get_signature(it)
    res =  encoder.encode([1, 2, 3, 16, 19, 11])
    print map(lambda x: bin(ord(x))[2:].zfill(8), res)

    # print encoder.can_pack([1, 1, 1, 1, 1], 5)


if __name__ == "__main__":
    main()