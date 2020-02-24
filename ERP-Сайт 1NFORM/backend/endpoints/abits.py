from flask_restplus import Namespace, Resource
from ..role_control import role
from .. import DataBase as DB
from flask import request, json
from .. import Questing
from datetime import datetime, timedelta


abits_api = Namespace('abits', description='Abits operations')


@abits_api.route('/')
class Faculty(Resource):
    @role('204')
    def get(self):
        filter = {
            'faculties': request.args.get('faculties'),
            'status': request.args.get('status'),
            'personal': request.args.get('personal'),
            'search': request.args.get('search')
        }
        fields = request.args.get('fields')
        limit = request.args.get('limit')
        token = request.headers.get("Authorization")
        member = DB.check_member("info", token)
        if not filter or not fields:
            return {"msg": "Faculties and filter is needed"}, 422
        res = DB.get_abits(filter, fields, limit, member["info"]["vk"])
        return res, 200

    def post(self):
        data = request.data
        if not data:
            return {"msg": "Data is needed"}, 422
        return DB.add_abit(json.loads(data)), 200


@abits_api.route('/<int:abit>')
class Abiturients(Resource):
    @role('204')
    def put(self, abit):
        data = request.data
        if not data:
            return {"msg": "Data is needed"}, 422

        data = json.loads(data)

        res_abit = DB.get_abit(abit, 'status,id,faculty,full_name,predictings')
        token = request.headers.get("Authorization")
        user = DB.check_member("info,score,quests,news,departments", token)
        if 'type' in data:
            if data['type'] == 'drop':
                if res_abit['status']['name'] == "4":
                    if res_abit['status']['found_by']['name'] == user['info']['name']:
                        DB.add_score(user, -2)
                        Questing.drop_abit_found_quests(user, res_abit)
                        return DB.drop_abit(res_abit['id']), 200

            if data['type'] == 'adding_conf':
                if res_abit['status']['name'] == "4":
                    if res_abit['faculty'] == user['info']['faculty']:
                        return DB.conf_abit(res_abit, user)

            if data['type'] == 'predict_failed':
                Questing.surf_quest("fail_predict", res_abit, user)
                Questing.surf_quest("platfinder_failed", res_abit, user)
                return DB.fail_predict(res_abit, data['predict_vk']), 200

            if data['type'] == 'predict_success' and res_abit['status']['name'] in ['1','2','3']:
                if res_abit['status']['name'] == '2':
                    if not res_abit['status']['taken_by']['id'] == user['info']['vk']:
                        return {"Msg": "Not yours"}, 422
                Questing.surf_quest("confirm_predict", res_abit, user)
                DB.add_surf_counter(user, res_abit['faculty'])
                DB.add_score(user, 2)
                Questing.surf_quest("platfinder_success", res_abit, user)
                return DB.confirm_abit(res_abit, data['predict_vk'], user, type='prediction'), 200

            if data['type'] == 'take_abit' and res_abit['status']['name'] in ['1','3']:
                if res_abit['status']['name'] == '3':
                    if res_abit['status']['taken_by']['id'] == user['info']['vk']:
                        return {"Msg": "This abiturient was alredy taken by %s" % user['id']}, 422

                Questing.surf_quest("take", res_abit, user)
                return DB.take_abit(res_abit, user), 200

            if data['type'] == 'hard_abit' and res_abit['status']['name'] == '2':
                if not res_abit['status']['taken_by']['id'] == user['info']['vk']:
                    return {"Msg": "This abiturient was alredy taken by %s" % user['id']}, 422

                Questing.surf_quest("hard", res_abit, user)
                return DB.hard_abit(res_abit, user), 200

            if data['type'] == 'confirm_abit' and res_abit['status']['name'] in ['2', '3']:
                if res_abit['status']['name'] == '2':
                    if not res_abit['status']['taken_by']['id'] == user['info']['vk']:
                        return {"Msg": "This abiturient was alredy taken by %s" % user['id']}, 422

                if 'vk' not in data:
                    return {"Msg": "Vk is needed"}, 422

                answer = DB.confirm_abit(res_abit, data['vk'], user, type='self')

                if res_abit['status']['name'] == '3':
                    exp_date = datetime.fromtimestamp(answer['status']['date_taken']) + timedelta(seconds = 21600)
                    date = datetime.now()
                    if date >= exp_date:
                        Questing.surf_quest("confirm", res_abit, user)
                else:
                    Questing.surf_quest("confirm", res_abit, user)
                DB.add_score(user, 2)
                DB.add_surf_counter(user, res_abit['faculty'])
                return answer, 200

            if data['type'] == 'comment':
                if 'comment' not in data:
                    return {"Msg": "Comment is needed"}, 422

                if res_abit['status']['taken_by']:
                    if not user['info']['name'] == res_abit['status']['taken_by']['name']:
                        if not res_abit['status']['name'] == "4":
                            DB.add_news({
                                "title": "Серфинг",
                                "text": "'%s' был прокомментирован" % res_abit['full_name'],
                                "type": "personal"
                            }, user['info']['vk'])

                Questing.surf_quest("comment", res_abit, user)
                return DB.comment_abit(res_abit, data['comment'], user), 200

            return {"Msg": "Wrong type passed"}, 422

        else:
            return {"Msg": "Type is needed"}, 422

    @role('204')
    def get(self, abit):
        filter = request.args.get('filter')
        if not filter:
            return {"msg": "Filter is needed"}, 422
        return DB.get_abit(abit, filter), 200

    @role('204')
    def post(self, abit):
        filter = request.args.get('filter')
        if not filter:
            return {"msg": "Filter is needed"}, 422
        return DB.get_abit(abit, filter), 200


@abits_api.route("/<int:id>/comments")
class Comments(Resource):
    @role('204')
    def post(self, id):
        data = request.data
        if not data:
            return {"Msg": "Data is needed"}, 422

        data = json.loads(data)
        member = DB.check_member("info", request.headers.get("Authorization"))

        if not data['comment']['author'] == member['info']['name']:
            return {"Msg": "Not your comment"}, 403

        if 'comment' not in data:
            return {"Msg": "Missing field 'comment'"}, 422

        return DB.delete_comment({
            "$pull": {
                "comments": data['comment']
            }
        }, id), 200
