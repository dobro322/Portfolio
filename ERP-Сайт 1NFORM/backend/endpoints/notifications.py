from flask_restplus import Namespace, Resource
from ..role_control import role
from .. import DataBase as DB
from flask import request


api = Namespace('notifications', description='Shop operations')


@api.route('/<int:id>')
class Shop(Resource):
    @role('204')
    def put(self, id):
        return DB.read_notification(request.headers.get("Authorization"), id), 200
