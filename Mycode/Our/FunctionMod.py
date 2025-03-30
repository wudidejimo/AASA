import nist256.ecdh as ecdh
import nist256.curve as curve
import nist256.big as big
import nist256.ecp as ecp
from nist256.sha256 import SHA256
from pypuf.simulation import XORArbiterPUF, ArbiterPUF
import numpy as np
import hashlib
from sympy.polys.polyfuncs import interpolate
from typing import List, Tuple
import numpy as np
from numpy.polynomial.polynomial import Polynomial
from sympy import Integer
from os import urandom
from hashlib import pbkdf2_hmac
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import random
from sympy import Integer, Symbol, expand, Rational
import secrets
# Fast Recursion
def T(n, x, p):
    if n == 0:
        return 1
    elif n == 1:
        return x
    elif n % 2 == 0:  # 偶数
        temp = T(n // 2, x, p)
        return (2 * temp * temp - 1) % p
    else:
        if n % 4 == 1:
            odd = (n + 3) // 4
            even = (n - 1) // 4  # 偶数
        else:
            odd = (n - 3) // 4
            even = (n + 1) // 4
        A = T(even, x, p)
        B = T(odd, x, p)
        C = (2 * A * A - 1) % p
        D = (2 * A * B - x) % p
        return (2 * C * D - x) % p


def hash_256_(*args):
    str1 = ""
    for arg in args:
        str1 = str1 + str(arg)
    str1 = str1.encode()
    return hashlib.sha3_256(str1).hexdigest()

def hash_256(*args):
    str1 = ""
    for arg in args:
        str1 = str1 + str(arg)
    str1 = str1.encode()
    return SHA256(str1).hexdigest()

def hash_512(*args):
    str1 = ""
    for arg in args:
        str1 = str1 + str(arg)
    str1 = str1.encode()
    return hashlib.sha3_512(str1).hexdigest()

def a_mul_p(a, G):
    Y = a * G
    return Y


def a_mul_pk(a, W):
    return ecdh.ECP_SvdpDH(a, W)

def hex_string_to_ndarray(hex_string):
    # 确保输入的 hex 字符串长度为 64 个字符（256 位），不足则左侧补 0
    hex_string = hex_string.zfill(64)
    # 将十六进制字符串转换为 32 字节，然后展开成 256 位数组
    b = bytes.fromhex(hex_string)
    bits = np.unpackbits(np.frombuffer(b, dtype=np.uint8))
    # 将 0 映射为 -1，1 映射为 1，并重塑为 (32, 8)
    return (bits.astype(np.int8) * 2 - 1).reshape((32, 8))

def ndarray_to_hex_string(ndarray):
    # 扁平化数组，并将 -1 映射为 0，1 保持为 1
    flat = ndarray.flatten()
    bits = ((flat + 1) // 2).astype(np.uint8)
    # 打包为字节，再转换为十六进制字符串（大写，并确保 64 位，不足则补 0）
    packed = np.packbits(bits)
    return packed.tobytes().hex().upper().zfill(64)

def expand_hex_string_to_ndarray(hex_string: str):
    total_blocks = 8  # 初始块加上 7 次更新共 8 块
    output = np.empty((32 * total_blocks, 8), dtype=np.int8)
    
    # 处理初始十六进制字符串
    output[:32] = hex_string_to_ndarray(hex_string)
    m = hashlib.sha256()
    
    # 生成后续 7 块，每次使用上一次的十六进制字符串进行 SHA256 更新
    for i in range(1, total_blocks):
        m.update(hex_string.encode('utf-8'))
        hex_string = m.hexdigest()
        output[i * 32:(i + 1) * 32] = hex_string_to_ndarray(hex_string)
    
    return output

def get_puf(c: str):
    # 扩展十六进制字符串为完整的 ndarray
    expanded_array = expand_hex_string_to_ndarray(c)
    # 评估 XOR Arbiter PUF（假设 XORArbiterPUF 已经定义）
    result_ndarray = XORArbiterPUF(n=8, k=1, seed=1).eval(expanded_array)
    # 转换结果为十六进制字符串返回
    return ndarray_to_hex_string(result_ndarray)



# def hex_string_to_ndarray(hex_string):
#     binary_string = bin(int(hex_string, 16))[2:].zfill(256)
#     binary_array = np.array(
#         [int(bit) * 2 - 1 for bit in binary_string], dtype=np.int8).reshape((32, 8))
#     return binary_array


# def ndarray_to_hex_string(ndarray):
#     # Flatten the ndarray to a 1D array
#     flattened_array = ndarray.flatten()

#     # Convert -1 to '0' and 1 to '1' in the flattened array
#     binary_array = ['1' if x == 1 else '0' for x in flattened_array]

#     # Join the binary digits into a single binary string
#     binary_string = ''.join(binary_array)

#     # Convert the binary string to a hex string
#     hex_string = hex(int(binary_string, 2))[2:].upper()

#     # Pad the hex string with leading zeros to make it 64 characters (256 bits)
#     hex_string = hex_string.zfill(64)

#     return hex_string


# def expand_hex_string_to_ndarray(hex_string: str):
#     m = hashlib.sha256()
#     c = hex_string_to_ndarray(hex_string)
#     for _ in range(0, 7):
#         m.update(hex_string.encode('utf-8'))
#         hex_string = m.hexdigest()
#         nd = hex_string_to_ndarray(m.hexdigest())
#         c = np.concatenate((c, nd), axis=0)
#     return c


# def get_puf(c: str):
#     c = expand_hex_string_to_ndarray(c)
#     r = ndarray_to_hex_string(XORArbiterPUF(n=8, k=1, seed=1).eval(c))
#     return r


def xor_strings(str1, str2):
    len2 = min(len(str1), len(str2))
    if (len(str1) > len(str2)):
        str3 = str1[:len2]
        result = ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(str3, str2))
        return result + str1[len2:]
    else:
        str3 = str2[:len2]
        result = ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(str1, str3))
        return result + str2[len2:]

