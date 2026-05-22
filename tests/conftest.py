import pytest

from framework.models.bears import BearTypes


@pytest.fixture
def valid_bear_payload():
    return {
        "bear_type": BearTypes.BLACK.value,
        "bear_name": "mikhail",
        "bear_age": 17.5,
    }


@pytest.fixture
def created_bear(alaska_client, valid_bear_payload, headers):
    response = alaska_client.create_bear(valid_bear_payload, headers)
    data = response.json()
    return data
