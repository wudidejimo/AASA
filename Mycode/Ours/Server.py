import json
import pickle
import socket
import time

from FunctionMod import *
from nist256.curve import p

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('127.0.0.1', 123)
server_socket.bind(server_address)
server_socket.listen(2)

 

shares=[]


MK = secrets.token_bytes(16).hex()
Xfs = int(secrets.token_bytes(16).hex(),16)
Honey_list = []
clients = {}
b_registration_stage = {}  
deltT = 1.0
while len(clients) < 2:
    client_socket, client_address = server_socket.accept()

   
    revice = pickle.loads(client_socket.recv(1024))

    if revice[0]=="A":
        clients["A"] = client_socket
        client_type, IDi, RPWi_star = revice
        T0 = secrets.token_bytes(16).hex()
        r0 = secrets.token_bytes(16).hex()

        TIDi = hash_256(IDi, T0)
        ki =  hash_256(IDi, hash_256(MK),r0)
        Ai = xor_strings(RPWi_star, hash_256(MK))
        msg0_A = [TIDi, ki, Ai]
        clients["A"].send(pickle.dumps(msg0_A))
    elif revice[0]=="B":
              
            clients["B"] = client_socket 
            client_type,  IDj, R = revice      
            X_Sj = hash_256(IDj, hash_256(MK))

            sss = SecretSharing(secret=Xfs)
            shares = sss.generate_shares(R)
            
            clients["B"].send(pickle.dumps(X_Sj))
            
            
           
        



clients.get("A").send(pickle.dumps(IDj))

X1, X2, V1, T1 = pickle.loads(clients.get("A").recv(1024))


if time.time()-T1>deltT:
    raise ValueError("T1 out")

startT1 = time.perf_counter()

temp1 = xor_strings(X1[:64], hash_256(TIDi, IDj, T1))
S1 = temp1[32:]  
r1 = temp1[:32]  



# 修正 X2 解码
decoded_value = xor_strings(X2[:64], hash_256(TIDi, IDj, r1))  
hash_mk_star = decoded_value[:32]
ki_star = decoded_value[32:]

ki = ki[:32]

if ki_star != ki:
    raise ValueError("fail")

V1_star = hash_256(X1,X2,S1,ki,r1,T1)

if V1_star != V1:
    raise ValueError("M1fail")


# ==============================================
T2 = time.time()
X3 = xor_strings((r1 + S1), hash_256(X_Sj, IDj, T2))

V2 = hash_256(X3, S1, r1, Xfs, T2)

server_section1 = time.perf_counter()-startT1



M2 = [X3, shares, V2, T2]
clients.get("B").send(pickle.dumps(M2))
# =====================================

X4, X5, V3, T3 = pickle.loads(clients.get("B").recv(1024))

if time.time()-T3>deltT:
    raise ValueError("T3out")
startT2 = time.perf_counter()
r2_star = xor_strings(X4, hash_256(S1, Xfs, T3)[:32])
SK_star = hash_256(S1, Xfs, r1, r2_star)[:32]
V3_star = hash_256(X4, X5, S1, IDj,Xfs, SK_star, T3)



if V3_star != V3:
    raise ValueError("M3fail")

#==================================
T4 = time.time()


R_new_str = xor_strings(X5, hash_256(S1, Xfs, r2_star))

R_new = [int(R_new_str[i:i+32].ljust(32, '0'), 16) % (10**10) for i in range(0, len(R_new_str), 32)][:5]


shares_new = sss.generate_shares(R_new)
Xfs_new = sss.reconstruct_secret(shares_new[:5])


TIDi_new = hash_256(TIDi, T4)[:32]
X6 = xor_strings(TIDi_new + SK_star, hash_256(TIDi, S1))

V4 = hash_256(X6, S1, SK_star, TIDi_new,  T4)

server_section2 = time.perf_counter()-startT2

print("server_section:",(server_section1+server_section2)*1000)

M4 = [X6, V4, T4]

clients.get("A").send(pickle.dumps(M4))



for client_socket in clients.values():
    client_socket.close()
server_socket.close()
