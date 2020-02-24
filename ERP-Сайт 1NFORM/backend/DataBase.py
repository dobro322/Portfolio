from pymongo import MongoClient
from uuid import uuid4
import requests
import json
import datetime
import time
import re
from random import randint

db = MongoClient("mongodb://xx:xx@123:27018/inform")
old = db.school.user
db = db.inform
inform_users = db.users
inform_kanbans = db.kanbans
inform_tables = db.tables
inform_quests = db.quests
inform_shop = db.shop
inform_abits = db.abiturients
inform_conversations = db.messages
inform_messages = db.messages_data
inform_invited_storage = db.invited_storage
inform_tickets = db.tickets
no_id = {"_id": 0}


# for t in inform_abits.find({"status.date_taken": {"$lt": 1566950400}, "status.name": "2"}):
#     print(t['full_name'])
#     inform_abits.update_one({'_id': t['_id']}, {"$set": {"status.name": "3"}})



def get_empty_id(collection):
    req = collection.find({}, {"id": 1}).sort("id", -1).limit(1)
    data = list(req)
    if len(data) == 1:
        return data[0]['id']
    else:
        return 0


def currtime():
    return time.mktime(datetime.datetime.now().timetuple())

"""
Организаторы проекта
"""


def add_user(data):
    query = {
        'role': '204',
        'token': str(uuid4()),
        'info': {
            'name': data['name'],
            'faculty': data['faculty'],
            'phone': data['phone'],
            'vk': data['vk'],
            'pic': json.loads(
                requests.post(
                    'https://api.vk.com/method/users.get?user_ids=%s&access_token=xxx&fields=photo_max_orig&v=5.101'
                    % data['vk']
                ).text
            )['response'][0]["photo_max_orig"],
        },
        'reprimands': [],
        'score': {
            'abtx': {
                'amount': 0,
            },
            'surf': [],
            'messages': []
        },
        'news': [],
        'quests': [],
        'departments': [],
        'settings': {
            'menu_pic': ''
        }
    }
    inform_users.insert_one(query)
    return query


# if __name__ == "__main__":
#     inform_users.delete_many({})
#     for user in old.find({"deps.passed": True}):
#         add_user({
#             "name": user["name"],
#             "faculty": user["faculty"],
#             "phone": user["phone"],
#             "vk": user["vk"]
#         })


def add_surf_counter(user, faculty):
    query = {
        "info.vk": int(user['info']['vk'])
    }
    if faculty in [x['faculty'] for x in user['score']['surf']]:
        query['score.surf.faculty'] = faculty
        changings = {
            "$inc": {"score.surf.$.amount": 1}
        }
    else:
        changings = {
            "$push": {
                "score.surf": {
                    "faculty": faculty,
                    "amount": 1
                }
            }
        }
    inform_users.update_one(query, changings)
    return inform_users.find_one(query, {"score": 1, "_id": 0})


def delete_user(id):
    inform_users.delete_one({"info.vk": id})
    return {"Msg": "Succesfully deleted " + str(id)}


def read_notification(token, id):
    query = {
        "token": token,
        "news.id": id
    }
    changings = {
        "$set": {"news.$.readed": True}
    }
    inform_users.update_one(query, changings)
    return inform_users.find_one({"token": token}, {"_id": 0, "news": 1})


def add_score(member, score):
    query = {
        "info.vk": member["info"]["vk"]
    }
    changings = {
        "$inc": {"score.abtx.amount": score}
    }
    inform_users.update_one(query, changings)
    return inform_users.find_one(query, no_id)


def add_user_message(member, conversation, text):
    query = {
        "info.vk": int(member['info']['vk'])
    }
    if len(member["score"]["messages"]) > 0:
        for conf in member["score"]["messages"]:
            if conf['title'] == conversation['title']:
                conf['amount'] += 1
                conf['words'] += len(text.split(' '))
            else:
                member['score']['messages'].append(
                    {
                        "title": conversation["title"],
                        "amount": 1,
                        "words": len(text.split(' '))
                    })
            changings = {
                "$set": {"score.messages": member["score"]["messages"]}
            }
            inform_users.update_one(query, changings)
            return inform_abits.find_one(query, no_id)
    else:
        member['score']['messages'] = [
            {
                "title": conversation["title"],
                "amount": 1,
                "words": len(text.split(' '))
            }
        ]
    changings = {
        "$set": {"score.messages": member["score"]["messages"]}
    }
    inform_users.update_one(query, changings)
    return inform_abits.find_one(query, no_id)


