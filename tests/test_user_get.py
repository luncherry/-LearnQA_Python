import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        response = requests.get("https://playground.learnqa.ru/api/user/2")

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_has_key(response2, "username")
        Assertions.assert_json_has_key(response2, "email")
        Assertions.assert_json_has_key(response2, "firstName")
        Assertions.assert_json_has_key(response2, "lastName")

    def test_get_user_details_auth_as_another_user(self):
        # Регистрируем первого пользователя (тот, под кем будем авторизоваться)
        register_data1 = self.prepare_registration_data()
        response_register1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data1)
        Assertions.assert_code_status(response_register1, 200)
        user1_id = self.get_json_value(response_register1, "id")

        # Регистрируем второго пользователя (чьи данные будем запрашивать)
        register_data2 = self.prepare_registration_data()
        response_register2 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data2)
        Assertions.assert_code_status(response_register2, 200)
        user2_id = self.get_json_value(response_register2, "id")

        # Авторизуемся первым пользователем
        login_data = {
            'email': register_data1['email'],
            'password': register_data1['password']
        }
        response_login = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        Assertions.assert_code_status(response_login, 200)
        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        # Запрашиваем данные второго пользователя, используя авторизацию первого
        response_get = requests.get(
            f"https://playground.learnqa.ru/api/user/{user2_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        # Проверяем, что в ответе только username (как при неавторизованном запросе)
        Assertions.assert_json_has_key(response_get, "username")
        Assertions.assert_json_has_not_key(response_get, "email")
        Assertions.assert_json_has_not_key(response_get, "firstName")
        Assertions.assert_json_has_not_key(response_get, "lastName")