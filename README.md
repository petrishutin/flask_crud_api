# Flask CRUD API service

## Description

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

Use swagger2.0 at /swagger-ui

###Important!!!
####To authorize in swagger fill token field with 'Bearer <your JWT token>', because OpenAPI2 does not support JWT directly

## Tech

- Framework: Flask 1.1
- ORM: SQLAlchemy
- Authorization: Flask-JWT-extended
- swagger2.0: flask_apispec + apispec
