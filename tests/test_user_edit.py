import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserEdit(BaseCase):

    # ---- Позитивный тест (для справки) ----
    def test_edit_user_positive(self):
        # Сначала создаём пользователя
        register_data = self.prepare_registration_data()
        response_create = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)
        Assertions.assert_code_status(response_create, 200)
        user_id = self.get_json_value(response_create, "id")

        # Авторизуемся
        login_data = {
            'email': register_data['email'],
            'password': register_data['password']
        }
        response_login = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        # Редактируем firstName
        new_name = "UpdatedName"
        edit_data = {"firstName": new_name}
        response_edit = requests.put(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data=edit_data
        )
        Assertions.assert_code_status(response_edit, 200)

        # Проверяем, что имя изменилось
        response_get = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_json_value_by_name(response_get, "firstName", new_name, "Имя не обновилось")

    # ---- Негативные тесты ----
    def test_edit_user_not_authorized(self):
        """Попытка изменить данные без авторизации (нет куки и токена)"""
        # Создаём пользователя
        register_data = self.prepare_registration_data()
        response_create = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)
        Assertions.assert_code_status(response_create, 200)
        user_id = self.get_json_value(response_create, "id")

        # Пытаемся изменить без авторизации
        edit_data = {"username": "Hacker"}
        response_edit = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}", data=edit_data)

        # Ожидаем ошибку авторизации (401 или 400)
        Assertions.assert_code_status(response_edit, 401)   # обычно неавторизованный запрос возвращает 401
        # Дополнительно проверим, что данные не изменились – можно сделать запрос без авторизации,
        # но он вернёт только username. Лучше проверить через авторизацию тем же пользователем.
        # Авторизуемся исходным пользователем и проверим, что username не изменился
        login_data = {
            'email': register_data['email'],
            'password': register_data['password']
        }
        response_login = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")
        response_get = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_json_value_by_name(response_get, "username", register_data['username'], "Username изменился без авторизации")

    def test_edit_user_authorized_as_another_user(self):
        """Авторизуемся одним пользователем, пытаемся изменить данные другого"""
        # Создаём первого пользователя (будет авторизован)
        user1_data = self.prepare_registration_data()
        response_user1 = requests.post("https://playground.learnqa.ru/api/user/", data=user1_data)
        Assertions.assert_code_status(response_user1, 200)
        user1_id = self.get_json_value(response_user1, "id")

        # Создаём второго пользователя (чьи данные будем пытаться изменить)
        user2_data = self.prepare_registration_data()
        response_user2 = requests.post("https://playground.learnqa.ru/api/user/", data=user2_data)
        Assertions.assert_code_status(response_user2, 200)
        user2_id = self.get_json_value(response_user2, "id")

        # Авторизуемся первым пользователем
        login_data = {
            'email': user1_data['email'],
            'password': user1_data['password']
        }
        response_login = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        # Пытаемся изменить данные второго пользователя
        new_username = "MaliciousUpdate"
        edit_data = {"username": new_username}
        response_edit = requests.put(
            f"https://playground.learnqa.ru/api/user/{user2_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data=edit_data
        )
        # Ожидаем ошибку доступа (403 или 400)
        Assertions.assert_code_status(response_edit, 403)  # обычно запрещено

        # Проверяем, что данные второго пользователя не изменились (авторизуемся им самим)
        login_data2 = {
            'email': user2_data['email'],
            'password': user2_data['password']
        }
        response_login2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data2)
        auth_sid2 = self.get_cookie(response_login2, "auth_sid")
        token2 = self.get_header(response_login2, "x-csrf-token")
        response_get = requests.get(
            f"https://playground.learnqa.ru/api/user/{user2_id}",
            headers={"x-csrf-token": token2},
            cookies={"auth_sid": auth_sid2}
        )
        Assertions.assert_json_value_by_name(response_get, "username", user2_data['username'], "Username второго пользователя изменился")

    def test_edit_user_invalid_email_no_at_sign(self):
        """Попытка изменить email на некорректный (без @) под авторизацией того же пользователя"""
        # Создаём пользователя
        register_data = self.prepare_registration_data()
        response_create = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)
        Assertions.assert_code_status(response_create, 200)
        user_id = self.get_json_value(response_create, "id")

        # Авторизуемся
        login_data = {
            'email': register_data['email'],
            'password': register_data['password']
        }
        response_login = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        # Пытаемся обновить email на некорректный
        invalid_email = "invalidemailexample.com"
        edit_data = {"email": invalid_email}
        response_edit = requests.put(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data=edit_data
        )
        # Ожидаем ошибку валидации (400)
        Assertions.assert_code_status(response_edit, 400)
        Assertions.assert_json_value_by_name(response_edit, "error", "Invalid email format", "Не пришла ошибка о неверном формате email")

    def test_edit_user_short_firstname(self):
        """Попытка изменить firstName на слишком короткое (1 символ)"""
        # Создаём пользователя
        register_data = self.prepare_registration_data()
        response_create = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)
        Assertions.assert_code_status(response_create, 200)
        user_id = self.get_json_value(response_create, "id")

        # Авторизуемся
        login_data = {
            'email': register_data['email'],
            'password': register_data['password']
        }
        response_login = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        # Пытаемся установить firstName = "A"
        short_name = "A"
        edit_data = {"firstName": short_name}
        response_edit = requests.put(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data=edit_data
        )
        # Ожидаем ошибку валидации (400)
        Assertions.assert_code_status(response_edit, 400)
        # Можно проверить текст ошибки (если API возвращает что-то конкретное)
        error_text = response_edit.json().get("error", "")
        assert "short" in error_text.lower() or "length" in error_text.lower(), "Не пришла ошибка о слишком коротком имени"