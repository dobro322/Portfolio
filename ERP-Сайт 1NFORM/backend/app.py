from flask_restplus import Api
from .endpoints.quests import api as quest_api
from .endpoints.abits import abits_api as abits_api
from .endpoints.deps import api as deps_api
from .endpoints.kanban import api as kanban_api
from .endpoints.kanban import task_api as task_api
from .endpoints.messages import api as messages_api
from .endpoints.team import api as team_api
from .endpoints.user import api as user_api
from .endpoints.event import api as event_api
from .endpoints.user import login as login_api
from .endpoints.shop import api as shop_api
from .endpoints.admin import api as admin_api
from .endpoints.notifications import api as notifications_api
from flask import Blueprint

api_v1 = Blueprint('api_v1', __name__)
api = Api(
    api_v1,
    version='1.0',
    title='1NFORM API',
    description='1NFORM-ERP API V1.0'
)


api.add_namespace(quest_api)
api.add_namespace(abits_api)
api.add_namespace(deps_api)
api.add_namespace(kanban_api)
api.add_namespace(messages_api)
api.add_namespace(team_api)
api.add_namespace(user_api)
api.add_namespace(task_api)
api.add_namespace(shop_api)
api.add_namespace(login_api)
api.add_namespace(admin_api)
api.add_namespace(notifications_api)
api.add_namespace(event_api)
