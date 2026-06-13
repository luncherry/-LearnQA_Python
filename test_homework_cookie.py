import requests
import pytest

def test_homework_cookie():
    """
    Тест для проверки cookie, возвращаемой методом https://playground.learnqa.ru/api/homework_cookie
    """
    url = "https://playground.learnqa.ru/api/homework_cookie"
    response = requests.get(url)


    print(f"\nСтатус-код ответа: {response.status_code}")
    print(f"Заголовки ответа: {response.headers}")
    print(f"Cookies в ответе: {response.cookies}")

    # Получаем словарь с cookie
    cookies_dict = response.cookies.get_dict()
    print(f"Словарь cookie: {cookies_dict}")

    # Проверяем, что cookie присутствует в ответе
    assert cookies_dict, "В ответе отсутствуют cookie"


    cookie_name = list(cookies_dict.keys())[0] if cookies_dict else None
    cookie_value = cookies_dict.get(cookie_name) if cookie_name else None

    print(f"Имя cookie: {cookie_name}")
    print(f"Значение cookie: {cookie_value}")


    assert cookie_name, "Имя cookie отсутствует или пустое"
    assert cookie_value, "Значение cookie отсутствует или пустое"