# PKCS7填充方法，确保明文长度是16的倍数
def pad(text):
    padding_size = 16 - (len(text) % 16)
    return text + chr(padding_size) * padding_size

# PKCS7解填充
def unpad(text):
    return text[:-ord(text[-1])]

# AES加密
def encrypt(text, key, iv):
    try:
        if isinstance(text, str):  # 兼容字符串输入
            text = text.encode('utf-8')
        key = key.encode('utf-8') if isinstance(key, str) else key
        iv = iv.encode('utf-8') if isinstance(iv, str) else iv
        
        text = pad(text.decode('utf-8')).encode('utf-8')  # 先填充再编码
        cipher = AES.new(key, AES.MODE_CBC, iv)
        cipher_text = cipher.encrypt(text)
        return b2a_hex(cipher_text).decode()  # 转换为16进制字符串，方便存储
    except Exception as e:
        print(f"加密错误: {e}")
        return None

# AES解密
def decrypt(cipher_text, key, iv):
    try:
        key = key.encode('utf-8') if isinstance(key, str) else key
        iv = iv.encode('utf-8') if isinstance(iv, str) else iv
        
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plain_text = cipher.decrypt(a2b_hex(cipher_text))
        return unpad(plain_text.decode('utf-8'))
    except Exception as e:
        print(f"解密错误: {e}")
        return None








