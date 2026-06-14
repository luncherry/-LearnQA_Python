import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserDelete(BaseCase):

    # 1. Попытка удалить пользователя с ID 2 (зарезервированного)
    def test_delete_user_id_2_forbidden(self):
        # Данные для авторизации под пользователем ID 2
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response_login = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        Assertions.assert_code_status(response_login, 200)
        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        # Пытаемся удалить пользователя с ID 2
        response_delete = requests.delete(
            "https://playground.learnqa.ru/api/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        # Ожидаем, что удаление запрещено (статус 400 или 403)
        # По заданию: система не даст удалить
        Assertions.assert_code_status(response_delete, 400)  # обычно возвращает 400

    # 2. Позитивный тест: создать пользователя, удалить, проверить отсутствие
    def test_delete_just_created_user_success(self):
        # Регистрируем пользователя
        register_data = self.prepare_registration_data()
        response_create = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)
        Assertions.assert_code_status(response_create, 200)
        user_id = self.get_json_value(response_create, "id")

        # Авторизуемся под ним
        login_data = {
            'email': register_data['email'],
            'password': register_data['password']
        }
        response_login = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        Assertions.assert_code_status(response_login, 200)
        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        # Удаляем пользователя
        response_delete = requests.delete(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_code_status(response_delete, 200)

        # Пробуем получить данные удалённого пользователя (авторизуясь им же, но он удалён)
        # Либо просто делаем неавторизованный запрос – он вернёт только username, но сам пользователь должен отсутствовать.
        # Лучше проверить, что при попытке авторизоваться под ним – ошибка.
        # Но по заданию: "попробовать получить его данные по ID и убедиться, что пользователь действительно удален".
        # Сделаем запрос без авторизации (так как авторизация через удалённого пользователя невозможна).
        response_get = requests.get(f"https://playground.learnqa.ru/api/user/{user_id}")
        # Ожидаем, что пользователь не найден (404) или ошибка авторизации (401)
        # API обычно возвращает 404 для несуществующего пользователя
        # Для этого теста важно, что данные не получены (нет username и т.д.)
        # Проверим, что статус не 200, и в ответе нет ключа "username" (или есть "error")
        assert response_get.status_code != 200, "Пользователь всё ещё существует"
        # Можно также проверить, что в ответе нет полей пользователя
        # Если статус 400/404, то json может быть с ошибкой
        # Альтернатива: попробовать авторизоваться удалённым пользователем – должна быть ошибка
        login_deleted = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        Assertions.assert_code_status(login_deleted, 400)  # неверные данные или пользователь удалён

    # 3. Негативный: удалить пользователя, будучи авторизованным другим пользователем
    def test_delete_user_authorized_as_another_user(self):
        # Создаём пользователя A (будет авторизован)
        user_a_data = self.prepare_registration_data()
        response_a = requests.post("https://playground.learnqa.ru/api/user/", data=user_a_data)
        Assertions.assert_code_status(response_a, 200)
        user_a_id = self.get_json_value(response_a, "id")

        # Создаём пользователя B (кого будем пытаться удалить)
        user_b_data = self.prepare_registration_data()
        response_b = requests.post("https://playground.learnqa.ru/api/user/", data=user_b_data)
        Assertions.assert_code_status(response_b, 200)
        user_b_id = self.get_json_value(response_b, "id")

        # Авторизуемся пользователем A
        login_a = {
            'email': user_a_data['email'],
            'password': user_a_data['password']
        }
        response_login_a = requests.post("https://playground.learnqa.ru/api/user/login", data=login_a)
        Assertions.assert_code_status(response_login_a, 200)
        auth_sid_a = self.get_cookie(response_login_a, "auth_sid")
        token_a = self.get_header(response_login_a, "x-csrf-token")

        # Пытаемся удалить пользователя B
        response_delete = requests.delete(
            f"https://playground.learnqa.ru/api/user/{user_b_id}",
            headers={"x-csrf-token": token_a},
            cookies={"auth_sid": auth_sid_a}
        )
        # Ожидаем ошибку (403 или 400)
        Assertions.assert_code_status(response_delete, 400)  # обычно 400 - forbidden

        # Убеждаемся, что пользователь B всё ещё существует (авторизуемся под ним)
        login_b = {
            'email': user_b_data['email'],
            'password': user_b_data['password']
        }
        response_login_b = requests.post("https://playground.learnqa.ru/api/user/login", data=login_b)
        Assertions.assert_code_status(response_login_b, 200)
        # Можем также получить его данные
        auth_sid_b = self.get_cookie(response_login_b, "auth_sid")
        token_b = self.get_header(response_login_b, "x-csrf-token")
        response_get_b = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_b_id}",
            headers={"x-csrf-token": token_b},
            cookies={"auth_sid": auth_sid_b}
        )
        Assertions.assert_code_status(response_get_b, 200)
        Assertions.assert_json_has_key(response_get_b, "username")