from flask import Flask, request
import models
from flask_cors import CORS
app = Flask(__name__)
CORS(
    app,
    supports_credentials=True
)

@app.route("/create", methods=['POST'])
def create():
    company = request.json["company"]
    name = request.json["name"]
    image = request.json["image"]
    name_key = request.json["encname"]
    company_key = request.json["enccompany"]
    
    meisi = models.Meishi(
        name=name,
        company=company,
        image=image,
        name_key=name_key,
        company_key=company_key
    )
    models.add(meisi)
    return "add"

@app.route("/search", methods=['POST'])
def search():
    company_key = request.json["company"]
    name_key = request.json["name"]
    print(name_key)
    
    result = []
    
    if name_key and company_key:
        print("both")
        meisi_list = models.select_by_name_and_company(name_key, company_key)
    elif name_key:
        print("namekey")
        meisi_list = models.select_by_name_key(name_key)
    elif company_key:
        print("companykey")
        meisi_list = models.select_by_company_key(company_key)
    else:
        print("else")
        meisi_list = []
        
    for meisi in meisi_list:
        result.append(meisi.to_dict())
    
    return result

if __name__ == "__main__":
    # サーバ立ち上げ
    app.run(
        host="0.0.0.0",
        port=5004)