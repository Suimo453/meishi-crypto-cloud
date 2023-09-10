import json

from peks import Test
DB_FILE_NAME = "detabase.json"

class Meishi():
    def __init__(self,name,company,image,name_key,company_key):
        self.name = name
        self.company = company
        self.image = image
        self.name_key = name_key
        self.company_key = company_key
    
    def to_dict(self):
        return self.__dict__

    def from_dict(d):
        self = Meishi("", "", "", "", "")
        self.__dict__ = d
        return self
    
    def __str__(self):
        return f'''=== Meishi ===
name = {self.name}
company = {self.company}
image = omit
name_key = {self.name_key}
company_key = {self.company_key}
'''

def select_all():
    with open(DB_FILE_NAME) as f:
        return json.load(f)

def save(detabase):
    with open(DB_FILE_NAME,"w") as f:
        return json.dump(detabase,f)

    ## 名刺の追加

def add(meishi):
    detabase = select_all()
    detabase.append(meishi.to_dict())
    save(detabase)

    ## 名刺の検索

def select_by_name_key(name_trapdoor):
    detabase = select_all()
    result = []
    for line in detabase:
        meishi = Meishi.from_dict(line)

        if Test(name_trapdoor, meishi.name_key):
            result.append(meishi)

    return result

def select_by_company_key(company_trapdoor):
    detabase = select_all()
    result = []
    for line in detabase:
        meishi = Meishi.from_dict(line)

        if Test(company_trapdoor, meishi.company_key):
            result.append(meishi)

    return result

def select(name_trapdoor,company_trapdoor):
    detabase = select_all()
    result = []
    for line in detabase:
        meishi = Meishi.from_dict(line)

        if Test(name_trapdoor, meishi.name_key) and Test(company_trapdoor, meishi.company_key):
            result.append(meishi)

    return result

    ## 試作用追加部分
if __name__ == "__main__":
    meishi1 = Meishi(company="kaisha",name="namae",image="aaaaaa",name_key="nama.ekagi",company_key="kai.shakagi")
    meishi2 = Meishi(company="kaishaA",name="namaeA",image="aaaaaa",name_key="nama.ekagiA",company_key="kai..shakagiA")
    add(meishi1)
    add(meishi2)
    ## print(select_all())

    meishi = select_by_name_key(name_key = "namaekagi")
    meishi = select_by_company_key(company_key = "namaekagi")
    print(meishi[0])
    
