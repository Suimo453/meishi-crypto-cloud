import json
DB_FILE_NAME = "detabase.json"

class Meishi():
    def __init__(self,name,company,image,name_key,company_key):
        self.name = name
        self.company = company
        self.image = image
        self.name_key = name_key
        self.company_key = company_key

def select_all():
    with open(DB_FILE_NAME) as f:
        return json.load(f)

def save(detabase):
    with open(DB_FILE_NAME,"w") as f:
        return json.dump(detabase,f)

def add(meishi):
    detabase = select_all()
    detabase.append(meishi.__dict__)
    save(detabase)


if __name__ == "__main__":
    meishi1 = Meishi(company="kaisha",name="namae",image="aaaaaa",name_key="namaekagi",company_key="kaishakagi")
    meishi2 = Meishi(company="kaishaA",name="namaeA",image="aaaaaa",name_key="namaekagiA",company_key="kaishakagiA")
    add(meishi1)
    add(meishi2)
    print(select_all())