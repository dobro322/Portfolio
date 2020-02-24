from flask_restplus import Namespace, Resource, fields
from ..role_control import role
from .. import DataBase as DB
from flask import json, request
from datetime import datetime, timedelta


def get_message_stat(id):
    data = DB.get_message_history(id)
    arr = {}

    for x in range(0, 32):
        date = str(datetime.fromtimestamp(1564358400).date() + timedelta(days = x) )
        arr[date] = {
            'count': 0,
            'words': 0
        }

    for (index, row) in enumerate(data):
        date = str(datetime.fromtimestamp(row['date']).date())
        if date in arr:
            arr[date]['count'] += 1
            arr[date]['words'] += len(row['text'].split(' '))

    return ([{x[0]: {'count': x[1]['count'], 'words': x[1]['words']}} for x in arr.items()])


def get_surfing_stat(id):
    data = DB.get_surfing_history(id)
    arr = {}

    for x in range(0, 32):
        date = str(datetime.fromtimestamp(1564358400).date() + timedelta(days = x) )
        arr[date] = 0

    for (index, row) in enumerate(data):
        date = str(datetime.fromtimestamp(row['status']['date_found']).date())
        if date in arr:
            arr[date] += 1
    return ([{x[0]: {'date_found': x[1]}} for x in arr.items()])


api = Namespace('team', description='Team operations')

team = api.model('Team', {
    'token': fields.String(required=True, description='User token'),
    'filter': fields.String(required=False, description='Key filters'),
})


@api.route("/")
class Team(Resource):
    @role('204')
    def get(self):
        data = request.args.get('filter')
        answer = DB.get_team(data)
        if not data:
            return {"Msg": "Filter is needed"}, 422
        return answer, 200

    @role('724')
    def post(self):
        data = json.loads(request.data)
        if not data:
            return {"Msg": "Data is needed"}, 422
        answer = DB.new_partner(data)
        return answer, 201

    @role('724')
    def put(self):
        return {'res': api.payload}, 201


@api.route("/<int:id>")
class Member(Resource):
    @role('204')
    def get(self, id):
        data = request.args.get('filter')

        if not data:
            return {"Msg": "Filter is needed"}, 422
        answer = DB.get_member(data, id)
        if request.args.get('extended'):
            answer['chatting'] = get_message_stat(id)
            answer['surfing'] = get_surfing_stat(id)

        return answer, 200

    @role('794')
    def delete(self, id):
        return DB.delete_user(id), 200