class SecretSharing:
    def __init__(self, secret: int):
        """
        初始化秘密共享系统，使用 SymPy 进行高效计算。
        :param secret: 需要保护的秘密值（整数）。
        """
        self.secret = Integer(secret)
        self.coefficients = [self.secret] + [Integer(random.randint(0, 10**10 - 1)) for _ in range(4)]
    
    def generate_shares(self, x_values: List[int]) -> List[Tuple[int, int]]:
        """
        使用 SymPy 计算 f(x) 值，大幅提高分片生成速度并保持精度。
        :param x_values: 需要计算 f(x) 的 x 值列表。
        :return: 计算出的 (x, f(x)) 对
        """
        shares = []
        for x in x_values:
            share_value = sum(coef * Integer(x)**i for i, coef in enumerate(self.coefficients))
            shares.append((x, int(share_value)))  # 确保返回整数，避免 SymPy 符号类型
        return shares

    @staticmethod
    def reconstruct_secret(shares: List[Tuple[int, int]]) -> int:
        """
        使用高效数值计算的拉格朗日插值恢复秘密，避免符号计算的额外开销。
        :param shares: 至少 5 份 (x, f(x)) 的分片数据
        :return: 恢复出的秘密值
        """
        if len(shares) < 5:
            raise ValueError("需要至少 5 份分片才能恢复秘密！")

        secret = Integer(0)  # 使用 SymPy 的高精度整数
        for i in range(len(shares)):
            xi, yi = shares[i]
            num, den = Integer(1), Integer(1)  # 计算拉格朗日基
            for j in range(len(shares)):
                if i != j:
                    xj, _ = shares[j]
                    num *= -xj
                    den *= (xi - xj)
            secret += yi * Rational(num, den)  # 使用 Rational 保持精度

        return int(secret)  # 转换回 Python 整数




class FuzzyKeyExtractor:
    def __init__(self, length=None, num_helpers=5, nonce_len=8, cipher_len=32, hash_func='sha256'):
        self.length = length
        self.num_helpers = num_helpers
        self.nonce_len = nonce_len
        self.cipher_len = cipher_len
        self.hash_func = hash_func

    def generate(self, value):
        if isinstance(value, (bytes, str)):
            value = np.frombuffer(value.encode() if isinstance(value, str) else value, dtype=np.uint8)

        if self.length is None:
            self.length = len(value)

        key = np.frombuffer(urandom(self.length), dtype=np.uint8)
        key_pad = np.concatenate((key, np.zeros(self.cipher_len - self.length, dtype=np.uint8)))  # 修正长度

        nonces = np.zeros((self.num_helpers, self.nonce_len), dtype=np.uint8)
        masks = np.zeros((self.num_helpers, self.length), dtype=np.uint8)
        digests = np.zeros((self.num_helpers, self.cipher_len), dtype=np.uint8)

        for helper in range(self.num_helpers):
            nonces[helper] = np.frombuffer(urandom(self.nonce_len), dtype=np.uint8)
            masks[helper] = np.frombuffer(urandom(self.length), dtype=np.uint8)

        vectors = np.bitwise_and(masks, value)

        for helper in range(self.num_helpers):
            digest = pbkdf2_hmac(self.hash_func, vectors[helper].tobytes(), nonces[helper].tobytes(), 1, self.cipher_len)
            digests[helper] = np.frombuffer(digest, dtype=np.uint8)

        ciphers = np.bitwise_xor(digests, key_pad)  # 现在 key_pad.shape = (32,)

        return (key.tobytes(), (ciphers, masks, nonces))

    def reproduce(self, value, helpers):
        if isinstance(value, (bytes, str)):
            value = np.frombuffer(value.encode() if isinstance(value, str) else value, dtype=np.uint8)

        if len(value) != self.length:
            raise ValueError(f'Cannot reproduce key: expected length {self.length}, got {len(value)}')

        ciphers, masks, nonces = helpers
        vectors = np.bitwise_and(masks, value)

        digests = np.zeros((self.num_helpers, self.cipher_len), dtype=np.uint8)
        for helper in range(self.num_helpers):
            digest = pbkdf2_hmac(self.hash_func, vectors[helper].tobytes(), nonces[helper].tobytes(), 1, self.cipher_len)
            digests[helper] = np.frombuffer(digest, dtype=np.uint8)

        plains = np.bitwise_xor(digests, ciphers)

        return plains[0, :self.length].tobytes() if np.sum(plains[:, self.length:]) == 0 else None
    


