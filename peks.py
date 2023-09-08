import hashlib
from bls12381 import ecp
from bls12381 import ecp2
from bls12381 import curve
from bls12381 import big
from bls12381.ecp import ECp
from bls12381.ecp2 import ECp2
from bls12381 import pair
from bls12381.fp12 import Fp12
from flask import Flask, request
app = Flask(__name__)


G2_TAB = []

def init():
    global G2_TAB
    G = ecp2.generator()
    if G.isinf():
        return False
    G2_TAB = pair.precomp(G)
    return True

def BLS_H(m):
    h = hashlib.shake_256()
    h.update(bytes(m, 'utf-8'))
    hm = big.from_bytes(h.digest(curve.EFS))
    HM = ECp()
    while not HM.set(hm):
        hm = hm + 1
    HM = curve.CurveCof * HM

    return HM


# 鍵ペア（秘密鍵SKと公開鍵PK）を生成する関数

def KeyPairGenerate():
    G = ecp2.generator()
    SK = big.rand(curve.r)
    PK = SK * G
    return (SK, PK)

# PEKS
def PKES(tag,PK):
    G = ecp2.generator()
    r = big.rand(curve.r)
    cipher_tag1 = r * G 
    h_tag = BLS_H(tag)
    h_r = r * PK

    cipher_tag2 = pair.ate(h_r,h_tag)
    cipher_tag2 = pair.fexp(cipher_tag2)
    return cipher_tag1,cipher_tag2

def Trapdoor(s,tag):
    h_tag = BLS_H(tag)
    trapdoor = s * h_tag
    return trapdoor

def Test(trapdoor,cipher_tag1,cipher_tag2):
    trap_tag = pair.ate(cipher_tag1,trapdoor)
    trap_tag = pair.fexp(trap_tag)
    return   trap_tag == cipher_tag2

init()
sk,pk  = KeyPairGenerate()
cipher_tag1,cipher_tag2 = PKES("atsu",pk)
trapdoor = Trapdoor(sk,"atsu")
result = Test(trapdoor,cipher_tag1,cipher_tag2)
print(result)

template = """
<p>Hello, {}!</p>
<form action='/hello' method='post'>
  <input name='name'></input>
  <input type='submit'></input>
</form>
"""

@app.route("/hello", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form["name"]
    else:
        name = "Taro"
    return template.format(name)

if __name__ == "__main__":
    # サーバ立ち上げ
    app.run(
        host="0.0.0.0",
        port=5000)