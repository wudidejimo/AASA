import json
import pickle
import socket
import struct
import time

from FunctionMod import *



# socke配置
NodeA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('127.0.0.1', 123)
NodeA.connect(server_address)

# 获取注册信息
client_type = "A"

deltT = 1.0

# 初始化阶段 注册阶段
IDi = secrets.token_bytes(16).hex()
PWi = secrets.token_bytes(16).hex()
a = secrets.token_bytes(32).hex()
Bio = secrets.token_bytes(16).hex()
RPWi =hash_256(IDi,PWi,Bio)
RPWi_star =xor_strings(RPWi, a)
LL = [client_type, IDi, RPWi_star]
NodeA.send(pickle.dumps(LL))




TIDi, ki, Ai = pickle.loads(NodeA.recv(1024))
hash_mk = xor_strings(Ai,RPWi_star)

Ai_star = xor_strings(Ai,a)
ki_star =  xor_strings(ki,xor_strings(RPWi,Bio))
V0 = hash_256(IDi, RPWi,ki,hash_mk)


# 等待Server的通知 收到通知就开始计时
IDj = pickle.loads(NodeA.recv(1024))

# 认证开始========================================================================================
t1 = time.perf_counter() 
RPWi_star = hash_256(IDi,PWi,Bio)
hash_mk_star = xor_strings(Ai_star, RPWi_star)
ki1 = xor_strings(ki_star, xor_strings(RPWi_star, Bio))

V0_star = hash_256(IDi, RPWi_star, ki1,hash_mk_star)

if V0_star != V0:
    raise ValueError("Ai验证失败")
ki1 = ki1[:32]
hash_mk_star1 = hash_mk_star[:32]
r1 = secrets.token_bytes(16).hex()
T1 = time.time()
S1 = hash_256(RPWi_star,hash_mk_star1,T1)[:32]
X1 = xor_strings((r1 + S1), hash_256(TIDi, IDj, T1))
X2 = xor_strings((hash_mk_star1 + ki1), hash_256(TIDi, IDj, r1))

V1 = hash_256(X1,X2,S1,ki1,r1,T1)

section_A1 = time.perf_counter() - t1

M1 = [X1,X2, V1, T1]
NodeA.send(pickle.dumps(M1))
# M1发送成功


t2 = time.perf_counter() 
NodeA_sectionOne_T1 = (t2-t1)*1000

# 接收消息4
X6, V4, T4= pickle.loads(NodeA.recv(1024))
t3 = time.perf_counter() 

if time.time()-T4>deltT:
    raise ValueError("T3过期")

temp = xor_strings(X6, hash_256(TIDi, S1))
SK_star = temp[32:]
TIDi_new = temp[:32]

V4_star = hash_256(X6,  S1, SK_star,TIDi_new, T4)

if V4_star !=V4:
    raise ValueError("MSG4验证失败")


section_A2 = (time.perf_counter() -t3)*1000


print("NodeA_section:",section_A1+section_A2)

t4 = time.perf_counter()
print("总时间: ", (t4 - t1) * 1000)

# 关闭连接
NodeA.close()
