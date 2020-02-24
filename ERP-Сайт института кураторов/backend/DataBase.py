from pymongo import MongoClient
from uuid import uuid4
import requests
import json
import datetime
import time
import re
from random import randint

db = MongoClient("mongodb://xx:xx@45.67.57.64:27018/IK")
no_id = {"_id": 0}
db = db.IK
members_db = db.members
places_db = db.places
reserve_log = db.reserve_log
forms_db = db.forms
forms_log = db.forms_log


def get_empty_id(collection):
    req = collection.find({}, {"id": 1}).sort("id", -1).limit(1)
    data = list(req)
    if len(data) == 1:
        return data[0]['id'] + 1
    else:
        return 0


def currtime():
    return time.mktime(datetime.datetime.now().timetuple())


###
# Member
###


def add_member(data):
    answer = json.loads(
        requests.post(
            'https://api.vk.com/method/users.get?user_ids=%s&access_token=3&fields=photo_max_orig&v=5.101'
            % data["vk"]
        ).text
    )["response"][0]
    query = {
        "token": str(uuid4()),
        "personal_info": {
            "name": data["name"].strip(),
            "group": data["member_group"].replace(" ", "").upper(),
            "phone": data["phone"],
            "vk": answer["id"],
            "faculty": data["faculty"].replace(" ", ""),
            "pic": answer["photo_max_orig"],
        },
        "group_info": {
            "faculty": data["group_faculty"].replace(" ", ""),
            "group": data["group_name"].replace(" ", "").upper(),
            "chief_adapter": data["chief_adapter"]
        }
    }
    id_res = members_db.insert_one(query).inserted_id
    return members_db.find_one({"_id": id_res}, no_id)


def get_member(id=None, token=None):
    query = {"personal_info.vk": int(id)} if id else {"token": token}
    res = members_db.find_one(query, no_id)
    return res


def get_members(query={}):
    res = members_db.find(query, {"token": 0, "_id": 0})
    return list(res)


###
# Places
###

placecece = [
          {
            "id": 0,
            "name": "Холл Грифона",
            "description": "1 корпус  2 этаж (дальний от метро)",
            "photo": "https://sun9-2.userapi.com/c851424/v851424763/1ad69b/AbmQVTGFklo.jpg",
            "reservation_time": [],
          },
          {
            "id": 1,
            "name": "Холл Лисы",
            "description": "1 корпус 3 этаж (ближе к метро)",
            "photo": "https://sun9-64.userapi.com/c854020/v854020763/f9c7d/eiHnu6WVB98.jpg",
            "reservation_time": [],
          },
          {
            "id": 2,
            "name": "Холл Дракона",
            "description": "1 корпус 4 этаж (ближе к метро)",
            "photo": "https://sun9-71.userapi.com/c858332/v858332763/7e634/Xk0ee1WIu2o.jpg",
            "reservation_time": [],
          },
          {
            "id": 3,
            "name": "Холл Моржа",
            "description": "1 корпус 4 этаж (дальше от метро)",
            "photo": "https://sun9-44.userapi.com/c850528/v850528763/1c89bd/3c8sGrmrOJo.jpg",
            "reservation_time": [],
          },
          {
            "id": 4,
            "name": "Холл Собаки",
            "description": "1 корпус 6 этаж (дальний от метро)",
            "photo": "https://sun9-47.userapi.com/c855424/v855424763/f6254/E3M4XXDYbJk.jpg",
            "reservation_time": [],
          },
          {
            "id": 5,
            "name": "Холл Оленя",
            "description": "1 корпус 6 этаж (ближний к метро)",
            "photo": "https://sun9-59.userapi.com/c855128/v855128763/f3640/kJ-7ybs3-YU.jpg",
            "reservation_time": [],
          },
          {
            "id": 6,
            "name": "Холл Медведя",
            "description": "1 корпус 7 этаж (ближний к метро)",
            "photo": "https://sun9-54.userapi.com/c858028/v858028763/7a287/NgD_f6rSUv8.jpg",
            "reservation_time": [],
          },
          {
            "id": 7,
            "name": "Холл Филина",
            "description": "1 корпус 7 этаж (дальний от метро)",
            "photo": "https://sun9-19.userapi.com/c850324/v850324763/1dd87d/bfZdDLDgWtw.jpg",
            "reservation_time": [],
          },
          {
            "id": 8,
            "name": "Холл Калибри",
            "description": "2 корпус 4 этаж (комната отдыха)",
            "photo": "https://sun9-56.userapi.com/c850224/v850224747/1d0fec/2e4NP37BzuY.jpg",
            "reservation_time": [],
          },
          {
            "id": 9,
            "name": "Другое",
            "description": "",
            "photo": "",
            "reservation_time": [],
          }
        ]