def get_member(filter, id):
    filter = {key: 1 for key in filter.split(',')}
    filter['_id'] = 0
    return inform_users.find_one({"info.vk": int(id)}, filter)


def add_news(data, id):
    member = get_member('info,news', id)
    query = {
        "info.vk": member['info']['vk']
    }
    if len(member['news']) > 0:
        tid = member['news'][-1]['id'] + 1
    else:
        tid = 0
    changings = {
        "$push": {
            "news": {
                'id': tid,
                'date': currtime(),
                'title': data['title'],
                'text': data['text'],
                'readed': False,
                'type': data['type'] if 'type' in data else 'everyone'
            }
        }
    }

    inform_users.update_one(query, changings)
    inform_users.find_one(query)
    return inform_users.find_one(query, {"news": 1, "_id": 0})


def check_member(filter, token):
    filter = {key: 1 for key in filter.split(',')}
    filter['_id'] = 0
    return inform_users.find_one({"token": token}, filter)


def get_self(filter, id):
    filter = {key: 1 for key in filter.split(',')}
    filter['_id'] = 0
    return inform_users.find_one({"token": id}, filter)


def get_team(filter):
    filter = {key: 1 for key in filter.split(',')}
    filter['_id'] = 0
    return list(inform_users.find({}, filter))


def edit_user(id, data):
    query = {
        "info.vk": int(id)
    }
    inform_users.update_one(query, {"$set": data})
    return inform_users.find_one(query, no_id)


def users_from_dep(dep, filter):
    query = {}
    if not dep == 'Все':
        query = {
            'departments': dep
        }
    filter = {key: 1 for key in filter.split(',')}
    filter['_id'] = 0
    answer = list(inform_users.find(query, filter))
    return answer

"""
Канбан-доска
"""


def add_task(task, member):
    query = {
        'id': get_empty_id(inform_kanbans) + 1,
        'title': task['title'],
        'description': task['description'],
        'deadline': task['deadline'],
        'department': task['department'],
        'type': task['type'],
        'responsibles': task['responsibles'],
        'author': {
            'vk': member['info']['vk'],
            'name': member['info']['name'],
            'created': currtime()
        },
        'comments': []
    }
    id = inform_kanbans.insert_one(query).inserted_id
    return inform_kanbans.find_one({"_id": id}, no_id)


def get_tasks(dep):
    query = {
        'department': dep
    }
    answer = list(inform_kanbans.find(query, no_id))
    return answer


def get_task(id):
    answer = inform_kanbans.find_one({"id": int(id)}, no_id)
    return answer


def delete_task(id):
    query = {
        'id': int(id)
    }
    inform_kanbans.delete_one(query)
    return {"msg": "Deleted id%s" % id}


def change_task(data, id):
    query = {
        'id': int(id)
    }
    changings = data
    inform_kanbans.update_one(query, {"$set": changings})
    return inform_kanbans.find_one(query, no_id)


def add_task_comment(comment, id, member):
    query = {
        'id': int(id)
    }
    changings = {
        "$push": {
            "comments": {
                "author": member['info']['name'],
                "text": comment,
                "pic": member['info']['pic'],
                "date": currtime()
            },
        }
    }
    inform_kanbans.update_one(query, changings)
    return inform_kanbans.find_one(query, no_id)


def get_member_deps(token):
    deps = check_member('departments', token)['departments']
    return deps


"""
Таблицы отделов
"""


def get_table(dep):
    query = {
        'department': dep
    }
    answer = list(inform_tables.find(query, no_id))
    return answer


def get_table_row(id):
    query = {
        'id': int(id)
    }
    answer = inform_tables.find_one(query, no_id)
    return answer


def add_table_row(data):
    query = {
        'id': get_empty_id(inform_tables) + 1,
        'department': data['department'],
        'data': data['data']
    }
    id = inform_tables.insert_one(query).inserted_id
    return inform_tables.find_one({"_id": id}, no_id)


def change_table(data, id):
    query = {
        'id': int(id)
    }
    id = inform_tables.update_one(query, {"$set": {"data": data}})
    return inform_tables.find_one(query, no_id)


def delete_table(id):
    query = {
        'id': int(id)
    }
    inform_tables.delete_one(query)
    return {"msg": "Deleted id%s" % id}


