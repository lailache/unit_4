import pytest
import requests
from pytest_httpserver import HTTPServer
from requests.auth import HTTPBasicAuth

from app.app import app

BASE_URL = 'http://127.0.0.1:5000'


@pytest.fixture
def api_client():
    class APIClient:
        def __init__(self, base_url):
            self.base_url = base_url
            self.auth = HTTPBasicAuth('user1', 'password1')

        def get(self, path, **kwargs):
            return requests.get(f'{self.base_url}{path}', auth=self.auth, **kwargs)

        def post(self, path, **kwargs):
            return requests.post(f'{self.base_url}{path}', auth=self.auth, **kwargs)

        def put(self, path, **kwargs):
            return requests.put(f'{self.base_url}{path}', auth=self.auth, **kwargs)

        def delete(self, path, **kwargs):
            return requests.delete(f'{self.base_url}{path}', auth=self.auth, **kwargs)

    return APIClient(BASE_URL)


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client


@pytest.fixture(scope="session")
def httpserver_listen_address():
    return "localhost", 5000


@pytest.fixture
def api_client_with_httpserver(httpserver: HTTPServer):
    class APIClient:
        def __init__(self, base_url):
            self.base_url = base_url

        def get(self, path, **kwargs):
            return requests.get(f'{self.base_url}{path}', **kwargs)

        def post(self, path, **kwargs):
            return requests.post(f'{self.base_url}{path}', **kwargs)

        def put(self, path, **kwargs):
            return requests.put(f'{self.base_url}{path}', **kwargs)

        def delete(self, path, **kwargs):
            return requests.delete(f'{self.base_url}{path}', **kwargs)

    return APIClient(f'http://{httpserver.host}:{httpserver.port}')
