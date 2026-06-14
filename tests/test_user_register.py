import allure
import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

@allure.epic("Тестирование API LearnQA")
@allure.feature("Управление пользователями")
class TestUserRegister(BaseCase):

    @allure.story("Регистрация пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Позитивный тест: создание пользователя с валидными данными")
    @allure.tag("positive", "smoke")
    @allure.link("https://playground.learnqa.ru/api/user/", name="API Docs")
    def test_create_user_successfully(self):
        # ... код теста ...
        pass

    @allure.story("Регистрация пользователя")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Негативный тест: email без символа @")
    @allure.tag("negative", "validation")
    @allure.issue("BUG-123", name="Багрепорт на отсутствие валидации email")
    def test_create_user_invalid_email_no_at_sign(self):
        # ... код теста ...
        pass

    @allure.story("Регистрация пользователя")
    @allure.severity(allure.severity_level.MINOR)
    @allure.description("Проверка обязательности всех полей при регистрации")
    @allure.tag("negative", "parametrized")
    @pytest.mark.parametrize("missing_field", ["email", "password", "username", "firstName", "lastName"])
    @allure.parameter("Отсутствующее поле", missing_field)
    def test_create_user_missing_field(self, missing_field):
        # ... код теста ...
        pass