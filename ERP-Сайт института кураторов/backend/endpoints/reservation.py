from flask_restplus import Namespace, Resource
from ..role_control import role
from .. import DataBase as DB
from flask import request, json


api = Namespace('reservation', description='Reservation operations')


def check_reservation(time_start, time_end, place_id):
    place = DB.places_db.find_one({"id": int(place_id)})
    if place["name"] == "Другое":
        return True

    for reservation in place["reservation_time"]:
        if reservation["aborted"]:
            continue

        if reservation["time_start"] >= time_end:
            continue

        if reservation["time_end"] <= time_start:
            continue

        return False

    return True


def get_reserved_places(member):
    query = {
        "reservation_time": {
            "$elemMatch": {
                "reserved_by.group": member["group_info"]["group"],
                "time_end": {"$gt": DB.currtime()},
                "aborted": False
            }
        }
    }
    return DB.get_places(query)


@api.route('/')
class Reservation(Resource):
    @role(1)
    def get(self):
        answ = DB.get_places()
        return answ, 200

    @role(1)
    def post(self):
        data = request.data
        if not data:
            return {"Msg": "No data"}, 422

        data = json.loads(data)
        token = request.headers.get('Authorization')
        member = DB.get_member(token=token)

        if get_reserved_places(member):
            return {"Msg": "Maximum 1 reservation"}, 422

        if not check_reservation(data["time_start"], data["time_end"], data["id"]):
            return {"Msg": "Wrong time"}, 422

        return DB.add_reservation(data, member), 201


@api.route("/reserved")
class Reserved(Resource):
    @role(1)
    def get(self):
        member_token = request.headers.get("Authorization")
        member = DB.get_member(token=member_token)
        places = get_reserved_places(member)
        return places, 200

    @role(1)
    def delete(self):
        member_token = request.headers.get("Authorization")
        member = DB.get_member(token=member_token)
        query = {
            "reservation_time": {
                "$elemMatch": {
                    "reserved_by.group": member["group_info"]["group"],
                    "time_end": {"$gt": DB.currtime()},
                    "aborted": False
                }
            }
        }
        chgangings = {
            "$set": {
                "reservation_time.$.aborted": True
            }
        }
        DB.update_reservation(query, chgangings)
        places = DB.get_places(query)
        return places, 200
