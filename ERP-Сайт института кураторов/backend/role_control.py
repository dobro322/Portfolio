from functools import wraps
from flask import request
from . import DataBase as DB


def role(arg):
    def func(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            role, token = arg, request.headers.get('Authorization')
            user = DB.get_member(token=token)
            if user:
                if user['role'] >= role:
                    return fn(*args, **kwargs)
                else:
                    return {"Msg": 'No permissions'}, 403
            else:
                return {"Msg": 'No user with such token'}, 401
        return wrapper
    return func