"""
Квесты
"""
quests = {
    'id': 1,
    'title': 'Title',
    'text': 'Description',
    'img': 'pic',
    'daily': False,
    'date': 'exp date',
    'audience': {
        'faculties': ['ИСиТ', 'ИКСС'],
        'department': ['Серфинг', 'Собеседники']
    },
    'counting': {
        'count': 5,
        'function': 'somefunction',
        'additional': {
            'faculty': 'ИСиТ'
        }
    }
}


def create_quest(data):
    date = datetime.datetime.strptime(data['date_exp'],  '%Y-%m-%d')
    data['date_exp'] = time.mktime(date.timetuple())
    try:
        query = {
            'id': get_empty_id(inform_quests) + 1,
            'title': data['title'],
            'text': data['comment'],
            'pic': data['pic'],
            'daily': data['daily'],
            'date': data['date_exp'],
            'audience': data['audience'],
            'counting': data['counting'],
            'cost': int(data['cost'])
        }
    except Exception as e:
        return {"Msg": "Missed arg " + str(e)}
    result = inform_quests.insert_one(query).inserted_id
    return inform_quests.find_one({"_id": result}, no_id)


def get_quests(data):
    query = {
        "$or": [
            {'audience.faculties': data['faculty']},
            {'audience.departments': {"$in": data['departments'].split(',')}}
        ]
    }
    result = list(inform_quests.find(query, no_id))
    return result


data = {
    'title': "Олды тут?",
    'text': "Найти 5 человек со своего факультета",
    'img': {
      'top': 100,
      'left': 0,
      'size': 600,
      'pic': "https://pp.userapi.com/c855136/v855136032/8adb8/P962KT2H-1M.jpg",
    },
    'audience': {
        'faculty': None,
        'departments': ['Фильтрация']
    },
    'daily': True,
    'counting': {
        'count': 5,
        'function': 'somefunction',
        'additional': {
            'faculty': 'ИСиТ',
        }
    },
    'date': currtime(),
    'cost': 100
}


"""
Магазин
"""


def add_slot(data):
    query = {
        "id": get_empty_id(inform_shop) + 1,
        "title": data["title"],
        "text": data["text"],
        "img": data["img"],
        "price": data["price"]
    }
    result = inform_shop.insert_one(query).inserted_id
    return inform_shop.find_one({"_id": result}, no_id)


def get_shop():
    result = inform_shop.find({}, {"cost": 0, "_id": 0})
    return list(result)


"""
Абитуриенты
"""


def reset():
    inform_abits.delete_many({})
    inform_users.update_many({}, {
        "$set": {
            "score": {
                'abtx': {
                    'amount': 0,
                },
                'surf': [],
                'messages': []
            },
            "news": [],
            "quests": []
        }
    })


def add_abit(data):
    try:
        query = {
            "id": get_empty_id(inform_abits) + 1,
            "full_name": data["full_name"],
            "studying_form": data["form"],
            "faculty": data["faculty"],
            "specialization": data["specialization"],
            "school": "",
            "bdate": "",
            "hometown": "",
            "respublic": "",
            "year_grad": "",
            "comments": [],
            "added_conf": False,
            "pic": "",
            "messages": [],
            "vk": "",
            "status": {
                "name": "1",
                "taken_by": "",
                "date_taken": "",
                "found_by": "",
                "date_found": ""
            },
            "predictings": []
        }
    except Exception as e:
        return {"Msg": "Missed argument: " + str(e)}
    answer = inform_abits.insert_one(query).inserted_id
    return inform_abits.find_one({"_id": answer}, no_id)


# abit = {
#     "full_name": "Чалов Чингизхан Алматович",
#     "form": "Очное",
#     "faculty": "ИКСС",
#     "specialization": "10.03.01"
# }
# add_abit(abit)


def drop_abit(id):
    query = {
        "id": int(id)
    }
    status = "2"
    abit_status = inform_abits.find_one(query)['status']

    if not abit_status['found_by']['id'] == abit_status['taken_by']['id']:
        status = "3"

    changings = {
        "$set": {
            "status.found_by": "",
            "status.date_found": "",
            "status.name": status,
            "vk": "",
            "pic": ""
        }
    }
    inform_abits.update_one(query, changings)
    return inform_abits.find_one(query, no_id)

# faculties = ["ИКСС","ИСиТ","РТС","ВУЦ","ГФ","ЦЭУБИ","ФП","ИНО","СПбКТ"]
# for x in range(0, 90):
#     add_abit({
#         'full_name': "Ковальчук Владислав Андреевич",
#         'form': "Очная",
#         "faculty": faculties[randint(0, 8)],
#         "specialization": "09.03.02"
#     })


