import validation
from aiohttp import web

SCHEMA = {
    'type': 'object',
    'properties': {
        'first_name': {'type': 'string'},
        'last_name': {'type': 'string'},
        'room_number': {'type': 'string'},
        'start_date': {'type': 'string', 'format': 'date-time'},
        'end_date': {'type': 'string', 'format': 'date-time'}
    },
    'required': ['first_name', 'last_name', 'start_date', 'end_date']
}


async def get_reservations(request):
    pass


@validation.validator(SCHEMA)
async def create_reservation(request):
    return web.Response(status=204)


@validation.validator(SCHEMA)
async def update_reservation(request):
    return web.Response(status=204)


async def delete_reservation(request):
    pass