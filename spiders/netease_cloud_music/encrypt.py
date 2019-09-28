import cgi
import json
import math
import random
from Crypto.Cipher import AES
import base64
import codecs


class Encrypt(object):
    MODULES = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    NONCE = '0CoJUm6Qyw8W8jud'
    PUB_KEY = '010001'

    @staticmethod
    def _create_secretKey(size):
        """
        生成指定长度的随机字符串
        """
        string = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        random_str = ""
        for i in range(size):
            e = math.floor(random.random() * len(string))
            random_str += list(string)[e]
        return random_str

    @staticmethod
    def _aes_encrypt(msg, key):
        """
        AES 加密
        """
        padding = 16 - len(msg) % 16  # 如果不是 16 的倍数则进行 padding
        msg = msg + padding * chr(padding)  # 这里使用 padding 对应的单字符进行填充
        iv = '0102030405060708'  # 用来加密或者解密的初始向量（必须是 16 位）

        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted_bytes = cipher.encrypt(msg)  # 加密后得到的是 bytes 类型的数据
        encode_str = base64.b64encode(encrypted_bytes)  # 使用 Base64 进行编码,返回 byte 字符串
        encode_text = encode_str.decode('utf-8')  # 对 byte 字符串按 utf-8 进行解码

        return encode_text

    @staticmethod
    def _rsa_encrypt(random_str, key, f):
        """
        RSA加密
        """
        string = random_str[::-1]  # 随机字符串逆序排列
        text = bytes(string, 'utf-8')  # 将随机字符串转换成 bytes 类型数据
        sec_key = int(codecs.encode(text, encoding='hex'), 16) ** int(key, 16) % int(f, 16)
        return format(sec_key, 'x').zfill(256)

    @classmethod
    def encrypted_request(cls, text):
        text = json.dumps(text)
        secKey = cls._create_secretKey(16)
        encText = cls._aes_encrypt(cls._aes_encrypt(text, cls.NONCE), secKey)
        encSecKey = cls._rsa_encrypt(secKey, cls.PUB_KEY, cls.MODULES)
        data = {
            'params': encText,
            'encSecKey': encSecKey
        }
        return data

    @classmethod
    def get_encoding_from_headers(cls, headers):
        content_type = headers.get('content-type')

        if not content_type:
            return None

        content_type, params = cgi.parse_header(content_type)

        if 'charset' in params:
            return params['charset'].strip("'\"")

        if 'text' in content_type:
            return 'ISO-8859-1'
