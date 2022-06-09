import chipwhisperer.analyzer as cwa
from chipwhisperer.analyzer.attacks.models.aes.key_schedule import key_schedule_rounds


class AesCBC(cwa.AESLeakageHelper):
    def __init__(self):
        self.prevct = [0] * 16 # IV
    def leakage(self, pt, ct, key, bnum):
        final = self.sbox(pt[bnum] ^ self.prevct[bnum] ^ key[bnum])
        self.prevct = ct
        return final

class AesCFB(cwa.AESLeakageHelper):
    def __init__(self):
        self.prevct = [0] * 16 # starts as IV value
    def leakage(self, pt, ct, key, bnum):
        final = self.sbox(self.prevct[bnum] ^ key[bnum])
        self.prevct = ct
        return final
    
class AesOFB(cwa.AESLeakageHelper):
    def __init__(self):
        self.prevoutput = [0] * 16 # starts as IV value
    def leakage(self, pt, ct, key, bnum):
        final = self.sbox(self.prevoutput[bnum] ^ key[bnum])
        self.prevoutput = ct ^ pt
        return final

class AesCTR(cwa.AESLeakageHelper):
    def leakage(self, pt, ct, key, bnum):
        aa = ct[bnum] ^ pt[bnum]
        st9 = self.inv_sbox(aa ^ key[bnum])
        return st9
    def process_known_key(self, inpkey):
        return key_schedule_rounds(inpkey, 0, 10)

def get_leakage_model(model):
    if model == "ECB":
        return cwa.leakage_models.sbox_output

    if model == "CBC":
        return cwa.leakage_models.new_model(AesCBC)

    if model == "CFB":
        return cwa.leakage_models.new_model(AesCFB)

    if model == "OFB":
        return cwa.leakage_models.new_model(AesOFB)

    if model == "CTR":
        return cwa.leakage_models.new_model(AesCTR)

    return None