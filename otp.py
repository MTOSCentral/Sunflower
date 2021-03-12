import time
from datetime import datetime
import pyotp
class OTP:
    def __init__(self,brand):
        self.brand=brand
        self.time_steps = int(time.mktime(datetime.utcnow().timetuple()) / 30)
        
    def genOTP(self):
        pw=pyotp.random_base32()
        qr_str=pyotp.totp.TOTP(pw).provisioning_uri('', issuer_name=self.brand+" 2 Factor Authentication")
        return [pw,qr_str]

    def VerifyOTP(self,pw,code):
        totp = pyotp.TOTP(pw)
        cor = totp.verify(code)
        return cor
