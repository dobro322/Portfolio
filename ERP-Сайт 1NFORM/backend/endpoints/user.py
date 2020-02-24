from flask_restplus import Namespace, Resource, fields
from ..role_control import role
from .. import DataBase as DB
from flask import request, json
import requests


api = Namespace('account', description='Account operations')
login = Namespace('login', description='Login operations')

login_in = api.model('login_in', {
    'code': fields.String(required=True, description='User code')
})


@api.route("/")
class Account(Resource):
    @role('204')
    def get(self):
        data = request.args.get('filter')
        if not data:
            return {"Msg": "Filter is needed"}, 422
        token = request.headers.get('Authorization')
        answer = DB.get_self(data, token)
        return answer, 200

    @role("204")
    def put(self):
        data = request.data
        if not data:
            return {"Msg": "Data is needed"}, 422

        data = json.loads(data)

        if data['type'] == 'settings':
            id = DB.check_member('info', request.headers.get("Authorization"))
            return DB.edit_user(id['info']['vk'], {"settings": data}), 200


@login.route("/")
class Login(Resource):
    @login.expect(login_in)
    def post(self):
        data = json.loads(request.data)
        if 'code' not in data:
            return {"Msg": "Code is needed"}, 422
        req = {
            'client_id': 6630817,
            'client_secret': 'oU6Tyg3MAMWJtpydg2Dh',
            'redirect_uri': 'https://1nform.ru/logging',
            'code': data['code']
        }
        answer = requests.get('https://oauth.vk.com/access_token', params = req)
        answer = json.loads(answer.text)
        if 'user_id' not in answer:
            return {"Msg": "Code is invalid"}, 422
        answer = answer['user_id']
        return DB.get_member('token', answer), 200
