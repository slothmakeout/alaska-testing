import allure
import pytest

from framework.models.bears import BearTypes


@allure.epic("Alaska Bear Service")
@allure.feature("CRUD Bears")
class TestCreateBear:
    @allure.title("Успешное создание и получение медведя")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_and_get_bear(self, alaska_client, valid_bear_payload, headers):
        create_response = alaska_client.create_bear(
            valid_bear_payload, headers)
        bear_id = create_response.json()

        get_response = alaska_client.get_bear(bear_id, headers)
        bear = get_response.json()

        assert bear["bear_type"] == valid_bear_payload["bear_type"], (
            "Вернулся некорректный тип\n"
            f"Response:\n{bear["bear_type"]}\n"
            f"Ожидаемый тип: {valid_bear_payload["bear_type"]}"
        )
        assert bear["bear_name"] == valid_bear_payload["bear_name"], (
            "Вернулось неккоректное имя\n"
            f"Response:\n{bear["bear_name"]}\n"
            f"Ожидаемый тип: {valid_bear_payload["bear_name"]}"
        )
        assert bear["bear_age"] == valid_bear_payload["bear_age"], (
            "Вернулся некорректный возраст\n"
            f"Response:\n{bear["bear_age"]}\n"
            f"Ожидаемый тип: {valid_bear_payload["bear_age"]}"
        )

    @allure.title("Создание медведя только с полем имени")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_only_name(self, alaska_client, headers):
        payload = {"bear_name": "dudeman"}
        create_response = alaska_client.create_bear(payload, headers)
        print(f"Status: {create_response.status_code}")
        print(f"Body: {create_response.text}")

        assert create_response.status_code == 400, (
            f"Ожидали 400, получили {create_response.status_code}\n"
            f"Body: {create_response.text}\n"
        )

    @allure.title("Создание медведя только с полем возраста")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_only_age(self, alaska_client, headers):
        payload = {"bear_age": 10.0}
        create_response = alaska_client.create_bear(payload, headers)
        print(f"Status: {create_response.status_code}")
        print(f"Body: {create_response.text}")

        assert create_response.status_code == 400, (
            f"Ожидали 400, получили {create_response.status_code}\n"
            f"Body: {create_response.text}\n"
        )

    @allure.title("Создание медведя только с полем типа")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_only_type(self, alaska_client, headers):
        payload = {"bear_type": BearTypes.BLACK.value}
        create_response = alaska_client.create_bear(payload, headers)
        print(f"Status: {create_response.status_code}")
        print(f"Body: {create_response.text}")

        assert create_response.status_code == 400, (
            f"Ожидали 400, получили {create_response.status_code}\n"
            f"Body: {create_response.text}\n"
        )

    @allure.title("Создание медведя с каждым из 4 типов")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("bear_type", [t.value for t in BearTypes])
    def test_create_bear_each_type(self, alaska_client, headers, bear_type):
        payload = {"bear_name": "dudeman", "bear_age": 10.0,
                   "bear_type": bear_type}
        create_response = alaska_client.create_bear(payload, headers)
        print(f"Status: {create_response.status_code}")
        print(f"Body: {create_response.text}")

        assert create_response.status_code == 200, (
            f"Ожидали 200, получили {create_response.status_code}\n"
            f"Body: {create_response.text}\n"
        )

        bear_id = create_response.json()
        get_response = alaska_client.get_bear(bear_id, headers)
        print(f"GET Status: {get_response.status_code}")
        print(f"GET Body: {get_response.text}")
        bear = get_response.json()
        print(f"GET bear: {bear}")

        assert bear["bear_type"] == bear_type, (
            f"Ожидали тип {bear_type}, получили {bear["bear_type"]}\n"
        )

    @allure.title("Создание медведя с пустым JSON")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_empty_json(self, alaska_client, headers):
        create_response = alaska_client.create_bear({}, headers)
        print(f"Status: {create_response.status_code}")
        print(f"Body: {create_response.text}")
        assert create_response.status_code == 400, (
            f"Ожидали 400, получили {create_response.status_code}\n"
            f"Body: {create_response.text}\n"
        )

    @allure.title("Создание медведя с неизвестным типом")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_bear_unknown_type(self, alaska_client, headers):
        payload = {"bear_name": "dudeman", "bear_age": 10.0,
                   "bear_type": "PINK"}
        create_response = alaska_client.create_bear(payload, headers)
        print(f"Status: {create_response.status_code}")
        print(f"Body: {create_response.text}")

        assert create_response.status_code == 400, (
            f"Ожидали 400, получили {create_response.status_code}\n"
            f"Body: {create_response.text}\n"
        )

    @allure.title("Создание медведя с типом в другом регистре")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_bear_another_case(self, alaska_client, headers):
        payload = {"bear_name": "dudeman", "bear_age": 10.0,
                   "bear_type": "Black"}
        create_response = alaska_client.create_bear(payload, headers)
        print(f"Status: {create_response.status_code}")
        print(f"Body: {create_response.text}")

        assert create_response.status_code == 400, (
            f"Ожидали 400, получили {create_response.status_code}\n"
            f"Body: {create_response.text}\n"
        )

    @allure.title("Создание медведя с невалидным возрастом")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("age", [-1, 0, 53, 100])
    def test_create_bear_invalid_age(self, alaska_client, headers, age):
        payload = {"bear_type": BearTypes.BLACK.value,
                   "bear_name": "test", "bear_age": age}
        response = alaska_client.create_bear(payload, headers)

        assert response.status_code == 400, (
            f"Ожидали 400 для возраста {age}, получили {response.status_code}\n"
            f"Body: {response.text}\n"
        )

    @allure.title("Создание медведя со строкой в поле возраста")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_bear_age_as_string(self, alaska_client, headers):
        payload = {"bear_type": BearTypes.BLACK.value,
                   "bear_name": "test", "bear_age": "test"}
        response = alaska_client.create_bear(payload, headers)
        print(f"Status: {response.status_code}")
        print(f"Body: {response.text}")

        assert response.status_code == 400, (
            f"Ожидали 400, получили {response.status_code}\n"
            f"Body: {response.text}\n"
        )

    @allure.title("Создание медведя с именем из одного символа")
    @allure.severity(allure.severity_level.MINOR)
    def test_create_bear_single_char_name(self, alaska_client, headers):
        payload = {"bear_type": BearTypes.BLACK.value,
                   "bear_name": "a", "bear_age": 5.0}
        create_response = alaska_client.create_bear(payload, headers)
        print(f"Status: {create_response.status_code}")
        print(f"Body: {create_response.text}")

        assert create_response.status_code == 200, (
            f"Ожидали 200, получили {create_response.status_code}\n"
            f"Body: {create_response.text}\n"
        )

        bear_id = create_response.json()
        get_response = alaska_client.get_bear(bear_id, headers)
        bear = get_response.json()
        print(f"GET Status: {get_response.status_code}")
        print(f"GET Body: {get_response.text}")
        print(f"GET bear: {bear}")

        assert bear["bear_name"] == "a", (
            f"Ожидали имя a, получили {bear["bear_name"]}\n"
        )

    @allure.title("Создание медведя с лишними полями в payload")
    @allure.severity(allure.severity_level.MINOR)
    def test_create_bear_extra_fields(self, alaska_client, headers):
        payload = {
            "bear_type": BearTypes.BLACK.value,
            "bear_name": "test",
            "bear_age": 5.0,
            "surname": "testovich",
        }
        create_response = alaska_client.create_bear(payload, headers)
        print(f"Status: {create_response.status_code}")
        print(f"Body: {create_response.text}")

        assert create_response.status_code == 200, (
            f"Ожидали 200, получили {create_response.status_code}\n"
            f"Body: {create_response.text}\n"
        )

        bear_id = create_response.json()
        get_response = alaska_client.get_bear(bear_id, headers)
        bear = get_response.json()
        print(f"GET Status: {get_response.status_code}")
        print(f"GET Body: {get_response.text}")
        print(f"GET bear: {bear}")

        assert bear["bear_type"] == BearTypes.BLACK.value
        assert bear["bear_name"] == "TEST"
        assert bear["bear_age"] == 5.0
        assert "surname" not in bear, (
            f"Лишнее поле surname присутствует в ответе: {bear}\n"
        )