def add_place(data):
    query = {
        "id": get_empty_id(places_db),
        "name": data["name"],
        "description": data["description"],
        "photo": data["photo"],
        "reservation_time": []
    }
    res_id = places_db.insert_one(query).inserted_id
    return places_db.find_one({"_id": res_id}, no_id)


def get_places(query={}):
    return list(places_db.find(query, no_id))


def add_reservation(data, member):
    query = {
        "id": data["id"]
    }
    new_reservation = {
        "time_start": data["time_start"],
        "time_end": data["time_end"],
        "reserved_by": {
          "name": member["personal_info"]["name"],
          "id": member["personal_info"]["vk"],
          "group": member["group_info"]["group"]
        },
        "aborted": False
    }

    if not data["type"] == "university":
        new_reservation["type"] = data["type"]

    places_db.update_one(query, {"$push": {"reservation_time": new_reservation}})
    return places_db.find_one(query, no_id)


def update_reservation(query, chgangings):
    return places_db.update(query, chgangings, multi=True)


def normalizer(number = '+7 (999) 999-99-99'):
    for a in ['(', ')' , '-', ' ']:
        number = number.replace(a, '')
    numb_arr = ['+7 ','(' , '', '', ') ' , '' , '' , '-' , '' , '-', '']
    for x in range(10, 0, -1):
        number, result = number[:-1], number[-1]
        numb_arr[x] += str(result)
    return ''.join(numb_arr)


if __name__ == "__main__":
    # members_db.delete_many({})
    import csv
    arr = []
    keys = ["date","name","vk","phone","faculty","member_group","group_faculty","group_name"]
    with open('data.csv', "r", encoding = "utf-8") as fin:
        reader = csv.reader(fin)
        for row in reader:
            dictionary = dict(zip(keys, row))
            dictionary["chief_adapter"] = False
            dictionary["vk"] = re.sub(r"(https://)?(www.)?(m.)?vk.com/", "", dictionary["vk"], flags = re.I)
            dictionary["phone"] = normalizer(dictionary["phone"])
            arr += dictionary
            try:
                add_member(dictionary)
                print(dictionary["name"], " added")
            except Exception as e:
                print(e, dictionary["name"])

    # members_db.update_many({},{"$set":{"role": 1}})
    # # places_db.delete_many({})
    # for place in placecece:
    #     add_place(place)


###
# Forms
###


def add_form(data):
    query = {
        "id": get_empty_id(forms_db),
        "name": data["name"],
        "description": data["description"],
        "enabled": False,
        "questions": data["questions"],
        "answers": [],
        "date_added": currtime()
    }
    res = forms_db.insert_one(query).inserted_id
    return forms_db.find_one({"_id": res}, no_id)


def get_forms(query={}, filter={"_id": 0}):
    res = forms_db.find(query, filter)
    return list(res)


def get_form(query={}, filter={"_id": 0}):
    res = forms_db.find_one(query, filter)
    return res


def update_form(query, chgangings):
    forms_db.update_one(query, chgangings)
    return forms_db.find_one(query, no_id)


def delete_form(query):
    res = forms_db.find_one(query)
    forms_db.delete_one({"_id": res["_id"]})
    return res
