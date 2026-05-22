import pytest

from config import BASE_URL
from framework.alaska_client import AlaskaClient


@pytest.fixture
def alaska_client():
    return AlaskaClient(base_url=BASE_URL)


@pytest.fixture
def headers():
    return {"Content-Type": "application/json"}


@pytest.fixture(autouse=True)
def cleanup(alaska_client, headers):
    alaska_client.delete_all_bears(headers)
    yield
    alaska_client.delete_all_bears(headers)
