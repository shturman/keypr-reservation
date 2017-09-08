import reservations
import storage
import json
from datetime import datetime
from aiohttp import web


# Global JSON datetime serializer
json.JSONEncoder.default = lambda self, obj: (obj.isoformat() if isinstance(obj, datetime) else None)


def error_handler_middleware():

    async def middleware_factory(app, handler):

        async def middleware(request):
            try:
                return await handler(request)
            except ValueError as e:
                return web.HTTPBadRequest(reason=e)

        return middleware

    return middleware_factory


def create_app():

    app = web.Application()

    app.middlewares.append(error_handler_middleware())

    app.router.add_get('/reservations/', reservations.get_reservations)
    app.router.add_post('/reservations/', reservations.create_reservation)
    app.router.add_put('/reservations/{id}/', reservations.update_reservation)
    app.router.add_delete('/reservations/{id}/', reservations.delete_reservation)

    app.on_startup.append(storage.on_startup)
    app.on_cleanup.append(storage.on_cleanup)

    return app


aio_app = create_app()

if __name__ == "__main__":
    web.run_app(aio_app, port=5000)
