import requests


class AlaskaClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def create_bear(self, data: dict, headers: dict) -> requests.Response:
        return requests.post(url=f"{self.base_url}/bear", json=data, headers=headers)

    def delete_bear(self, bear_id: int, headers: dict) -> requests.Response:
        return requests.delete(url=f"{self.base_url}/bear/{bear_id}", headers=headers)

    def get_bear(self, bear_id: int, headers: dict) -> requests.Response:
        return requests.get(url=f"{self.base_url}/bear/{bear_id}", headers=headers)

    def get_all_bears(self, headers: dict) -> requests.Response:
        return requests.get(url=f"{self.base_url}/bear", headers=headers)

    def update_bear(self, bear_id: int, data: dict, headers: dict) -> requests.Response:
        return requests.put(url=f"{self.base_url}/bear/{bear_id}", json=data, headers=headers)

    def delete_all_bears(self, headers: dict) -> requests.Response:
        return requests.delete(url=f"{self.base_url}/bear", headers=headers)
