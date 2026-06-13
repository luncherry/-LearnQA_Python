import requests
import pytest

def test_homework_header():
    url = "https://playground.learnqa.ru/api/homework_header"
    response = requests.get(url)

    # Выводим все заголовки для визуального контроля (ключ -s в pytest)
    print("\n=== Заголовки ответа ===")
    for header, value in response.headers.items():
        print(f"{header}: {value}")

    # Извлекаем интересующий заголовок (название может быть 'x-secret-homework-header')
    # Вы можете сначала запустить тест с print, чтобы увидеть реальное имя заголовка,
    # а затем зафиксировать его в assert.
    secret_header = response.headers.get("x-secret-homework-header")

    # Проверяем, что заголовок существует и имеет ожидаемое значение
    # (значение вы также узнаете из print)
    assert secret_header is not None, "Заголовок 'x-secret-homework-header' отсутствует в ответе"
    assert secret_header == "SomeSecretValue", f"Неверное значение заголовка: {secret_header}"

    # Альтернативно, если имя заголовка другое, можно заменить на то, что увидите в print