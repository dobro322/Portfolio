from flask_restplus import Namespace, Resource
from ..role_control import role
from .. import DataBase as DB
from flask import request, json
from ..Questing import QUEST_HANDLER, achieve_quest

api = Namespace('admin', description='Quests operations')


@api.route('/')
class Admin(Resource):
    @role('794')
    def get(self):
        quest_names = []

        for quest in QUEST_HANDLER:
            for type in QUEST_HANDLER[quest]:
                for name in QUEST_HANDLER[quest][type]:
                    quest_names.append({
                        'description': QUEST_HANDLER[quest][type][name]['description'],
                        'function': name
                    })

        data = {
            'quests': quest_names,
            'all_quests': list(DB.inform_quests.find({},{"_id": 0})),
            'team': DB.get_team('departments,info,reprimands,news,quests')
        }
        return data, 200


@role('794')
@api.route('/<string:type>')
class AdminChange(Resource):
    def put(self, type):
        data = request.data
        if not data:
            return {"Msg": "Data is needed"}, 422
        data = json.loads(data)

        if type == 'user_department':
            return DB.edit_user(data['vk'], {"departments": data['departments']}), 200

        if type == 'role':
            return DB.edit_user(data['vk'], {"role": data['role']}), 200

        if type == 'achieve_quest':
            return achieve_quest(data['member'], data['quest']), 200
