from flask import Flask
from flask_restful import Api

from app import config
from app.db.db_engine import initiate_db
from app.resources.authorization import LogOut, LogIn
from app.resources.todos import ToDos
from app.resources.users import Users
from utils.jwt_auth import JWTAuth


app = Flask(__name__)
app.config.from_object(config)
app.url_map.strict_slashes = False

jwt = JWTAuth(app)
api = Api(app)

api.add_resource(Users, '/users')
api.add_resource(LogIn, '/login')
api.add_resource(LogOut, '/logout')
api.add_resource(ToDos, '/todos/<string:username>', '/todos/<string:username>/<int:todo_id>')

if __name__ == '__main__':
    initiate_db()
    app.run(port=8080, debug=1)
