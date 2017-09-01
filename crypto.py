from Crypto.Cipher import DES3
import base64

encoding = "utf-8"
secret_key = "changxinganhui2016*04*25"
iv = "01234567"

# PKCS#5 PKCS#7
BS = DES3.block_size
pad = lambda s: s + (BS - len(s) % BS) * bytes([BS - len(s) % BS])
unpad = lambda s: s[0:-(s[-1])]



def encode(plaintext):
    data_bytes = bytes(plaintext, encoding='utf-8')
    des3 = DES3.new(secret_key, mode=DES3.MODE_CBC, IV=iv)
    result = des3.encrypt(pad(data_bytes))
    ciphertext = base64.b64encode(result)
    return ciphertext



def decode(ciphertext):
    ciphertext = base64.b64decode(ciphertext)
    des3 = DES3.new(secret_key, mode=DES3.MODE_CBC, IV=iv)
    result = des3.decrypt(ciphertext)
    plaintext = unpad(result)
    return str(plaintext, encoding='utf-8')


def test():
    import json
    res = encode(json.dumps({'linename': '1路'}, ensure_ascii=False, separators=(',', ':')))
    print('encode:', res)
    res = decode(res)
    print('decode:', res)

if __name__ == "__main__":
    test()
