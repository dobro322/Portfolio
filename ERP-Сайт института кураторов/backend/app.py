from flask_restplus import Api
from .endpoints.reservation import api as reservation_api
from .endpoints.user import api as user_api
from .endpoints.members import api as members_api
from .endpoints.forms import api as forms_api
from flask import Blueprint

endorfin = Blueprint('endorfin', __name__)
api = Api(
    endorfin,
    version='1.0',
    title='ENDORFIN API',
    description='ENDORFIN-ERP API V1.0'
)


api.add_namespace(reservation_api)
api.add_namespace(user_api)
api.add_namespace(members_api)
api.add_namespace(forms_api)
