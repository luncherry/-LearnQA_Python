import requests
import sys
import io


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

URL = "https://playground.learnqa.ru/ajax/api/compare_query_type"


print("1. Запрос GET без параметра method")
response = requests.get(URL)
print(f"   Статус: {response.status_code}")
print(f"   Ответ: {response.text}\n")


print("2. Запрос HEAD (не входит в POST, GET, PUT, DELETE)")
try:
    # HEAD-запрос не имеет тела, поэтому .text будет пустым
    response_head = requests.head(URL, params={"method": "HEAD"})
    print(f"   Статус: {response_head.status_code}")
    print(f"   Ответ: {response_head.text} (у HEAD обычно нет тела)\n")
except Exception as e:
    print(f"   Ошибка: {e}\n")

print("3. Запрос GET с method=GET (правильное сочетание)")
response_correct = requests.get(URL, params={"method": "GET"})
print(f"   Статус: {response_correct.status_code}")
print(f"   Ответ: {response_correct.text}\n")

print("4. Перебор всех сочетаний реальных методов и параметра method")
http_methods = ["GET", "POST", "PUT", "DELETE"]
method_values = ["GET", "POST", "PUT", "DELETE"]

print("\nТаблица результатов (реальный метод -> значение param 'method'):\n")
for real_method in http_methods:
    for param_method in method_values:
        # Выбираем способ передачи параметра
        if real_method == "GET":
            resp = requests.get(URL, params={"method": param_method})
        elif real_method == "POST":
            resp = requests.post(URL, data={"method": param_method})
        elif real_method == "PUT":
            resp = requests.put(URL, data={"method": param_method})
        elif real_method == "DELETE":
            resp = requests.delete(URL, data={"method": param_method})
        
        # Анализируем ответ
        is_success = "success" in resp.text.lower()
        match = (real_method == param_method)
        

        print(f"  {real_method:6} -> method={param_method:6} | статус: {resp.status_code} | ответ: {resp.text:20} | совпадает? {match}")
        
        if match and not is_success:
            print(f"      Аномалия: методы совпадают ({real_method}), но сервер ответил ошибкой!")
        if not match and is_success:
            print(f"      Аномалия: методы НЕ совпадают ({real_method} != {param_method}), но сервер ответил успехом!")

print("\nАнализ завершён.")