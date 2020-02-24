from flask_restplus import Namespace, Resource, fields
from ..role_control import role
from .. import DataBase as DB
from flask import request, json
import requests
import re
from .. import Questing

api = Namespace('conversations', description='Messages operations')


@api.route("/")
class Conversations(Resource):
    def post(self):
        data = json.loads(request.data)
        if data:
            return DB.add_conversation(data), 201

    @role('794')
    def get(self):
        temp = list([])
        for i in range(89, 105):
            data = {
                'access_token': "fd84df13ed5b21103536ea168dba0475e0b35fd7e7ca80d9d8b9bd8b5fa4dfb2171f3df817bc0e81964f2",
                'v': "5.101",
                'peer_ids': 2000000000+i
            }
            answer = requests.post('https://api.vk.com/method/messages.getConversationsById', data).text

            try:
                answer = json.loads(answer)['response']['items'][0]
                a = {
                    "peer_id": answer['peer']['id'],
                    "title": answer['chat_settings']['title'],
                    "faculty": re.match("\w+", answer['chat_settings']['title']).group(0)
                }
                DB.add_conversation(a)
                temp.append(a)
            except Exception:
                pass
        return temp


@api.route("/messages")
class Messages(Resource):
    def post(self):
        try:
            data = json.loads(request.data)
            conversation = DB.find_conversation(data['peer_id'])
            member = DB.get_member('info,score,quests,departments,news', data['from_id'])
            if conversation:
                if 'action' in data:
                    if data['action']['type'] == 'chat_invite_user':
                        abit = DB.get_abit_by_vk(data['action']['member_id'])
                        if abit:
                            abit = DB.get_abit_by_vk(data['action']['member_id'])
                            Questing.surf_quest("add", abit, member)
                            return DB.added_abit(data['action']['member_id']), 201
                        else:
                            return DB.add_chat_invite_storage(data['action']['member_id']), 201
                    else:
                        return {"Msg", "Useless action " + data['action']['type']}, 422

                else:
                    abit = DB.get_abit_by_vk(data['from_id'])
                    if member:
                        Questing.message_quest("new", member, data['text'])

                        DB.add_user_message(member, conversation, data['text'])
                    elif abit:
                        DB.add_abit_message(abit, conversation, data['text'])
                    else:
                        return {"Msg": "No user with this id"}, 422
                    return DB.add_message(data, conversation), 201

            else:
                return {"Msg": "No conversation for this message"}, 422
        except Exception as e:
            return {"Msg": "Failed " + str(e)}