def change_abit(data, id):
    query = {
        "id": int(id)
    }
    changings = {
        "$set": data
    }
    inform_abits.update_one(query, changings)
    return inform_abits.find_one(query, no_id)


def delete_comment(data, id):
    query = {
        "id": int(id)
    }
    inform_abits.update_one(query, data)
    return inform_abits.find_one(query, no_id)


def fail_predict(abit, predict_vk):
    query = {
        "id": int(abit["id"]),
        "predictings.id": int(predict_vk)
    }
    changings = {
        "$set": {
            "predictings.$.failed": True
        }
    }
    inform_abits.update_one(query, changings)
    abit = inform_abits.find_one({"id": abit["id"]}, no_id)
    return abit


def add_abit_message(abit, conversation, text):
    query = {
        "vk": int(abit['vk'])
    }
    if len(abit["messages"]) > 0:
        for conf in abit["messages"]:
            if conf['title'] == conversation['title']:
                conf['amount'] += 1
                conf['words'] += len(text.split(' '))
    else:
        abit['messages'] = [
            {
                "title": conversation["title"],
                "amount": 1,
                "words": len(text.split(' '))
            }
        ]
    changings = {
        "$set": {"messages": abit["messages"]}
    }
    inform_abits.update_one(query, changings)
    return inform_abits.find_one(query, no_id)


def get_abit(id, filter):
    query = {
        "id": int(id)
    }
    filter = {key: 1 for key in filter.split(',')}
    filter['_id'] = 0
    return inform_abits.find_one(query, filter)


def get_abits(filter, fields, limit, vk):
    query = {}
    if not filter['search']:
        if not filter['faculties'] == 'Все':
            query["faculty"] = filter['faculties']

        if not filter['status'] == 'Все':
            query["status.name"] = filter["status"]
        if filter["personal"] == 'true':
            query["$or"] = [{"status.found_by.id": vk}, {"status.taken_by.id": vk}]

    else:
        query = {
            "full_name": {"$regex": filter['search']}
        }

    fields = {key: 1 for key in fields.split(',')}
    fields['_id'] = 0
    answ = inform_abits.find(query, fields)
    max = answ.count()
    founded = 0
    answ = list(answ)
    for r in answ:
        if r['status']['name'] == '4':
            founded += 1

    limit = answ[:int(limit)]
    return {"data": limit, 'max': max, 'founded': founded}


def take_abit(abit, member):
    abit_query = {
        "status.name": "2",
        "status.taken_by.id": member["info"]["vk"]
    }
    count = inform_abits.find(abit_query).count()
    if count >= 8:
        return get_abit(abit['id'], 'status')
    query = {
        "id": int(abit['id'])
    }
    changings = {
        "$set": {
            "status.name": "2",
            "status.taken_by": {
                "name": member['info']['name'],
                "id": member['info']['vk']
            },
            "status.date_taken": currtime()
        }
    }
    inform_abits.update_one(query, changings)
    return get_abit(abit['id'], 'status')


def get_abit_by_vk(vk):
    query = {
        "vk": int(vk)
    }
    return inform_abits.find_one(query, no_id)


def hard_abit(abit, member):
    query = {
        "id": int(abit['id'])
    }
    changings = {
        "$set": {
            "status.name": "3",
        }
    }
    inform_abits.update_one(query, changings)
    return get_abit(abit['id'], 'status')


def conf_abit(abit, member):
    query = {
        "id": int(abit['id'])
    }
    changings = {
        "$set": {
            "status.adding_by": {
                "name": member['info']['name'],
                "id": member['info']['vk'],
                "date": currtime()
            }
        }
    }
    inform_abits.update_one(query, changings)
    return get_abit(abit['id'], 'status')


def get_surfing_history(id):
    query = {
        "status.found_by.id": id
    }
    filter = {
        "id": 1,
        "status.date_found": 1,
        "_id": 0
    }
    result = inform_abits.find(query, filter)
    return list(result)


