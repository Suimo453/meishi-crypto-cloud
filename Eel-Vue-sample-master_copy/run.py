import eel
import searchencrypt
import json
import os
from cryptography.fernet import Fernet
# import searchencrypt.py as searchencrypt

# html/css/jsの入っているディレクトリを指定
eel.init('view', allowed_extensions=['.js', '.html', '.css'])



# JavaScriptから呼べるように関数を登録

def keygen():
    if os.path.isfile("key.json"):
        return
    
    ck = Fernet.generate_key()
    
    sk,pk  = searchencrypt.KeyPairGenerate()
    with open("key.json", "w") as f:
        json.dump({
            "sk":sk.decode("utf-8"),
            "pk":pk.decode("utf-8"),
            "ck":ck.decode("utf-8")
        },f)
        
def readkey():
    with open("key.json", "r") as f:
        key = json.load(f) 
        sk = key["sk"].encode()
        pk = key["pk"].encode()
        ck = key["ck"].encode()
    return sk, pk, ck


keygen()
sk,pk,ck = readkey()
fernet = Fernet(ck)

@eel.expose
def enctag(tag):
    return searchencrypt.PKES(tag, pk)

@eel.expose
def trap(tag):
    return searchencrypt.Trapdoor(sk, tag).decode("utf-8")
    
@eel.expose
def enc(plain):
    return fernet.encrypt(plain.encode("utf-8")).decode("utf-8")

@eel.expose
def dec(cipher):
    return fernet.decrypt(cipher.encode("utf-8")).decode("utf-8")

# 最初の画面のhtmlファイルを指定
eel.start('html/index.html', port=9000)
