import validation
from aiohttp import web
from dateutil.parser import parse

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
    from_date = request.rel_url.query.get('from_date', default=None)
    to_date = request.rel_url.query.get('to_date', default=None)
    reservations = await request.app['storage'].get_reservations(
        from_date and parse(from_date),
        to_date and parse(to_date)
    )
    return web.json_response(reservations)


@validation.validator(SCHEMA)
async def create_reservation(request):
    reservation = await request.json()
    reservation['start_date'], reservation['end_date'] = parse(reservation['start_date']), parse(reservation['end_date'])
    return web.json_response(
        {
            'reservation_id': await request.app['storage'].create_reservation(reservation)
        }
    )


@validation.validator(SCHEMA)
async def update_reservation(request):
    reservation = await request.json()
    reservation['start_date'], reservation['end_date'] = parse(reservation['start_date']), parse(reservation['end_date'])
    await request.app['storage'].update_reservation(request.match_info['id'], reservation)
    return web.Response(status=204)


async def delete_reservation(request):
    await request.app['storage'].delete_reservation(request.match_info['id'])
    return web.Response(status=204)