@allure.epic("Alaska Bear Service")
@allure.feature("GET Bears")
class TestGetBear:
    @allure.title("Получение всех медведей")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_all_bears(self, alaska_client, headers):
        payload1 = {
            "bear_type": BearTypes.BLACK.value,
            "bear_name": "test",
            "bear_age": 5.0
        }
        payload2 = {
            "bear_type": BearTypes.POLAR.value,
            "bear_name": "test",
            "bear_age": 5.0
        }

        id1 = alaska_client.create_bear(payload1, headers).json()
        id2 = alaska_client.create_bear(payload2, headers).json()

        get_response = alaska_client.get_all_bears(headers)
        print(f"GET Status: {get_response.status_code}")
        print(f"GET Body: {get_response.text}")
        bears = get_response.json()
        bear_ids = [bear["bear_id"] for bear in bears]

        assert id1 in bear_ids, (
            f"Медведь {id1} не найден в списке всех медведей\n"
            f"Все id: {bear_ids}\n"
        )
        assert id2 in bear_ids, (
            f"Медведь {id2} не найден в списке всех медведей\n"
            f"Все id: {bear_ids}\n"
        )

    @allure.title("Получение медведя по несуществующему id")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_bear_by_unexisting_id(self, alaska_client, headers):
        get_response = alaska_client.get_bear(0, headers)
        print(f"GET Body: {get_response.text}")
        assert get_response.status_code == 400, (
            f"Ожидали 400, получили {get_response.status_code}\n"
            f"Body: {get_response.text}\n"
        )

    @allure.title("Получение медведя с буквами в id")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_bear_by_str_id(self, alaska_client, headers):
        get_response = alaska_client.get_bear("abc", headers)
        print(f"GET Body: {get_response.text}")
        assert get_response.status_code == 400, (
            f"Ожидали 400, получили {get_response.status_code}\n"
            f"Body: {get_response.text}\n"
        )


