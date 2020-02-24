import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId

# in_order - в очереди
# busy - на приеме
# canceled - отменил
# passed - закончил прием

import uuid

client = MongoClient('mongodb://xx:xx@134.0.116.69:27017')

db = client.ochered


secret_key = "xxx"

# ###### #
# Faculties
# ####### #


courses = db.Courses


def add_course(token, course, fac):
    if token == secret_key:
        courses.insert_one(
            {
                "name": course,
                "faculty": fac
            }
        )
        return courses.find_one({"name": course},{"_id": 0})
    return None


def get_courses():
    return list(courses.find({}, {"_id": 0}))


# ###### #
# USERS
# ####### #

users = db.users


def addToOrder(fac,  info):
    nowday = datetime.datetime.utcnow()
    user = {
        # "_id": DBSide
        "order": users.find({
            "date": {
                "$gt": datetime.datetime(
                    nowday.year,
                    nowday.month,
                    nowday.day,
                    0, 0, 0, 0
                )
            },
            "faculty": fac
        }).count() + 1,
        "status": 'in_order',
        "operator": None,
        "faculty": fac,
        "date": nowday,
        "info": info,  # {vk, phone etc.}
        "token": str(uuid.uuid4())
    }
    post_id = users.insert_one(user).inserted_id
    return users.find_one({"_id": ObjectId(post_id)}, {'_id': 0})


def checkUserToken(token):
    query = {"token": token}
    res_users = users.find_one(query)
    return True if res_users else False


def editUser(token, dict):
    query = {"token": token}
    dist = {"$set": dict}
    users.update_one(query, dist)
    return users.find_one(query)


def getInOrder(fac):
    query = {"faculty": fac, "status": "in_order"}
    res_users = users.find(query, {'_id': 0}).sort([("date", 1)])
    return res_users


def getUser(token):
    query = {"token": token}
    user = users.find_one(query, {'_id': 0})
    order_users = list(getInOrder(user['faculty']))
    prev = 0
    if order_users:
        prev = user['order'] - order_users[0]['order']
    return {'user': user, 'prev': prev}


def get_faculty_users(faculty):
    query = {"faculty": faculty, "$or": [{"status": "in_order"}, {"status": "busy"}]}
    res_users = users.find(query, {"_id": 0}).sort("order", 1)
    return res_users


def getUsers():
    return users.find({}, {'_id': 0})


def delete_all_users():
    users.delete_many({})
    return 'Succes'


def move_user(token, faculty):
    nowday = datetime.datetime.utcnow()
    users.update_one({"token": token}, {"$set": {
        "order": users.find({
            "date": {
                "$gt": datetime.datetime(
                    nowday.year,
                    nowday.month,
                    nowday.day,
                    0, 0, 0, 0
                )
            },
            "faculty": faculty
        }).count() + 1,
        "faculty": faculty,
        "status": "in_order",
        "operator": None
    }})
    return users.find_one({"token": token}, {"_id": 0})


# delete_all_users()


# ###### #
# ПУНКТ ПРИЕМА
# ####### #

operators = db.operators


def registerOperator(fac, number, code):
    operator = {
        # "_id": DBSide
        "number": number,
        "code": code,
        "faculty": fac,
        "token": str(uuid.uuid4()),
        "current": None,
        "online": False
    }
    post_id = operators.insert_one(operator).inserted_id
    return operators.find_one({"_id": ObjectId(post_id)}, {"_id": 0})


# def changeOperatorStatus(token):
#     operator
#     operators.update_one({"token": token},{""})


def getOperators(fac=None):
    if not fac:
        return list(operators.find({}, {'_id': 0}))
    else:
        return list(operators.find({'faculty': fac}, {'_id': 0}))


def delete_all_operators():
    operators.delete_many({})
    return 'Succes'


def checkOperatorToken(token):
    query = {"token": token}
    res_operators = operators.find_one(query)
    return True if res_operators else False


def clearCurrent(token):
    res_operator = operators.find_one({"token": token})
    if res_operator['current']:
        users.update_one({"token": res_operator["current"]}, {"$set": {"status": "passed", 'operator': None}})
        operators.update_one({'token': token}, {"$set": {"current": None}})
        return users.find_one({"token": res_operator["current"]}, {"_id": 0})
    return {}


def getFreeInOrder(fac, token):
    res_operator = operators.find_one({"token": token})
    current_user = clearCurrent(token)
    res_users = list(getInOrder(fac))
    if res_users:
        users.update_one({'token': res_users[0]['token']}, {"$set": {'status': 'busy', 'operator': res_operator['number']}})
        operators.update_one({'token': token}, {"$set": {"current": res_users[0]['token']}})
        res_users = users.find_one({"token": res_users[0]['token']}, {"_id": 0})
    return [current_user, res_users]


def delete_all():
    operators.delete_many({})
    users.delete_many({})


# delete_all()
