import pytest
import requests
from datetime import datetime

# Если у вас есть готовые BaseCase и Assertions – используйте их.
# Здесь я привожу самостоятельные тесты без внешних зависимостей.

class TestUserRegister:

    def generate_unique_email(self):
        """Генерирует уникальный email для позитивного теста"""
        base = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%dY%H%M%S")
        return f"{base}{random_part}@{domain}"

    # --- Позитивный тест ---
    def test_create_user_successfully(self):
        email = self.generate_unique_email()
        data = {
            "email": email,
            "password": "123",
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa"
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        assert response.status_code == 200
        assert "id" in response.json(), "Ответ не содержит id пользователя"

    # --- 1. Некорректный email (без @) ---
    def test_create_user_invalid_email_no_at_sign(self):
        email = "invalidemailexample.com"  # нет символа @
        data = {
            "email": email,
            "password": "123",
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa"
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        assert response.status_code == 400
        assert response.json().get("error") == "Invalid email format", \
            "Ожидалась ошибка о неверном формате email"

    # --- 2. Отсутствие одного из обязательных полей (параметризация) ---
    @pytest.mark.parametrize("missing_field", ["email", "password", "username", "firstName", "lastName"])
    def test_create_user_missing_field(self, missing_field):
        # Базовые корректные данные
        valid_data = {
            "email": self.generate_unique_email(),
            "password": "123",
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa"
        }
        # Удаляем проверяемое поле
        test_data = valid_data.copy()
        del test_data[missing_field]

        response = requests.post("https://playground.learnqa.ru/api/user/", data=test_data)
        assert response.status_code == 400
        error_msg = response.json().get("error", "")
        assert "missing" in error_msg.lower() or "required" in error_msg.lower(), \
            f"Ожидалась ошибка о пропущенном поле, поле: {missing_field}"

    # --- 3. Имя длиной в 1 символ ---
    def test_create_user_very_short_name(self):
        data = {
            "email": self.generate_unique_email(),
            "password": "123",
            "username": "a",  # один символ
            "firstName": "learnqa",
            "lastName": "learnqa"
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        # Ожидается ошибка валидации (обычно 400)
        assert response.status_code == 400
        assert "short" in response.json().get("error", "").lower() or \
               "length" in response.json().get("error", "").lower(), \
               "Не пришла ошибка о слишком коротком имени"

    # --- 4. Имя длиннее 250 символов ---
    def test_create_user_very_long_name(self):
        long_name = "a" * 251  # 251 символ
        data = {
            "email": self.generate_unique_email(),
            "password": "123",
            "username": long_name,
            "firstName": "learnqa",
            "lastName": "learnqa"
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        assert response.status_code == 400
        assert "long" in response.json().get("error", "").lower() or \
               "length" in response.json().get("error", "").lower(), \
               "Не пришла ошибка о слишком длинном имени"