import time
import numpy as np
import hashlib
import secrets
from FunctionMod import *
import numpy as np
import hashlib

import numpy as np
import hashlib
import numpy as np
import hashlib

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

def get_puf1(c: str):
    # 扩展十六进制字符串为完整的 ndarray
    expanded_array = expand_hex_string_to_ndarray(c)
    # 评估 XOR Arbiter PUF（假设 XORArbiterPUF 已经定义）
    result_ndarray = XORArbiterPUF(n=8, k=1, seed=1).eval(expanded_array)
    # 转换结果为十六进制字符串返回
    return ndarray_to_hex_string(result_ndarray)

# def hex_string_to_ndarray(hex_string):
#     # 将十六进制字符串转换为 32 字节，然后展开成 256 位数组
#     b = bytes.fromhex(hex_string)
#     bits = np.unpackbits(np.frombuffer(b, dtype=np.uint8))
#     # 将 0 映射为 -1，1 保持为 1，并重塑为 (32, 8)
#     return (bits.astype(np.int8) * 2 - 1).reshape((32, 8))

# def ndarray_to_hex_string(ndarray):
#     # 扁平化数组，并将 -1 映射为 0，1 保持为 1
#     flat = ndarray.flatten()
#     bits = ((flat + 1) // 2).astype(np.uint8)
#     # 打包为字节，再转换为十六进制字符串（大写，并确保 64 位，不足则补 0）
#     packed = np.packbits(bits)
#     return packed.tobytes().hex().upper().zfill(64)

# def expand_hex_string_to_ndarray(hex_string: str):
#     total_blocks = 8  # 初始块加上 7 次更新共 8 块
#     output = np.empty((32 * total_blocks, 8), dtype=np.int8)
    
#     # 处理初始十六进制字符串
#     output[:32] = hex_string_to_ndarray(hex_string)
#     m = hashlib.sha256()
    
#     # 生成后续 7 块，每次使用上一次的十六进制字符串进行 SHA256 更新
#     for i in range(1, total_blocks):
#         m.update(hex_string.encode('utf-8'))
#         hex_string = m.hexdigest()
#         output[i * 32:(i + 1) * 32] = hex_string_to_ndarray(hex_string)
    
#     return output

# def get_puf1(c: str):
#     # 扩展十六进制字符串为完整的 ndarray
#     expanded_array = expand_hex_string_to_ndarray(c)
#     # 评估 XOR Arbiter PUF（假设 XORArbiterPUF 已经定义）
#     result_ndarray = XORArbiterPUF(n=8, k=1, seed=1).eval(expanded_array)
#     # 转换结果为十六进制字符串返回
#     return ndarray_to_hex_string(result_ndarray)


# -------------- 测试代码 --------------
def run_tests():
    print("===== 测试 PUF 性能和正确性 =====")
    
    # 1. 生成随机 HEX 输入
    hex_input = secrets.token_bytes(16).hex()
    print(f"测试输入: {hex_input}")

    # 2. 计算 PUF 输出
    start_time1 = time.perf_counter()
    for _ in range(1000):
        puf_output1 = get_puf1(hex_input)
    end_time1 = time.perf_counter()
    

    start_time = time.perf_counter()
    for _ in range(1000):
        puf_output = get_puf(hex_input)
    end_time = time.perf_counter()
    # 3. 打印结果
    print(f"PUF 输出: {puf_output1}")
    print(f"计算时间: {end_time1 - start_time1:.6f} ms")
      # 3. 打印结果
    print(f"PUF 输出: {puf_output}")
    print(f"计算时间: {end_time - start_time:.6f} ms")
 
if __name__ == "__main__":
    run_tests() 
