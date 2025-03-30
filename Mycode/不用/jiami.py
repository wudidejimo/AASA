import random
from gmpy2 import invert, isqrt, gcd

class SimpleScheme():
    
    def __init__(self):
        while True:
            self.q = random.randint(1 << 128, (1 << 129) - 1)
            self.f = random.randint(1, int(isqrt(self.q // 2)))
            self.g = random.randint(int(isqrt(self.q // 4)), int(isqrt(self.q // 2)))

            if gcd(self.f, self.q * self.g) == 1:
                break
        
        self.h = invert(self.f, self.q) * self.g % self.q
        
        print(f'pk = (q, h) = ({self.q}, {self.h})')
        print(f'sk = (f, g) = ({self.f}, {self.g})')
    
    def enc(self, m):
        assert m < isqrt(self.q // 4)
        
        r = random.randint(1, int(isqrt(self.q // 2)))
        e = (r * self.h + m) % self.q
        
        print(f'rg+mf = {r * self.g + m * self.f}')
        
        print(f'e = {r * self.h % self.q} + {m} = {e}')
        
        return int(e)

    def dec(self, e):
        a = self.f * e % self.q
        
        print(f'a = {a}')
        
        b = invert(self.f, self.g) * a % self.g
        
        print(f'b = {b}')

worker = SimpleScheme()
c = worker.enc(114514)
worker.dec(c)



# pk = (q, h) = (514230918051282920692602780404498492433, 115647624614577988455515336107635422730)
# sk = (f, g) = (2405709868378346209, 15028670797073718546)
# rg+mf = 13054637933699032665165943687110631912
# e = 259719708311083043320270690207664511027 + 114514 = 259719708311083043320270690207664625541
# a = 13054637933699032665165943687110631912
# b = 114514