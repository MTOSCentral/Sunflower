import base64
class EncryptPass:
    def __init__(self):
        pass
    def encrypt(self,key, clear):
        enc = []
        for i in range(len(clear)):
            key_c = key[i % len(key)]
            enc_c = (ord(clear[i]) + ord(key_c)) % 256
            enc.append(enc_c)
        return base64.urlsafe_b64encode(bytes(enc))
    def decrypt(self,key, enc):
        dec = []
        enc = base64.urlsafe_b64decode(enc)
        for i in range(len(enc)):
            key_c = key[i % len(key)]
            dec_c = chr((256 + enc[i] - ord(key_c)) % 256)
            dec.append(dec_c)
        return "".join(dec)
