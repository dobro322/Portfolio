from flask_restplus import Namespace, Resource
from ..role_control import role
from .. import DataBase as DB


api = Namespace('shop', description='Shop operations')


@api.route('/')
class Shop(Resource):
    @role('204')
    def get(self):
        return DB.get_shop(), 200
