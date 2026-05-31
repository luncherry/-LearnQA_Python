import requests
url = "https://playground.learnqa.ru/api/get_text"
response = requests.get(url)
# Проверяем статус ответа (по желанию)
response.raise_for_status()
# Выводим содержимое текста ответа
print(response.text)