from flask_restplus import Namespace, Resource, fields
from ..role_control import role
from .. import DataBase as DB
from flask import request, json
import requests


api = Namespace('account', description='Account operations')


@api.route("/")
class Account(Resource):
    @role(1)
    def get(self):
        token = request.headers.get('Authorization')
        answer = DB.get_member(token=token)
        return answer, 200

    @role(1)
    def put(self):
        data = request.data
        if not data:
            return {"Msg": "Data is needed"}, 422

        data = json.loads(data)

        if data['type'] == 'settings':
            id = DB.get_member(token=request.headers.get("Authorization"))
            return DB.edit_user(id['info']['vk'], {"settings": data}), 200


@api.route("/login/")
class Login(Resource):
    def post(self):
        data = json.loads(request.data)
        if 'code' not in data:
            return {"Msg": "Code is needed"}, 422
        req = {
            'client_id': 7136223,
            'client_secret': 'zNNsp0NNe7wMSCoabay5',
            'redirect_uri': 'http://xn--80agtricmdcg.xn--p1ai/login',
            'code': data['code']
        }
        answer = requests.get('https://oauth.vk.com/access_token', params=req)
        answer = json.loads(answer.text)
        if 'user_id' not in answer:
            return {"Msg": "Code is invalid"}, 422
        answer = answer['user_id']
        return DB.get_member(id=answer), 200
