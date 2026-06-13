import requests
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

url = "https://playground.learnqa.ru/api/long_redirect"
response = requests.get(url, allow_redirects=True)

redirect_count = len(response.history)
final_url = response.url

print(f"Количество редиректов: {redirect_count}")
print(f"Итоговый URL: {final_url}")