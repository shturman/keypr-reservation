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
                raise ValueError(e.message)
            except json.decoder.JSONDecodeError as e:
                raise ValueError(e.msg)
        return validate
    return wrapper
