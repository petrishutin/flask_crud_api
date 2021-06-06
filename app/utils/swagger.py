from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

spec = APISpec(
    title="TODOs - Flask CRUD API",
    version="0.0.1",
    openapi_version="3.0.0",
    plugins=[MarshmallowPlugin()],
)

jwt_scheme = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
spec.components.security_scheme("jwt", jwt_scheme)
