from cryptography.fernet import Fernet
 
# 暗号化・復号化対象のメッセージ
data = "ここに平文を挿入".encode("utf-8")
 
# インスタンス生成
key = Fernet.generate_key()
f = Fernet(key)
 
# 暗号化されたデータ
token = f.encrypt(data)
print(token)
 
# 復号化されたデータ
data_decrypt = f.decrypt(token)
print(f.decrypt(token).decode("utf-8"))

