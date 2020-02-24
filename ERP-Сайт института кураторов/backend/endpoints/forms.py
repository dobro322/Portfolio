from flask_restplus import Namespace, Resource, fields
from ..role_control import role
from .. import DataBase as DB
from flask import request, json


api = Namespace('forms', description='Forms operations')


@api.route('/')
class Forms(Resource):
    @role(1)
    def get(self):
        token = request.headers.get("Authorization")
        member = DB.get_member(token=token)
        query = {}
        if member["role"] < 3:
            query["enabled"] = True

        res = DB.get_forms(query, filter={"answers": 0, "_id": 0})

        for form in res:
            query = {
                "answers.feed_by.vk": member["personal_info"]["vk"],
                "id": form["id"]
            }
            if not DB.get_form(query):
                form["completed"] = False
            else:
                form["completed"] = True

        return res, 200

    @role(3)
    def post(self):

        data = request.data
        if not data:
            return {"Msg": "Data is required"}, 422

        data = json.loads(data)

        try:
            data = {
                "name": data["name"],
                "description": data["description"],
                "questions": data["questions"]
            }
        except Exception as e:
            return {"Msg": "Missing value {}".format(str(e))}, 422

        res = DB.add_form(data)
        return res, 201


@api.route('/<int:id>')
class Form(Resource):
    @role(2)
    def get(self, id):

        query = {
            "id": id
        }
        res = DB.get_form(query)

        return res, 200

    @role(1)
    def post(self, id):

        data = request.data
        if not data:
            return {"Msg": "Data is required"}, 422

        data = json.loads(data)

        if "answers" not in data:
            return {"Msg": "Missing field 'answers'"}, 422

        token = request.headers.get("Authorization")
        member = DB.get_member(token=token)
        answer = {
            "date": DB.currtime(),
            "feed_by": member,
            "answers": data["answers"]
        }

        query = {
            "id": id
        }
        chgangings = {
            "$push": {
                "answers": answer
            }
        }
        res = DB.update_form(query, chgangings)
        DB.forms_log.insert_one({
            "form": res["name"],
            "answer": answer
        })
        return res, 201

    @role(3)
    def put(self, id):

        query = {
            "id": id
        }
        res = DB.get_form(query)
        chgangings = {
            "$set": {
                "enabled": not res["enabled"]
            }
        }
        res = DB.update_form(query, chgangings)
        return res, 200

    @role(3)
    def delete(self, id):
        query = {
            "id": id
        }
        DB.delete_form(query)
        return {"Msg": "Success"}, 200