def confirm_abit(abit, vk, member, type):
    query = {
        "id": int(abit['id'])
    }
    vk = re.sub(r"(https?://)?(m.)?vk.com/", "", str(vk))
    vk = int(json.loads(
        requests.post(
            'https://api.vk.com/method/users.get?user_ids=%s&access_token=xxx&v=5.101'
            % vk
        ).text)['response'][0]["id"]),
    maybe = inform_invited_storage.find_one({"vk": vk[0]})
    changings = {
        "$set": {
            "status.name": "4",
            "added_conf": True if maybe else False,
            "status.found_by": {
                "name": member['info']['name'],
                "id": member['info']['vk']
            },
            "status.date_found": currtime(),
            "vk": vk[0],
            "pic": json.loads(
                requests.post(
                    'https://api.vk.com/method/users.get?user_ids=%s&access_token=xxx&fields=photo_max_orig&v=5.101'
                    % vk
                ).text
            )['response'][0]["photo_max_orig"]
        }
    }

    for pred in abit['predictings']:
        if pred['id'] == vk[0]:
            if type == 'self':
                add_news({"title": "Наказание","text": "Вы самостоятельно подтвердили '%s', который был в системе. С вас были сняты баллы" % abit['full_name'],"type":"personal"},member['info']['vk'])
                add_score(member, -12)
            tquery = {
                "id": int(abit['id']),
                "predictings.id": pred['id']
            }
            tchangings = {
                "$set": {
                    "predictings.$.correct": True
                }
            }
            inform_abits.update_one(tquery, tchangings)

    inform_abits.update_one(query, changings)
    return get_abit(abit['id'], 'status,vk,pic')


def comment_abit(abit, comment, member):
    query = {
        "id": int(abit['id'])
    }
    changings = {
        "$push": {
            "comments": {
                "author": member['info']['name'],
                "text": comment,
                "pic": member['info']['pic'],
                "date": currtime()
            },
        }
    }
    inform_abits.update_one(query, changings)
    return get_abit(abit['id'], 'comments')


"""
Сообщения
"""

conversation = {
    "peer_id": "some peer_id",
    "title": "conversation title",
    "faculty": "ИСиТ",
    "messages": [
        {
            "date": currtime(),
            "author": "author from_id",
            "text": "author text",
            "attachments": "author attachments",
        }
    ]
}


def add_conversation(data):
    query = {
        "id": get_empty_id(inform_conversations) + 1,
        "peer_id": data['peer_id'],
        "title": data['title'],
        "faculty": data['faculty'],
        "messages": []
    }
    result = inform_conversations.insert_one(query).inserted_id
    return inform_conversations.find_one({"_id": result}, no_id)


def find_conversation(peer_id):
    query = {
        "peer_id": peer_id
    }
    return inform_conversations.find_one(query, no_id)


def added_abit(id):
    query = {
        "vk": int(id)
    }
    changings = {
        "$set": {
            "added_conf": True
        }
    }
    inform_abits.find_one(query)
    inform_abits.update_one(query, changings)
    return inform_abits.find_one(query, no_id)


def add_chat_invite_storage(abit):
    query = {
        "vk": int(abit)
    }
    result = inform_invited_storage.insert_one(query).inserted_id
    return inform_invited_storage.find_one({"_id": result}, no_id)


def check_invite_storage(abit):
    query = {
        "vk": int(id)
    }
    return inform_invited_storage.find_one(query, no_id)


def get_message_history(id):
    query = {
        "author": id
    }
    result = inform_messages.find(query, no_id)
    return list(result)


def add_message(data, conversation):
    query = {
        "peer_id": int(conversation["peer_id"]),
        "date": currtime(),
        "author": data["from_id"],
        "text": data["text"],
        "attachments": data["attachments"]
    }
    result = inform_messages.insert_one(query).inserted_id
    return inform_messages.find_one({"_id": result}, {"_id": 0})


"""
Tickets
"""


def add_ticket(data):
    query = {
        'id': get_empty_id(inform_tickets) + 1,
        'vk': int(data['vk']),
        'name': data['name'],
        'faculty': data['faculty'],
        'pic': data['pic'],
        'date': currtime()
    }
    res = inform_tickets.insert_one(query).inserted_id
    return inform_tickets.find_one({"_id": res}, {"_id": 0})


def check_ticket(user_id, member_name):
    query = {
        "$set": {
            "arrived": {
                "date": currtime(),
                "checked_by": member_name,
                "state": True
            }
        }
    }
    filter = {
        "id": int(user_id)
    }
    inform_tickets.update_one(filter, query)
    return inform_tickets.find_one(filter, no_id)


# inform_tickets.update_many({},{"$set": {"arrived": {
#     "date": None,
#     "checked_by": None,
#     "state": False
# }}})
