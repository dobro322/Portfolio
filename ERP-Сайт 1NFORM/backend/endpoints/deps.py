from flask_restplus import Namespace, Resource
from ..role_control import role
from .. import DataBase as DB
from flask import request, json

api = Namespace('deps', description='Deps operations')


@api.route('/')
class Table(Resource):
    @role('204')
    def get(self):
        department = request.args.get('department')
        if not department:
            return {"Msg": "Department is needed"}, 422

        table = {
            'data': DB.get_table(department),
            'dep_members': DB.users_from_dep(department, "info.name")
        }
        return table, 200

    @role('204')
    def post(self):

        data = request.data
        if not data:
            return {"Msg": "Not data"}, 422

        data = json.loads(data)

        if data['department'] in DB.check_member('departments', request.headers.get('Authorization'))['departments']:
            return DB.add_table_row(data), 200
        else:
            return {"Msg": 'Not allowed'}, 405


@api.route('/<int:row>')
class Row(Resource):
    @role('204')
    def put(self, row):
        data = request.data
        if not data:
            return {"Msg": 'No data passed'}, 422

        data = json.loads(data)

        if DB.get_table_row(row)['department'] in DB.check_member('departments', request.headers.get('Authorization'))['departments']:
            return DB.change_table(data['data'], row), 200
        else:
            return {"Msg": 'Not allowed'}, 405

    @role('724')
    def delete(self, row):
        if DB.get_table_row(row)['department'] in DB.check_member('departments', request.headers.get('Authorization'))['departments']:
            return DB.delete_table(row), 200
        else:
            return {"Msg": 'Not allowed'}, 405
