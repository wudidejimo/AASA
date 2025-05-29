import struct
class SHA256:
   
    K = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
        0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
        0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
        0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
        0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
        0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
        0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
        0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
        0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ]

    
    _initial_H = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
    ]

    def __init__(self, message=b''):
        self._buffer = message

    def update(self, message):
        self._buffer += message

    def _pad(self, message):
      
        original_length = len(message) * 8
        message += b'\x80'
        
        pad_len = (56 - (len(message) % 64)) % 64
        message += b'\x00' * pad_len
        message += struct.pack('>Q', original_length)
        return message

    def digest(self):
        padded = self._pad(self._buffer)
        mask = 0xffffffff
        K = self.K  
       
        h0, h1, h2, h3, h4, h5, h6, h7 = self._initial_H

        
        for i in range(0, len(padded), 64):
            block = padded[i:i + 64]
           
            W = list(struct.unpack('>16L', block))
            W += [0] * 48

         
            for j in range(16, 64):
                w15 = W[j - 15]
               
                s0 = (((w15 >> 7) | (w15 << (32 - 7))) & mask) ^ \
                     (((w15 >> 18) | (w15 << (32 - 18))) & mask) ^ (w15 >> 3)
                w2 = W[j - 2]
                s1 = (((w2 >> 17) | (w2 << (32 - 17))) & mask) ^ \
                     (((w2 >> 19) | (w2 << (32 - 19))) & mask) ^ (w2 >> 10)
                W[j] = (W[j - 16] + s0 + W[j - 7] + s1) & mask

            a, b, c, d = h0, h1, h2, h3
            e, f, g, h = h4, h5, h6, h7

           
            for j in range(64):
                S1 = (((e >> 6) | (e << (32 - 6))) & mask) ^ \
                     (((e >> 11) | (e << (32 - 11))) & mask) ^ \
                     (((e >> 25) | (e << (32 - 25))) & mask)
                ch = (e & f) ^ ((~e) & g)
                temp1 = (h + S1 + ch + K[j] + W[j]) & mask
                S0 = (((a >> 2) | (a << (32 - 2))) & mask) ^ \
                     (((a >> 13) | (a << (32 - 13))) & mask) ^ \
                     (((a >> 22) | (a << (32 - 22))) & mask)
                maj = (a & b) ^ (a & c) ^ (b & c)
                temp2 = (S0 + maj) & mask

                h = g
                g = f
                f = e
                e = (d + temp1) & mask
                d = c
                c = b
                b = a
                a = (temp1 + temp2) & mask

          
            h0 = (h0 + a) & mask
            h1 = (h1 + b) & mask
            h2 = (h2 + c) & mask
            h3 = (h3 + d) & mask
            h4 = (h4 + e) & mask
            h5 = (h5 + f) & mask
            h6 = (h6 + g) & mask
            h7 = (h7 + h) & mask

        return struct.pack('>8L', h0, h1, h2, h3, h4, h5, h6, h7)

    def hexdigest(self):
        return ''.join(f'{byte:02x}' for byte in self.digest())

    def sha256(self, message):
        if isinstance(message, str):
            self._buffer = message.encode('utf-8')
        else:
            self._buffer = message
        return self.hexdigest()


 
