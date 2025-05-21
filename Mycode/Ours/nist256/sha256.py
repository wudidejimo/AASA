import struct
class SHA256:
    # 常量 K
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

    # 初始哈希值 H
    _initial_H = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
    ]

    def __init__(self, message=b''):
        self._buffer = message

    def update(self, message):
        self._buffer += message

    def _pad(self, message):
        """
        优化后的填充：
         - 添加一个 0x80 字节
         - 计算需要补充的 0 字节数后一次性添加
         - 最后添加原始消息长度（64-bit 大端整数）
        """
        original_length = len(message) * 8
        message += b'\x80'
        # 消息长度需要满足： (len(message)*8 + 64) % 512 == 0
        pad_len = (56 - (len(message) % 64)) % 64
        message += b'\x00' * pad_len
        message += struct.pack('>Q', original_length)
        return message

    def digest(self):
        padded = self._pad(self._buffer)
        mask = 0xffffffff
        K = self.K  # 常量列表
        # 使用局部变量缓存初始哈希值
        h0, h1, h2, h3, h4, h5, h6, h7 = self._initial_H

        # 按 512-bit（64 字节）块处理消息
        for i in range(0, len(padded), 64):
            block = padded[i:i + 64]
            # 将 64 字节分解成 16 个 32-bit 无符号整数
            W = list(struct.unpack('>16L', block))
            W += [0] * 48

            # 消息扩展
            for j in range(16, 64):
                w15 = W[j - 15]
                # 内联旋转：右移 n 位 = (x >> n) | (x << (32 - n))
                s0 = (((w15 >> 7) | (w15 << (32 - 7))) & mask) ^ \
                     (((w15 >> 18) | (w15 << (32 - 18))) & mask) ^ (w15 >> 3)
                w2 = W[j - 2]
                s1 = (((w2 >> 17) | (w2 << (32 - 17))) & mask) ^ \
                     (((w2 >> 19) | (w2 << (32 - 19))) & mask) ^ (w2 >> 10)
                W[j] = (W[j - 16] + s0 + W[j - 7] + s1) & mask

            a, b, c, d = h0, h1, h2, h3
            e, f, g, h = h4, h5, h6, h7

            # 64轮压缩
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

            # 累加每个块的结果
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

# class SHA256:
#     # 常量 K
#     K = [
#         0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
#         0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
#         0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
#         0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
#         0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
#         0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
#         0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
#         0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
#         0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
#         0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
#         0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
#         0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
#         0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
#         0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
#         0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
#         0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
#     ]

#     # 初始哈希值 H
#     _initial_H = [
#         0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
#         0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
#     ]

#     def __init__(self, message=b''):
#         """
#         初始化 SHA256 实例，可以传入初始消息（字节串）。
#         """
#         self._buffer = message

#     def update(self, message):
#         """
#         添加消息数据，message 为字节串
#         """
#         self._buffer += message

#     @staticmethod
#     def rotr(x, n, bits=32):
#         """
#         右移运算：将 x 右移 n 位（循环右移）
#         """
#         return ((x >> n) | (x << (bits - n))) & ((1 << bits) - 1)

#     def _pad(self, message):
#         """
#         对消息进行填充：
#          - 首先追加一个 0x80 字节（即10000000）
#          - 然后追加 0x00 字节，直到消息长度满足 (len*8 + 64) % 512 == 0
#          - 最后追加原始消息长度（64-bit大端整数）
#         """
#         original_length = len(message) * 8
#         message += b'\x80'
#         while (len(message) * 8 + 64) % 512 != 0:
#             message += b'\x00'
#         message += struct.pack('>Q', original_length)
#         return message

#     def digest(self):
#         """
#         返回 32 字节的 SHA-256 哈希值（bytes）。
#         """
#         padded = self._pad(self._buffer)
#         H = self._initial_H.copy()

#         # 按 512-bit (64 字节) 块处理消息
#         for i in range(0, len(padded), 64):
#             block = padded[i:i + 64]
#             # 将 64 字节分解成 16 个 32-bit 无符号整数，并扩展到 64 个整数
#             W = list(struct.unpack('>16L', block)) + [0] * 48

#             # 消息扩展
#             for j in range(16, 64):
#                 s0 = self.rotr(W[j - 15], 7) ^ self.rotr(W[j - 15], 18) ^ (W[j - 15] >> 3)
#                 s1 = self.rotr(W[j - 2], 17) ^ self.rotr(W[j - 2], 19) ^ (W[j - 2] >> 10)
#                 W[j] = (W[j - 16] + s0 + W[j - 7] + s1) & 0xFFFFFFFF

#             # 初始化工作寄存器
#             a, b, c, d, e, f, g, h = H

#             # 64 轮压缩函数
#             for j in range(64):
#                 S1 = self.rotr(e, 6) ^ self.rotr(e, 11) ^ self.rotr(e, 25)
#                 ch = (e & f) ^ ((~e) & g)
#                 temp1 = (h + S1 + ch + self.K[j] + W[j]) & 0xFFFFFFFF
#                 S0 = self.rotr(a, 2) ^ self.rotr(a, 13) ^ self.rotr(a, 22)
#                 maj = (a & b) ^ (a & c) ^ (b & c)
#                 temp2 = (S0 + maj) & 0xFFFFFFFF

#                 h = g
#                 g = f
#                 f = e
#                 e = (d + temp1) & 0xFFFFFFFF
#                 d = c
#                 c = b
#                 b = a
#                 a = (temp1 + temp2) & 0xFFFFFFFF

#             # 累加当前块的计算结果
#             H = [
#                 (H[0] + a) & 0xFFFFFFFF,
#                 (H[1] + b) & 0xFFFFFFFF,
#                 (H[2] + c) & 0xFFFFFFFF,
#                 (H[3] + d) & 0xFFFFFFFF,
#                 (H[4] + e) & 0xFFFFFFFF,
#                 (H[5] + f) & 0xFFFFFFFF,
#                 (H[6] + g) & 0xFFFFFFFF,
#                 (H[7] + h) & 0xFFFFFFFF,
#             ]

#         # 返回 32 字节的哈希值
#         return b''.join(struct.pack('>L', h) for h in H)

#     def hexdigest(self):
#         """
#         返回 64 位十六进制字符串表示的哈希值。
#         """
#         return ''.join(f'{x:02x}' for x in self.digest())
 