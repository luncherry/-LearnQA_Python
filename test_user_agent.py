import pytest
import requests

# Загружаем тестовые данные из gist (сырой JSON)
GIST_URL = "https://gist.githubusercontent.com/KotovVitaliy/138894aa5b6fa442163561b5db6e2e6/raw/664c23e6b2b7023f68b8f7e2ca1f04c3aa7a600a/user_agents.json"

def get_test_data():
    """Загружает список тестовых случаев из Gist."""
    response = requests.get(GIST_URL)
    response.raise_for_status()
    data = response.json()
    # Преобразуем в список кортежей (user_agent, expected)
    test_cases = []
    for item in data:
        user_agent = item["user_agent"]
        expected = item["expected"]
        test_cases.append((user_agent, expected))
    return test_cases

@pytest.mark.parametrize("user_agent, expected", get_test_data())
def test_user_agent_check(user_agent, expected):
    url = "https://playground.learnqa.ru/ajax/api/user_agent_check"
    response = requests.get(url, headers={"User-Agent": user_agent})
    assert response.status_code == 200, f"Неверный статус: {response.status_code}"
    actual = response.json()
    
    # Проверяем каждый параметр
    errors = []
    for field in ["device", "browser", "platform"]:
        if actual.get(field) != expected.get(field):
            errors.append(f"{field}: ожидалось '{expected.get(field)}', получено '{actual.get(field)}'")
    
    assert not errors, f"Несовпадения для User-Agent: {user_agent}\n" + "\n".join(errors)