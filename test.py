from app import client
from models import Region


def test_simple():
    mylist = [1, 2, 3, 4, 5]

    assert 1 in mylist


def test_get():
    res = client.get('/region')

    assert res.status_code == 200

    assert len(res.get_json()) == len(Region.query.all())
    assert res.get_json()[0]['id'] == 1


def test_post():
    data = {
        'name': 'Восточный',
        'region_id': 'None'
    }

    res = client.post('/region', json=data)

    assert res.status_code == 200


def test_put():
    res = client.put('/region/1', json={'name': 'Южный'})

    assert res.status_code == 200
    assert Region.query.get(1).name == 'Центральный'


def test_delete():
    res = client.delete('/region/1')

    assert res.status_code == 204
    assert Region.query.get(1) is None
