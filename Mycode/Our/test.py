import json
import pickle
import socket
import time
import secrets
from FunctionMod import *

import sys   #sys模块提供了一系列有关Python运行环境的变量和函数。



print(sys.version)


# Chaos mapping parameters
ri= 399202342336 # 155033642076
p= 115792089210356248762697446949407573530086143415290314195533631308867097853951
rj = 3983623723 # 1594324474

G = ecp.generator()
x = secrets.token_bytes(16).hex()




CA =""
# random
t1 = time.perf_counter()
for i in range(1000):
    CA = secrets.token_bytes(16).hex()
t2 = time.perf_counter()
print("getRandom:",(t2-t1))   # res*1000 /1000 = res




# hash function
t1 = time.perf_counter()
for i in range(1000):
    hash_256(x)
t2 = time.perf_counter()
print("Hash:",(t2-t1))

# PUF
t1 = time.perf_counter()
for i in range(1000):
    RA = get_puf(CA)
    if i == 0:
        print(RA)
t2 = time.perf_counter()
print("PUF:",(t2-t1))


m0 = secrets.token_bytes(16).hex()
r0 = secrets.token_bytes(16).hex()
x = secrets.token_bytes(32).hex()
pk1 = a_mul_p(int(x,16), G)
k1_star = big.modadd(int(m0, 16), big.modmul(int(r0, 16), int(x,16), curve.r),
                         curve.r) % curve.r  # (m + r*s)

# Construct Chameleon Random Numbers
r1 = secrets.token_bytes(16).hex()
T1 = time.time()
r1_1 = hash_256(r1,T1)[:32]
m1 = big.modsub(int(k1_star), big.modmul(int(r1_1, 16), int(x, 16), curve.r), curve.r)
#  Chameleon hash function
t1 = time.perf_counter()
for i in range(100):
    CH1_2 = ecp.mul(G, int(m1), pk1, int(r1_1, 16))
t2 = time.perf_counter()
print("CH:",(t2-t1)*1000/100)


# Tm
aaa = int(x,16)
t1 = time.perf_counter()
for i in range(10):
    pk = aaa*G
t2 = time.perf_counter()
print("Tepm:",(t2-t1)*1000/10)

# chaotic map
xx = secrets.token_bytes(16).hex()
t1 = time.perf_counter()
for i in range(100):
    T(ri,int(xx,16),p)
t2 = time.perf_counter()
print("Tcm:",(t2-t1)*1000/100)



# # Fuzzy Extractor
original_value = b"Hello, Secure Key!"
extractor = FuzzyKeyExtractor()

# 计算 generate() 的时间
t1 = time.perf_counter()
for _ in range(100):
    key, helpers = extractor.generate(original_value)
t2 = time.perf_counter()
# print("Generated Key:", key.hex())
print("Generate Time(Gen):", (t2 - t1) * 1000 / 100, "ms")

# 计算 reproduce() 的时间
t1 = time.perf_counter()
for _ in range(100):
    recovered_key = extractor.reproduce(original_value, helpers)
t2 = time.perf_counter()
# print("Recovered Key:", recovered_key.hex() if recovered_key else "Key could not be recovered.")
print("Reproduce Time(Rep):", (t2 - t1) * 1000 / 100, "ms")





#secret sharing
secret = int(secrets.token_bytes(16).hex(), 16)
ss = SecretSharing(secret=secret)
C = [secrets.token_bytes(16).hex() for _ in range(5)]  
R = [int(get_puf(c), 16) for c in C] 

# 计算 generate_shares() 的时间
t1 = time.perf_counter()
for _ in range(100):
    shares = ss.generate_shares(R)
    recovered_secret = ss.reconstruct_secret(shares[:5])
t2 = time.perf_counter()
print("Tsm:", (t2 - t1) * 1000 / 100, "ms")


# symmetric encryption
text = secrets.token_bytes(16).hex()
key = secrets.token_bytes(16).hex()
iv = secrets.token_bytes(16)
t1 = time.perf_counter()
for _ in range(100):
    encrypted_text = encrypt(text,key,iv)  # 加密 
    d = decrypt(encrypted_text,key,iv)  # 解密 
t2 = time.perf_counter()
print("Tenc:", (t2 - t1) * 1000 / 100/2, "ms")



