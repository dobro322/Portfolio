from pymongo import MongoClient
from uuid import uuid4

db = MongoClient('xxx', 27017).education
groups = db.groups
allgr = db.allgr
answers = db.answers


def new_answer(data):
    query = {
        'group': data['group'],
        'common': data['common'],
        'first': data['first'],
        'second': data['second'],
        'choise': data['choice'],
        'user': data['user'],
        'token': str(uuid4())
    }
    res = answers.insert_one(query).inserted_id
    return answers.find_one({"_id": res}, {"_id": 0})


def new_allgroup(data):
    if not allgr.find_one({'name': data['name'].upper()}):
        query = {
            'name': data['name'].upper(),
            'faculty': data['faculty'],
            'course': data['course'],
            'articles': {'first': [], 'second': []}
        }
        res = allgr.insert_one(query).inserted_id
        return allgr.find_one({'_id': res}, {'_id': 0})
    else:
        return 'yiss'


def new_group(data):
    if not groups.find_one({'name': data['name'].upper()}):
        query = {
            'name': data['name'].upper(),
            'faculty': data['faculty'],
            'course': data['course'],
            'articles': {'first': [], 'second': []}
        }
        res = groups.insert_one(query).inserted_id
        return groups.find_one({'_id': res}, {'_id': 0})
    else:
        return groups.find_one({'name': data['name'].upper()}, {'_id': 0})


def update_group(data):
    filter = {'name': data['name'].upper()}
    query = {'articles': data['articles']}
    groups.update_one(filter, {'$set': query})
    return groups.find_one(filter, {'_id': 0})


def get_group(data):
    filter = {'name': data['name'].upper()}
    return groups.find_one(filter, {'_id': 0})


def all_groups(data):
    filter = {}
    answ = []
    res = list(groups.find(filter, {'_id': 0}))
    for r in res:
        for id, temp in enumerate(r['articles']['first']):
            r['articles']['first'][id] = True
        for id, temp in enumerate(r['articles']['second']):
            r['articles']['second'][id] = True
        answ += [r]
    return answ


def groups_only(data):
    filter = {}
    res = list(groups.find(filter, {"name": 1, "faculty": 1, "_id": 0}))
    return res
