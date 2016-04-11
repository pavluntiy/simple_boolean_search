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
            cur_log = math.ceil(math.log(x, 2)) if x != 0 else 1
            max_log = max(max_log, cur_log)

        # print max_log
        if n * max_log <= 28:
            return True

        return False

    # def get_signature(self, n):
    #     return bin(self.values.index(n))[2:].zfill(4)

    # def get_n(self, signature):
    #     return self.values[int(signature, 2)]

    # def get_fill_len(self, n):
    #     return 28/n

    def encode_batch(self, xs):
        # print len(xs)
        # resstr = bin(self.values.index(len(xs)))[2:].zfill(4)
        self.write_str(bin(self.values.index(len(xs)))[2:].zfill(4))
        fill_len = 28/(len(xs))


        counter = 4
        for x in xs:
            # resstr += bin(x)[2:].zfill(fill_len)
            tmp = bin(x)[2:].zfill(fill_len)
            self.write_str(tmp)
            counter += len(tmp)
            # for b in bin(x)[2:].zfill(fill_len):
            #     if b == "1":
            #         self.writer.add(1)
            #     else:
            #         self.writer.add(0)
            #     counter += 1
            # print resstr

        while counter < 32:
            self.writer.add(0)
            counter += 1

        # print resstr

        # return resstr

    def write_str(self, s): 
        for c in s:
            if c == '1':
                self.writer.add(1)
            else:
                self.writer.add(0)
                  

    def encode(self, xs):

        self.writer = BitstreamWriter()
    
        while len(xs) > 0:
            # acc = 0
            # cur = 0
            # n = 1
            # for i in range(1, 28 + 1):
                # if 
            for n in self.values:
                # for 

                if self.can_pack(xs[:n], n):
                    break

            resstr = self.encode_batch(xs[:n])
            # print resstr
            # self.write_str(resstr)

            xs = xs[n:]


        return self.writer.getbytes()

    def read_str(self):


        res_str = ""

        i = 0
        while i < 32:  #and not self.reader.finished(): wrong number of bits indicates an error
            cur_bit = self.reader.get()
            if cur_bit == 1:
                res_str += '1'
            else:
                res_str += '0'
            i += 1

        return res_str

    def decode_batch(self, res_str):
        res_list = []
        n = self.values[int(res_str[:4], 2)]
        res_str = res_str[4:]

        num_len = 28/n
        i = 0
        while i + num_len <= 28:
            cur = res_str[i:i + num_len]
            # print cur
            i += num_len
            res_list.append(int(cur, 2))
        # print res_list
        return res_list

        
            
    def decode(self, blob):
        self.reader = BitstreamReader(blob)

        res_list = []

        while not self.reader.finished():
            cur_str = self.read_str()
            # print cur_str
            res_list += self.decode_batch(cur_str)
            # print "====="

        return res_list




        

def main():
    encoder = Simple9Encoder()
    # for it in encoder.values:
    #     print encoder.get_signature(it)
    for i in range(1, 100 * 100 * 100):
        res = encoder.encode([111, 12])
    # res =  encoder.encode([1, 2, 3, 16, 19, 11, 23422, 143, 19, 81])
        res =  encoder.encode([0, 0, 11, 12, 123481234, 234234, 2322222, 1111, 11, 12, 13, 14, 1523, 234123412, 11, 0, 1, 2, 3])
    # print map(lambda x: bin(ord(x))[2:].zfill(8), res)
        encoder.decode(res)

    # print encoder.can_pack([1, 1, 1, 1, 1], 5)


if __name__ == "__main__":
    import cProfile
    cProfile.run("main()")