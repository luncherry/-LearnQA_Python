import json

class Assertions:
    @staticmethod
    def assert_json_value_by_name(response, name, expected_value, error_message):
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            assert False, f"Ответ не является JSON. Текст: {response.text}"
        assert name in response_json, f"В ответе нет поля '{name}'. JSON: {response_json}"
        assert response_json[name] == expected_value, error_message

    @staticmethod
    def assert_json_has_key(response, name):
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            assert False, f"Ответ не является JSON. Текст: {response.text}"
        assert name in response_json, f"В ответе нет ключа '{name}'. JSON: {response_json}"

    @staticmethod
    def assert_json_has_keys(response, names):
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            assert False, f"Ответ не является JSON. Текст: {response.text}"
        for name in names:
            assert name in response_json, f"В ответе нет ключа '{name}'. JSON: {response_json}"

    @staticmethod
    def assert_json_has_not_key(response, name):
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            assert False, f"Ответ не является JSON. Текст: {response.text}"
        assert name not in response_json, f"В ответе не должно быть ключа '{name}', но он есть. JSON: {response_json}"

    @staticmethod
    def assert_status_code(response, expected_status_code):
        assert response.status_code == expected_status_code, \
            f"Неверный статус-код. Ожидалось: {expected_status_code}, получено: {response.status_code}"