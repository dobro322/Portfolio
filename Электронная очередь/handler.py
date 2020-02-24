import mainServer as DB


# ###### #
# USERS
# ####### #


def new_user(data):
    answ = {}
    if 'faculty' not in data:
        answ["faculty"] = "Valid string required"
    if 'info' not in data:
        answ["info"] = "Valid string required"
    if answ:
        return answ
    return DB.addToOrder(data['faculty'], data['info'])


def move_user(data):
    answ = {}
    if 'operator_token' not in data:
        answ["operator_token"] = "Valid string required"
    if 'user_token' not in data:
        answ["user_token"] = "Valid string required"
    if 'new_faculty' not in data:
        answ["new_faculty"] = "Valid string required"
    if answ:
        return answ
    return DB.move_user(data['user_token'], data['new_faculty'])


def get_state(data):
    if 'token' not in data:
        return {'token': 'Valid string required'}
    return DB.getUser(data['token'])


def all_users(data):
    return list(DB.getUsers())


def delete_all_users(data):
    return DB.delete_all_users()


def update_info(data):
    answ = {}
    if 'token' not in data:
        answ["token"] = "Valid string required"
    if 'user' not in data:
        answ["user"] = "Valid string required"
    if answ:
        return answ
    return DB.editUser(data['token'], data['user'])


# ###### #
# OPERATOR
# ####### ##


def add_course(data):
    answ = {}
    if 'course' not in data:
        answ["course"] = "Valid string required"
    if 'faculty' not in data:
        answ["faculty"] = "Valid string required"
    if 'token' not in data:
        answ["token"] = "Valid string required"
    if answ:
        return answ
    return DB.add_course(data['token'], data['course'], data['faculty'])


def show_tv(data):
    faculties = []
    for faculty in data:
        faculties += [{'faculty': faculty, 'items': list(DB.get_faculty_users(faculty))}]
    return faculties


def clearCurrent(data):
    return DB.clearCurrent(data['token'])


def get_course(data):
    return DB.get_courses()


def call_user(data):
    answ = {}
    if 'token' not in data:
        answ["token"] = "Valid string required"
    else:
        if not DB.checkOperatorToken(data['token']):
            answ["token"] = "Valid string required"
    if 'faculty' not in data:
        answ["faculty"] = "Valid string required"
    if answ:
        return answ
    return DB.getFreeInOrder(data['faculty'], data['token'])


def delete_all_operators(data):
    return DB.delete_all_operators()


def show_operators(data):
    if 'fac' in data:
        return DB.getOperators(data['faculty'])
    else:
        return DB.getOperators()


def create_operator(data):
    answ = {}
    if 'faculty' not in data:
        answ["faculty"] = "Valid string required"
    if 'code' not in data:
        answ["code"] = "Valid string required"
    if 'number' not in data:
        answ["number"] = "Valid string required"
    if answ:
        return answ
    return DB.registerOperator(data['faculty'], data['number'], data['code'])
