#coding: utf-8

import MarchDB as MDB


def create_answer(data):
    if data['action'] == 'new':
        MDB.add_particapant(data['id'])
        return True

    if data['action'] == 'check':
        return MDB.is_exist(data['id'])

    if data['action'] == 'ticket':
        return MDB.get_ticket_number(data['id'])


def check_person(id):
    return MDB.is_exist(id)


def add_person(id):
    return MDB.add_particapant(id)


def get_number(id):
    return str(MDB.get_ticket(id))


def get_wish(number, id):
    if id == "96131590":
        return "Не забывай о том, насколько ты прекрасна"
    elif id == "192595550":
        return "С тобой я готов опаздывать на каждое метро"
    elif id == "45733510":
        return "ты самая грациозная лисичка"
    elif id == "51529557":
        return "Ты самая милая Кисонька в этом универе"
    elif id == "21766756":
        return "Платас - пидарас"
    elif id == "12085093":
        return "Если ты это видишь, то Лера увидит твое пожелание"
    elif id == "7562715":
        return "Твои посты самые лучшие"
    elif id == "77344803":
        return "Оставайся такой же милой и умной. Спасибо что ты есть в моей жизни. P.S. Жду делать лайки :)"
    else:
        count = MDB.wish_count()
        number = int(number) % int(count)
        number = number if number > 0 else int(count)
        return MDB.wish(number)


def check_key(key):
    print('check_key')
    return MDB.is_used(key)


def key_used(key):
    print('key_used')
    return MDB.set_used(key)
