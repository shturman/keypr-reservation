import app
import json
import pytest
from datetime import datetime


@pytest.fixture()
def client(loop, test_client):
    return loop.run_until_complete(test_client(app.create_app()))


async def test_no_body(client):
    assert (await client.post('/reservations/')).status == 400
    assert (await client.put('/reservations/123/')).status == 400


async def test_wrong_format(client):
    assert (await client.post('/reservations/', data=json.dumps({'first_name': 'name'}))).status == 400
    assert (await client.put('/reservations/234/', data=json.dumps({'first_name': 'name'}))).status == 400


async def test_ok_format(client):
    ok_reservation = json.dumps(
        {
            'first_name': 'name',
            'last_name': 'last name',
            'start_date': datetime.now().isoformat(),
            'end_date': datetime.now().isoformat()
        })
    create_response = await client.post('/reservations/', data=ok_reservation)
    put_response = await client.put('/reservations/12123/', data=ok_reservation)

    assert create_response.status == 204
    assert put_response.status == 204

