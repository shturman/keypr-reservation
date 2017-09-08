import os
import app
import json
import pytest
import storage
from datetime import datetime, timedelta


@pytest.fixture()
def client(loop, test_client):
    try:
        os.remove(storage.STORAGE_FILE)
    except FileNotFoundError:
        pass
    return loop.run_until_complete(test_client(app.create_app()))


async def test_no_body(client):
    assert (await client.post('/reservations/')).status == 400
    assert (await client.put('/reservations/123/')).status == 400


async def test_wrong_format(client):
    assert (await client.post('/reservations/', data=json.dumps({'first_name': 'name'}))).status == 400
    assert (await client.put('/reservations/234/', data=json.dumps({'first_name': 'name'}))).status == 400


async def test_crud(client):
    ok_reservation = json.dumps(
        {
            'first_name': 'name',
            'last_name': 'last name',
            'start_date': datetime.now().isoformat(),
            'end_date': (datetime.now() + timedelta(days=2)).isoformat()
        })
    create_response = await client.post('/reservations/', data=ok_reservation)
    assert create_response.status == 200

    response_json = json.loads(await create_response.text())

    put_response = await client.put('/reservations/%s/' % response_json['reservation_id'], data=ok_reservation)
    assert put_response.status == 204

    get_response = await client.get('/reservations/')
    assert get_response.status == 200 and len(json.loads(await get_response.text())) == 1

    get_response = await client.get('/reservations/from_date=%s' % (datetime.now() + timedelta(days=1)))
    assert get_response.status == 404

    get_response = await client.get('/reservations/?from_date=%s' % (datetime.now() + timedelta(days=1)))
    assert get_response.status == 200 and len(json.loads(await get_response.text())) == 0

    delete_response = await client.delete('/reservations/%s/' % response_json['reservation_id'])
    assert delete_response.status == 204

    get_response = await client.get('/reservations/')
    assert get_response.status == 200 and len(json.loads(await get_response.text())) == 0
