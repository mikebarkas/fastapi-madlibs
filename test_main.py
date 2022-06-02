from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root():
    response = client.get('/')
    assert response.status_code == 200


def test_no_madlibs():
    response = client.get('/v1/not-found')
    r = response.json()
    assert response.status_code == 404


def test_madlibs_1():
    response = client.get('/v1/madlibs')
    r = response.json()
    assert response.status_code == 200


def test_madlibs_2():
    response = client.get('/v2/madlibs')
    r = response.json()
    assert response.status_code == 200
    # assert response.json() == {'status': 'success'}
