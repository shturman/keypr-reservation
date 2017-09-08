import pickle
import random
import string

STORAGE_FILE = 'reservations.data'


class Storage:
    def __init__(self, storage_file_name):
        self.storage_file_name = storage_file_name
        try:
            with open(self.storage_file_name, mode='rb') as file:
                self.reservations = pickle.load(file)
        except (FileNotFoundError, EOFError, pickle.UnpicklingError):
            self.reservations = {}

    async def get_reservations(self, from_date=None, to_date=None):
        def date_filter(reservation):
            return \
                (not from_date or reservation['start_date'] >= from_date) and \
                (not to_date or reservation['end_date'] <= to_date)
        filtered = [(k, v) for k,v in self.reservations.items() if date_filter(v)]
        return [{'id': reservation_id, **reservation} for reservation_id, reservation in filtered]

    async def create_reservation(self, reservation):
        reservation_id = ''.join(random.SystemRandom().choices(string.ascii_letters + string.digits, k=8))
        self.reservations[reservation_id] = reservation
        return reservation_id

    async def update_reservation(self, reservation_id, reservation):
        if reservation_id in self.reservations:
            self.reservations[reservation_id] = reservation

    async def delete_reservation(self, reservation_id):
        self.reservations.pop(reservation_id, None)

    async def stop(self):
        with open(self.storage_file_name, mode='wb') as file:
            pickle.dump(self.reservations, file)


async def on_startup(app):
    app['storage'] = Storage(STORAGE_FILE)


async def on_cleanup(app):
    await app['storage'].stop()
