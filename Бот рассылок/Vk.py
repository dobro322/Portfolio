import vk
from Settings import token as access_token
import random

session = vk.Session()
api = vk.API(session, v=5.103)

def trySend(fn):
    """
    Пытаемся отправить сообщение
    Иначе выводим текст ошибки в консоль для отладки
    """
    try:
        def catch_arg(body):
            fn(body)
    except Exception as e:
        raise e
    return fn


@trySend
def send_message(user_id, token, message="", keyboard=None, post=""):
    if keyboard:
        api.messages.send(
            access_token=token,
            random_id=random.randint(-2**64, 2**64),
            user_id=user_id,
            message=message,
            attachment=post,
            keyboard=keyboard
        )
    else:
        api.messages.send(
            access_token=token,
            random_id=random.randint(-2**64, 2**64),
            user_id=user_id,
            message=message,
            attachment=post,
        )


@trySend
def get_user(user_id):
    return api.users.get(
        access_token=access_token,
        user_ids=user_id,
        fields="photo_max_orig"
    )[0]


@trySend
def get_community(token):
    return api.groups.getById(
        access_token=token
    )[0]
