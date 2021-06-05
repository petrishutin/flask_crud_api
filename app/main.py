from flask import Flask
from flask_restful import Api
from flask_apispec import FlaskApiSpec

from app import config
from app.db.db_engine import init_db
from app.resources import Users, LogIn, LogOut, ToDosGetAllPost, ToDosGetByIdPutDelete
from app.utils.jwt_auth import JWTAuth

app = Flask(__name__)
app.config.from_object(config)
app.url_map.strict_slashes = False

jwt = JWTAuth(app)

api = Api(app)
api.add_resource(Users, '/users')
api.add_resource(LogIn, '/login')
api.add_resource(LogOut, '/logout')
api.add_resource(ToDosGetAllPost, '/todos/<string:username>')
api.add_resource(ToDosGetByIdPutDelete, '/todos/<string:username>/<int:todo_id>')

docs = FlaskApiSpec(app)
docs.register(Users)
docs.register(LogIn)
docs.register(LogOut)
docs.register(ToDosGetAllPost)
docs.register(ToDosGetByIdPutDelete)

if __name__ == '__main__':
    init_db()
    app.run(port=8080, debug=1)
