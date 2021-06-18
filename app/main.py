from flask import Flask
from flask_restful import Api
from flask_apispec import FlaskApiSpec

from app import config
from app.db.db_engine import init_db
from app.resources import Users, LogIn, LogOut, ToDosGetAllPost, ToDosGetByIdPutDelete
from app.utils.jwt_auth import JWTAuth
from app.utils.swagger import spec, update_paths_with_bearer_security_check

app = Flask(__name__)
app.config.from_object(config)
app.url_map.strict_slashes = False
app.config.update({'APISPEC_SPEC': spec})

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

fields_to_add_bearer_security_check = {
    '/logout': ('get',),
    '/todos/{username}': ('get', 'post'),
    '/todos/{username}/{todo_id}': ('get', 'put', 'delete')
}
update_paths_with_bearer_security_check(spec, fields_to_add_bearer_security_check)

if __name__ == '__main__':
    init_db()
    app.run(port=8080, debug=1)
