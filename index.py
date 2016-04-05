import struct


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

class VarByteEncoder:
    # def __init__(self):
        
        


    def encode(self, xs):
        # self.writer = BitstreamWriter()
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
            # print cur
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

            # else:
            #     i -= 1
            res.append(x)
        # self.reader = BitstreamReader(blob)
        # res = ""
        # while not self.reader.finished():
        #     b = self.reader()
        #     if b:
        #         res += "1"
        #     else:
        #         res += "0"

        # return self.decode_string(res)
        # print res
        return list(reversed(res))

a = VarByteEncoder()
t  = a.encode([2, 3, 2, 191, 0, 500000000000, 128, 0])
print map(lambda x: bin(ord(x)), t)
print a.decode(t)
