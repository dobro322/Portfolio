from flask_restplus import Namespace, Resource, fields
from ..role_control import role
from .. import DataBase as DB
from flask import request, json
import requests


api = Namespace('members', description='Members operations')


@api.route("/")
class Members(Resource):
    @role(1)
    def get(self):
        answer = DB.get_members()
        return answer, 200
