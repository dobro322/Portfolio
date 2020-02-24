from flask_restplus import Namespace, Resource
from ..role_control import role
from .. import DataBase as DB
from flask import request, json
import requests
from ..Ticket import create_ticket


def ticket_template(code, barcode, fio, faculty):
    ticket_example = {
        "text": [
            {
                "size": 220,
                "font_family": "Museo900",
                "color": (255, 255, 255),
                "text": code,
                "coord": {
                    'x': 135,
                    'y': 2240
                }
            },
            {
                "size": 70,
                "font_family": "Museo900",
                "color": (255, 255, 255),
                "text": fio,
                "coord": {
                    'x': 620,
                    'y': 2300
                }
            },
            {
                "size": 80,
                "font_family": "Museo900",
                "color": (255, 255, 255),
                "text": faculty,
                "coord": {
                    'x': 990,
                    'y': 2428
                }
            }
        ],
        "barcodes": [
            {
                "width": 100,
                "crop": (30, 150, 30, 750),  # lfeft/upper/rigth/lower
                "scale": 3,
                "type": "code128",
                "code": barcode,
                "coords": (20, 2570)
            }
        ],
        "picture": {
            "file": "project/ticket.png",
        }
    }
    return ticket_example


api = Namespace('event', description='Quests operations')


@api.route('/participants')
class Participants(Resource):
    @role("724")
    def get(self):
        query = {
            'status': 'all',
            'token': 'v910fd0a1s98310xjgos9124d141ta'
        }
        try:
            data = requests.get("http://ksilligan.ru:3002/api/get_unchecked", params=query)
            data = json.loads(data.text) if not data.text == "Not Found" else {"Msg": "Not Found"}
            return data, 200
        except Exception as e:
            return {"Msg": str(e)}, 422


@api.route('/participant/<int:id>')
class Participant(Resource):
    @role("724")
    def get(self, id):
        res = DB.inform_tickets.find_one({"id": id}, {"_id": 0})
        member = DB.check_member("info", request.headers.get('Authorization'))
        if not res['arrived']['state']:
            DB.check_ticket(id, member['info']['name'])
        user = DB.inform_abits.find_one({"vk": res['vk']})
        res['bdate'] = user['bdate']
        params = {
            "token": "af9a99sa71038507-4114691-Vlad",
            "fio": res['name'],
            'bdate': res['bdate']
        }
        kibeya_pic = requests.get("http://ksilligan.ru:3005/api/getPhoto", params=params).text
        res['kib_pic'] = kibeya_pic

        if res:
            return res, 200
        else:
            return {"Msg": "No such ticket"}, 422

    @role("724")
    def put(self, id):
        data = request.data
        if not data:
            return {"Msg": "Data is needed"}, 422

        data = json.loads(data)

        if 'type' not in data:
            return {"Msg": "Type is needed"}, 422

        if data['type'] == 'agreement':

            if 'status' not in data:
                return {"Msg": "Status is needed"}, 422

            if int(data['status']) == 0 and 'msg' not in data:
                return {"Msg": "Message is needed"}, 422

            query = {
                'token': 'v910fd0a1s98310xjgos9124d141ta',
                'vk': int(id),
                'status': data['status']
            }

            if int(data['status']) == 0:
                query['msg'] = data['msg']

            data = requests.post("http://ksilligan.ru:3002/api/agreement_checked", data=query)
            return {"Msg": data.text}, 200

        if data['type'] == 'payment':
            ticket = ""
            if 'status' not in data:
                return {"Msg": "Status is needed"}, 422

            if int(data['status']) == 0 and 'msg' not in data:
                return {"Msg": "Message is needed"}, 422

            query = {
                'token': 'v910fd0a1s98310xjgos9124d141ta',
                'vk': int(id),
                'status': data['status']
            }

            if int(data['status']) == 0:
                query['msg'] = data['msg']
                data = requests.post("http://ksilligan.ru:3002/api/payment_accepted?token={}&vk={}&status={}".format(
                    'v910fd0a1s98310xjgos9124d141ta',
                    int(id),
                    data['status']
                ), files={"ticket": ticket})
            else:
                member = DB.get_abit_by_vk(id)
                try:
                    member_ticket = DB.add_ticket({
                        'vk': int(member['vk']),
                        'name': member['full_name'],
                        'faculty': member['faculty'],
                        'pic': member['pic'],
                    })
                except:
                    member_ticket = DB.inform_tickets.find_one({"vk": int(id)})
                ticketid = member_ticket['id']
                temp = ticket_template(
                    ticketid,
                    '1NFORM-' + '0000'[0: 4 - len(str(ticketid))] + str(ticketid),
                    """{}
{}""".format(member_ticket['name'].split(' ')[1], member_ticket['name'].split(' ')[0]),
                    member_ticket['faculty']
                )
                ticket = create_ticket(
                    pic=temp['picture'],
                    barcodes=temp['barcodes'],
                    texts=temp['text']
                )
                query['ticket'] = ticket

                data = requests.post("http://ksilligan.ru:3002/api/payment_accepted?token={}&vk={}&status={}".format(
                    'v910fd0a1s98310xjgos9124d141ta',
                    int(id),
                    data['status']
                ), files={"ticket": ticket})
            return {"Msg": data.text}, 200
