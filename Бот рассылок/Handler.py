import Vk
import DataBase as DB
from KeyBoard import KeyBoard, Button
import json



def create_mailing(data):
    users = DB.Users(data["sub_id"]).get()
    for user in users:
        status = "Success"
        try:
            Vk.send_message(
                user[0],
                data["message"],
                post = data["attachment"]
            )
        except Exception as e:
            status = str(e)

        DB.Mail().add(
            user[0],
            data["sub_id"],
            data["message"],
            data["attachment"],
            data["author_id"],
            status
        )
    return status


def get_sub(data, group_id):
    subs = DB.Subscriptions(group_id).get()
    data["text"] = data["text"].lower()
    for sub in subs:
        kw = sub[2]
        if kw in data["text"]:
            return sub
    return None


def create_auto_mailing(data, group_id):
    comm = DB.Community().get(group_id)
    res = get_sub(data, group_id)
    if not res:
        return None
    users = DB.Users(res[0]).get()
    for user in users:
        status = "Success"
        try:
            Vk.send_message(
                user[0],
                message=res[3],
                post="wall{}_{}".format(data["owner_id"], data["id"]),
                token=comm["token"]
            )
        except Exception as e:
            status = str(e)

        DB.Mail().add(
            user[0],
            res[0],
            res[3],
            "wall{}_{}".format(data["owner_id"], data["id"]),
            "auto",
            status
        )
    return status


def get_sub_kb(user_id, group_id):
    user_subs = DB.User_subscription().get(user_id, group_id)

    KB = KeyBoard(2, True)
    for sub in user_subs:
        BT = Button(
            sub[1],
            sub[0],
            "True" if sub[5] else "False",
            "green" if sub[5] else "white"
        )
        KB.add(BT)
    return KB.get()


def get_community(data):
    community = DB.Community().get(data["group_id"])
    return community


def start_answer(data, group_id):
    try:
        DB.User(data["from_id"]).add()
    except:
        print("Exist")
    community = get_community({"group_id": group_id})
    sub_kb = get_sub_kb(data["from_id"], group_id)
    Vk.send_message(
        data["from_id"],
        community["token"],
        message="Подписки группы",
        keyboard=sub_kb
    )


def create_answer(data, group_id):
    DB.Message().add(
        data["text"],
        data["attachment"] if "attachment" in data else "Empty",
        data["payload"] if "payload" in data else "Empty",
        data["from_id"]
    )
    if data["text"].lower() == "начать":
        start_answer(data, group_id)
        return True

    if "payload" not in data:
        return False

    data["payload"] = json.loads(data["payload"])
    if "command" in data["payload"]:
        start_answer(data, group_id)


    if "payload" in data:
        if data["payload"]["active"] == "True":
            DB.User_subscription().remove(data["payload"]["sub_id"], data["from_id"])
        else:
            DB.User_subscription().add(data["from_id"], data["payload"]["sub_id"])

        sub_kb = get_sub_kb(data["from_id"], group_id)
        community = get_community({"group_id": group_id})
        Vk.send_message(
            data["from_id"],
            community["token"],
            message="Подписки обновлены",
            keyboard=sub_kb
        )
        return True

    return False


def new_sub_type(data):
    sub = DB.Subscription()
    sub_id = sub.add(
        data["name"],
        data["keyword"],
        data["text"],
        data["group_id"]
    )
    return sub_id


def get_admin(data):
    admin = DB.Admin(data["login"], data["password"])
    return admin.get()


def get_subs(data):
    subs = DB.Subscriptions(data["group_id"])
    return subs.get()


def set_admin_group(data):
    admin = DB.Admin(data["login"])
    return admin.set_gr(data["group_token"], data["conf_token"])


def new_admin(data):
    admin = DB.Admin(data["login"], data["password"])
    return admin.add()


def remove_sub(data):
    return DB.Subscription().remove(data["sub_id"])


def edit_sub(data):
    return DB.Subscription().change(data["name"], data["keyword"], data["text"], data["id"])
