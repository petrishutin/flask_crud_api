# Flask CRUD API service

### Description

Example of simple service with CRUD (TODO notes) and JWT authorization

Auth resources:
- user create
- user update
- user login(receive JWT token)
- user logout(revoke JWT token)

Content resources:
- create TODO
- get TODO by id
- get all TODOs
- update TODO
- delete TODO

### Tech

- Framework: Flask 1.1
- ORM: SQLAlchemy
- Authorization: Flask-JWT-extended

## Improve

- Add logging
- Add schemas + Validation(Marshmallow)
- Add apispecs(swagger)