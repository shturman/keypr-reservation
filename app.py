import reservations
from aiohttp import web


def create_app():

    app = web.Application()

    app.router.add_get('/reservations/', reservations.get_reservations)
    app.router.add_post('/reservations/', reservations.create_reservation)
    app.router.add_put('/reservations/{id}/', reservations.update_reservation)
    app.router.add_delete('/reservations/{id}/', reservations.delete_reservation)

    return app


aio_app = create_app()

if __name__ == "__main__":
    web.run_app(aio_app, port=5000)
