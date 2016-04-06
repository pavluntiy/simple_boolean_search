import struct
class VarByteEncoder:
    name = "varbyte"
        
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
            # print bin(ord(blob[i]))
            x += cur - 128
            i -= 1
            cur = struct.unpack('B', blob[i])[0]
            if cur < 128:
                d = 128
                # print x
                while cur < 128:
                    x += cur * d
                    i -= 1
                    cur = struct.unpack('B', blob[i])[0]
                    
                    d *= 128
                    # print x

            res.append(x)

        return list(reversed(res))