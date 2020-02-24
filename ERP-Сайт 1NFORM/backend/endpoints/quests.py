from flask_restplus import Namespace, Resource
from ..role_control import role
from .. import DataBase as DB
from flask import request, json


api = Namespace('quests', description='Quests operations')


@api.route('/')
class Quest(Resource):
    @role('204')
    def get(self):
        faculty = request.args.get('faculty')
        if not faculty:
            return {"Msg": "Faculty is needed"}, 422
        department = request.args.get('departments')
        if not department:
            return {"Msg": "Department is needed"}, 422

        return DB.get_quests({'faculty': faculty, 'departments': department}), 200

    @role('794')
    def post(self):
        data = request.data
        if not data:
            return {"Msg": "Data is needed"}, 422

        return DB.create_quest(json.loads(data)), 201
