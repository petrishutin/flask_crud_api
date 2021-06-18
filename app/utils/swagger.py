from typing import Dict

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

spec = APISpec(
    title="TODOs - Flask CRUD API",
    version="0.0.1",
    openapi_version="2.0.0",
    plugins=[MarshmallowPlugin()],
)

spec.components.security_scheme("Bearer", {"type": "apiKey", "name": "Authorization", "in": "header"})


def update_paths_with_bearer_security_check(spec: APISpec, paths_list: Dict[str, tuple]):
    for path in paths_list:
        for method in paths_list[path]:
            spec._paths[path][method].update({'security': [{'Bearer': []}]})
