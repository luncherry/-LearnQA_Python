import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserAuth(BaseCase):
    def test_auth_user(self):
        url = "https://playground.learnqa.ru/api/user/login"
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }
        response = requests.post(url, data=data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "user_id")
        Assertions.assert_json_value_by_name(
            response,
            "user_id",
            1,
            "ID пользователя не совпадает с ожидаемым"
        )