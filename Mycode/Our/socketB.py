import pickle
import socket
import time

from FunctionMod import *
import re
import json

NodeB = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('127.0.0.1', 123)
NodeB.connect(server_address)

client_type = "B"

R = []


deltT = 1.0

# 初始化阶段 注册阶段
C = [secrets.token_bytes(16).hex() for _ in range(6)]  
R = [int(get_puf(c), 16)% (10**12) for c in C]  



IDj = secrets.token_bytes(16).hex()

LL = [client_type, IDj, R]
NodeB.send(pickle.dumps(LL))

X_Sj = pickle.loads(NodeB.recv(1024))



# 接受Msg2==========================================================================
X3, shares, V2, T2 = pickle.loads(NodeB.recv(4096))
startT1 = time.perf_counter()


if time.time()-T2>deltT:
    raise ValueError("T2过期")


temp2 = (xor_strings(X3, hash_256(X_Sj, IDj, T2)))
r1 = temp2[:32]
S1 = temp2[32:]



R_star = [get_puf(c) for c in C]


t0 = time.perf_counter()
Xfs_star = SecretSharing.reconstruct_secret(shares[:5])
print("reconstruct:",(time.perf_counter()-t0)*1000)

V2_star = hash_256(X3, S1, r1, Xfs_star, T2)


if V2_star != V2:
    raise ValueError("M2验证失败")

# ==============================================
r2 = secrets.token_bytes(16).hex()
T3 = time.time()



C_new = [secrets.token_bytes(16).hex() for _ in range(5)] 
R_new = [get_puf(c) for c in C_new]  # 确保 PUF 返回的是十六进制字符串

R_new_str = "".join(R_new)  # 拼接成字符串





# 建立会话密钥
SK = hash_256(S1, Xfs_star, r1, r2)[:32]
X4 = xor_strings(r2, hash_256(S1, Xfs_star, T3)[:32])
X5 = xor_strings(R_new_str, hash_256(S1, Xfs_star, r2))
V3 = hash_256(X4, X5, S1, IDj, Xfs_star, SK, T3)
print("NodeB_section:",(time.perf_counter()-startT1)*1000)



# 发送msg3====================================================================================
M3 = [X4, X5, V3, T3]
NodeB.send(pickle.dumps(M3))
# 关闭连接
NodeB.close()
