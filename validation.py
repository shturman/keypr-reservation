import jsonschema
import json
from aiohttp import web
from functools import wraps


def validator(schema):
    def wrapper(func):
        @wraps(func)
        async def validate(request):
            try:
                jsonschema.validate(await request.json(), schema)
                return await func(request)
            except jsonschema.ValidationError as e:
                raise web.HTTPBadRequest(reason=e.message)
            except json.decoder.JSONDecodeError as e:
                raise web.HTTPBadRequest(reason=e.msg)
        return validate
    return wrapper