@allure.epic("Alaska Bear Service")
@allure.feature("PUT Bears")
class TestUpdateBear:
    @allure.title("Успешное обновление медведя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_bear_success(self, alaska_client, valid_bear_payload, headers):
        bear_id = alaska_client.create_bear(valid_bear_payload, headers).json()

        updated_payload = {
            "bear_type": BearTypes.POLAR.value,
            "bear_name": "updated",
            "bear_age": 25.0,
        }
        update_response = alaska_client.update_bear(bear_id, updated_payload, headers)
        print(f"PUT Status: {update_response.status_code}")
        print(f"PUT Body: {update_response.text}")
        assert update_response.status_code == 200, (
            f"Ожидали 200, получили {update_response.status_code}\n"
            f"Body: {update_response.text}\n"
        )

        get_response = alaska_client.get_bear(bear_id, headers)
        bear = get_response.json()
        print(f"GET after PUT: {bear}")

        assert bear["bear_type"] == BearTypes.POLAR.value, (
            f"Тип не обновился. Ожидали {BearTypes.POLAR.value}, получили {bear["bear_type"]}\n"
        )
        assert bear["bear_name"] == "UPDATED", (
            f"Имя не обновилось. Ожидали UPDATED, получили {bear["bear_name"]}\n"
        )
        assert bear["bear_age"] == 25.0, (
            f"Возраст не обновился. Ожидали 25.0, получили {bear["bear_age"]}\n"
        )

    @allure.title("Частичное обновление - только имя")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_bear_only_name(self, alaska_client, valid_bear_payload, headers):
        bear_id = alaska_client.create_bear(valid_bear_payload, headers).json()

        update_response = alaska_client.update_bear(bear_id, {"bear_name": "newname"}, headers)
        print(f"PUT Status: {update_response.status_code}")
        print(f"PUT Body: {update_response.text}")
        assert update_response.status_code == 200

        bear = alaska_client.get_bear(bear_id, headers).json()
        print(f"GET after PUT: {bear}")
        assert bear["bear_name"] == "NEWNAME", (
            f"Имя не обновилось. Ожидали NEWNAME, получили {bear["bear_name"]}\n"
        )

    @allure.title("Частичное обновление - только возраст")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_bear_only_age(self, alaska_client, valid_bear_payload, headers):
        bear_id = alaska_client.create_bear(valid_bear_payload, headers).json()

        update_response = alaska_client.update_bear(bear_id, {"bear_age": 30.0}, headers)
        print(f"PUT Status: {update_response.status_code}")
        print(f"PUT Body: {update_response.text}")
        assert update_response.status_code == 200, (
            f"Ожидали 200, получили {update_response.status_code}\n"
            f"Body: {update_response.text}\n"
        )

        bear = alaska_client.get_bear(bear_id, headers).json()
        print(f"GET after PUT: {bear}")
        assert bear["bear_age"] == 30.0, (
            f"Возраст не обновился. Ожидали 30.0, получили {bear["bear_age"]}\n"
        )

    @allure.title("Частичное обновление - только тип")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_bear_only_type(self, alaska_client, valid_bear_payload, headers):
        bear_id = alaska_client.create_bear(valid_bear_payload, headers).json()

        update_response = alaska_client.update_bear(bear_id, {"bear_type": BearTypes.GUMMY.value}, headers)
        print(f"PUT Status: {update_response.status_code}")
        print(f"PUT Body: {update_response.text}")
        assert update_response.status_code == 200, (
            f"Ожидали 200, получили {update_response.status_code}\n"
            f"Body: {update_response.text}\n"
        )

        bear = alaska_client.get_bear(bear_id, headers).json()
        print(f"GET after PUT: {bear}")
        assert bear["bear_type"] == BearTypes.GUMMY.value, (
            f"Тип не обновился. Ожидали {BearTypes.GUMMY.value}, получили {bear["bear_type"]}\n"
        )

    @allure.title("Обновление медведя с пустым телом")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_bear_empty_body(self, alaska_client, valid_bear_payload, headers):
        bear_id = alaska_client.create_bear(valid_bear_payload, headers).json()

        update_response = alaska_client.update_bear(bear_id, {}, headers)
        print(f"PUT Status: {update_response.status_code}")
        print(f"PUT Body: {update_response.text}")
        assert update_response.status_code == 400, (
            f"Ожидали 400, получили {update_response.status_code}\n"
            f"Body: {update_response.text}\n"
        )

    @allure.title("Обновление медведя с невалидными данными")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_bear_invalid_data(self, alaska_client, valid_bear_payload, headers):
        bear_id = alaska_client.create_bear(valid_bear_payload, headers).json()

        invalid_payload = {"bear_type": "INVALID", "bear_age": -5}
        update_response = alaska_client.update_bear(bear_id, invalid_payload, headers)
        print(f"PUT Status: {update_response.status_code}")
        print(f"PUT Body: {update_response.text}")
        assert update_response.status_code == 400, (
            f"Ожидали 400, получили {update_response.status_code}\n"
            f"Body: {update_response.text}\n"
        )

    @allure.title("Обновление медведя по несуществующему id")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_bear_nonexistent_id(self, alaska_client, headers):
        payload = {"bear_type": BearTypes.BLACK.value, "bear_name": "ghost", "bear_age": 5.0}
        update_response = alaska_client.update_bear(99999, payload, headers)
        print(f"PUT Status: {update_response.status_code}")
        print(f"PUT Body: {update_response.text}")
        assert update_response.status_code == 404, (
            f"Ожидали 404, получили {update_response.status_code}\n"
            f"Body: {update_response.text}\n"
        )


@allure.epic("Alaska Bear Service")
@allure.feature("DELETE Bears")
class TestDeleteBear:
    @allure.title("Удаление всех медведей")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_all_bears(self, alaska_client, headers):
        payload1 = {"bear_type": BearTypes.BLACK.value, "bear_name": "first", "bear_age": 5.0}
        payload2 = {"bear_type": BearTypes.POLAR.value, "bear_name": "second", "bear_age": 10.0}
        alaska_client.create_bear(payload1, headers)
        alaska_client.create_bear(payload2, headers)

        delete_response = alaska_client.delete_all_bears(headers)
        print(f"DELETE Status: {delete_response.status_code}")
        print(f"DELETE Body: {delete_response.text}")
        assert delete_response.status_code == 200, (
            f"Ожидали 200, получили {delete_response.status_code}\n"
            f"Body: {delete_response.text}\n"
        )

        get_response = alaska_client.get_all_bears(headers)
        bears = get_response.json()
        print(f"GET after DELETE: {bears}")
        assert bears == [], (
            f"После удаления всех медведей список не пуст: {bears}\n"
        )

    @allure.title("Удаление медведя по id")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_bear_by_id(self, alaska_client, valid_bear_payload, headers):
        bear_id = alaska_client.create_bear(valid_bear_payload, headers).json()

        delete_response = alaska_client.delete_bear(bear_id, headers)
        print(f"DELETE Status: {delete_response.status_code}")
        print(f"DELETE Body: {delete_response.text}")
        assert delete_response.status_code == 200, (
            f"Ожидали 200, получили {delete_response.status_code}\n"
            f"Body: {delete_response.text}\n"
        )

        get_response = alaska_client.get_bear(bear_id, headers)
        print(f"GET after DELETE Status: {get_response.status_code}")
        print(f"GET after DELETE Body: {get_response.text}")
        assert get_response.status_code == 404, (
            f"Медведь {bear_id} всё ещё доступен после удаления. "
            f"Статус: {get_response.status_code}\n"
        )

    @allure.title("Удаление по несуществующему id")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_bear_nonexistent_id(self, alaska_client, headers):
        delete_response = alaska_client.delete_bear(99999, headers)
        print(f"DELETE Status: {delete_response.status_code}")
        print(f"DELETE Body: {delete_response.text}")
        assert delete_response.status_code == 404, (
            f"Ожидали 404, получили {delete_response.status_code}\n"
            f"Body: {delete_response.text}\n"
        )

    @allure.title("Удаление всех медведей когда база пуста")
    @allure.severity(allure.severity_level.MINOR)
    def test_delete_all_bears_when_empty(self, alaska_client, headers):
        delete_response = alaska_client.delete_all_bears(headers)
        print(f"DELETE Status: {delete_response.status_code}")
        print(f"DELETE Body: {delete_response.text}")
        assert delete_response.status_code == 200, (
            f"Ожидали 200, получили {delete_response.status_code}\n"
            f"Body: {delete_response.text}\n"
        )

    @allure.title("Удаление медведя с буквами в id")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_bear_letters_in_id(self, alaska_client, headers):
        delete_response = alaska_client.delete_bear("abc", headers)
        print(f"DELETE Status: {delete_response.status_code}")
        print(f"DELETE Body: {delete_response.text}")
        assert delete_response.status_code == 404, (
            f"Ожидали 404, получили {delete_response.status_code}\n"
            f"Body: {delete_response.text}\n"
        )

    @allure.title("Повторное удаление того же id дважды")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_bear_same_id_twice(self, alaska_client, valid_bear_payload, headers):
        bear_id = alaska_client.create_bear(valid_bear_payload, headers).json()

        first_delete = alaska_client.delete_bear(bear_id, headers)
        print(f"1st DELETE Status: {first_delete.status_code}")
        assert first_delete.status_code == 200

        second_delete = alaska_client.delete_bear(bear_id, headers)
        print(f"2nd DELETE Status: {second_delete.status_code}")
        print(f"2nd DELETE Body: {second_delete.text}")
        assert second_delete.status_code == 404, (
            f"Повторное удаление должно вернуть 404, получили {second_delete.status_code}\n"
            f"Body: {second_delete.text}\n"
        )
