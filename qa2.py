import requests
import json
import pytest
import random
import string

BASE_URL = "https://reqres.in/api"
API_KEY = "reqres-free-v1"

def get_headers():
    return {
        "x-api-key": API_KEY
    }

created_user_id = None
test_user_data = None

def generate_random_string(length=8):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def log_request_info(method, url, data=None, response=None):
    print(f"\n=== {method} Request to {url} ===")
    if data:
        print(f"Request body: {json.dumps(data, indent=2)}")
    if response:
        print(f"Status code: {response.status_code}")
        try:
            print(f"Response body: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"Response body: {response.text}")
    print("=" * 50)

def test_get_users_list():
    url = f"{BASE_URL}/users"
    response = requests.get(url, headers=get_headers())
    log_request_info("GET", url, response=response)
    assert response.status_code == 200, f"Ожидался статус-код 200, получен {response.status_code}"
    response_data = response.json()
    assert 'data' in response_data, "Ответ не содержит ключ 'data'"
    assert 'page' in response_data, "Ответ не содержит ключ 'page'"
    assert len(response_data['data']) > 0, "Список пользователей пуст"
    for user in response_data['data']:
        assert 'id' in user, "Пользователь не имеет поля 'id'"
        assert 'email' in user, "Пользователь не имеет поля 'email'"
        assert 'first_name' in user, "Пользователь не имеет поля 'first_name'"
        assert 'last_name' in user, "Пользователь не имеет поля 'last_name'"
        assert '@' in user['email'], f"Email пользователя {user['id']} не содержит символ @"

def test_get_single_user():
    user_id = 2
    url = f"{BASE_URL}/users/{user_id}"
    response = requests.get(url, headers=get_headers())
    log_request_info("GET", url, response=response)
    assert response.status_code == 200, f"Ожидался статус-код 200, получен {response.status_code}"
    response_data = response.json()
    assert 'data' in response_data, "Ответ не содержит ключ 'data'"
    user_data = response_data['data']
    assert user_data['id'] == user_id, f"ID пользователя в ответе ({user_data['id']}) не соответствует запрошенному ({user_id})"
    assert 'email' in user_data, "Данные пользователя не содержат email"
    assert 'first_name' in user_data, "Данные пользователя не содержат first_name"
    assert 'last_name' in user_data, "Данные пользователя не содержат last_name"
    assert '@' in user_data['email'], f"Email пользователя не содержит символ @: {user_data['email']}"
    assert '.' in user_data['email'].split('@')[-1], f"Email пользователя не содержит домен после @: {user_data['email']}"

def test_create_user():
    global created_user_id, test_user_data
    test_user_data = {
        "name": f"Test User {generate_random_string()}",
        "job": "QA Engineer"
    }
    url = f"{BASE_URL}/users"
    response = requests.post(url, json=test_user_data, headers=get_headers())
    log_request_info("POST", url, test_user_data, response)
    assert response.status_code == 201, f"Ожидался статус-код 201, получен {response.status_code}"
    response_data = response.json()
    assert 'id' in response_data, "Ответ не содержит ID созданного пользователя"
    assert 'name' in response_data, "Ответ не содержит имя пользователя"
    assert response_data['name'] == test_user_data['name'], "Имя пользователя в ответе не соответствует отправленному"
    created_user_id = response_data['id']

def test_update_user_put():
    global test_user_data
    if not created_user_id:
        pytest.skip("Пропуск теста, так как ID пользователя не был получен")
    updated_user_data = {
        "name": f"Updated User {generate_random_string()}",
        "job": "Senior QA Engineer"
    }
    url = f"{BASE_URL}/users/{created_user_id}"
    response = requests.put(url, json=updated_user_data, headers=get_headers())
    log_request_info("PUT", url, updated_user_data, response)
    assert response.status_code == 200, f"Ожидался статус-код 200, получен {response.status_code}"
    response_data = response.json()
    assert 'name' in response_data, "Ответ не содержит имя пользователя"
    assert response_data['name'] == updated_user_data['name'], "Имя пользователя в ответе не соответствует отправленному"
    test_user_data = updated_user_data

def test_update_user_patch():
    if not created_user_id:
        pytest.skip("Пропуск теста, так как ID пользователя не был получен")
    patch_data = {
        "job": "Lead QA Engineer"
    }
    url = f"{BASE_URL}/users/{created_user_id}"
    response = requests.patch(url, json=patch_data, headers=get_headers())
    log_request_info("PATCH", url, patch_data, response)
    assert response.status_code == 200, f"Ожидался статус-код 200, получен {response.status_code}"
    response_data = response.json()
    assert 'job' in response_data, "Ответ не содержит должность пользователя"
    assert response_data['job'] == patch_data['job'], "Должность пользователя в ответе не соответствует отправленной"

def test_delete_user():
    if not created_user_id:
        pytest.skip("Пропуск теста, так как ID пользователя не был получен")
    url = f"{BASE_URL}/users/{created_user_id}"
    response = requests.delete(url, headers=get_headers())
    log_request_info("DELETE", url, response=response)
    assert response.status_code == 204, f"Ожидался статус-код 204, получен {response.status_code}"
    assert response.text == "", "Ответ на DELETE запрос должен быть пустым"

def test_get_nonexistent_user():
    user_id = 999
    url = f"{BASE_URL}/users/{user_id}"
    response = requests.get(url, headers=get_headers())
    log_request_info("GET", url, response=response)
    assert response.status_code == 404, f"Ожидался статус-код 404, получен {response.status_code}"

def test_create_user_invalid_data():
    empty_data = {}
    url = f"{BASE_URL}/users"
    response = requests.post(url, json=empty_data, headers=get_headers())
    log_request_info("POST", url, empty_data, response)
    assert response.status_code == 201, f"Ожидался статус-код 201, получен {response.status_code}"

def test_register_user_successful():
    register_data = {
        "email": "eve.holt@reqres.in",
        "password": "pistol"
    }
    url = f"{BASE_URL}/register"
    response = requests.post(url, json=register_data, headers=get_headers())
    log_request_info("POST", url, register_data, response)
    assert response.status_code == 200, f"Ожидался статус-код 200, получен {response.status_code}"
    response_data = response.json()
    assert 'token' in response_data, "Ответ не содержит токен"
    assert 'id' in response_data, "Ответ не содержит ID пользователя"

def test_register_user_unsuccessful():
    incomplete_data = {
        "email": "sydney@fife"
    }
    url = f"{BASE_URL}/register"
    response = requests.post(url, json=incomplete_data, headers=get_headers())
    log_request_info("POST", url, incomplete_data, response)
    assert response.status_code == 400, f"Ожидался статус-код 400, получен {response.status_code}"
    response_data = response.json()
    assert 'error' in response_data, "Ответ не содержит сообщение об ошибке"

def test_get_users_with_pagination():
    page = 2
    per_page = 3
    url = f"{BASE_URL}/users?page={page}&per_page={per_page}"
    response = requests.get(url, headers=get_headers())
    log_request_info("GET", url, response=response)
    assert response.status_code == 200, f"Ожидался статус-код 200, получен {response.status_code}"
    response_data = response.json()
    assert 'page' in response_data, "Ответ не содержит поле 'page'"
    assert 'per_page' in response_data, "Ответ не содержит поле 'per_page'"
    assert 'total' in response_data, "Ответ не содержит поле 'total'"
    assert 'total_pages' in response_data, "Ответ не содержит поле 'total_pages'"
    assert 'data' in response_data, "Ответ не содержит поле 'data'"
    assert response_data['page'] == page, f"Номер страницы не соответствует запрошенному ({page} != {response_data['page']})"
    assert response_data['per_page'] == per_page, f"Количество элементов на странице не соответствует запрошенному ({per_page} != {response_data['per_page']})"
    assert len(response_data['data']) == per_page, f"Количество пользователей на странице не соответствует per_page ({len(response_data['data'])} != {per_page})"
    expected_total_pages = (response_data['total'] + per_page - 1) // per_page
    assert response_data['total_pages'] == expected_total_pages, f"Общее количество страниц вычислено неверно ({response_data['total_pages']} != {expected_total_pages})"
    for user in response_data['data']:
        assert 'id' in user, "Пользователь не имеет поля 'id'"
        assert 'email' in user, "Пользователь не имеет поля 'email'"
        assert 'first_name' in user, "Пользователь не имеет поля 'first_name'"
        assert 'last_name' in user, "Пользователь не имеет поля 'last_name'"
        assert '@' in user['email'], f"Email пользователя {user['id']} не содержит символ @"

def test_login_successful():
    login_data = {
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    }
    url = f"{BASE_URL}/login"
    response = requests.post(url, json=login_data, headers=get_headers())
    log_request_info("POST", url, login_data, response)
    assert response.status_code == 200, f"Ожидался статус-код 200, получен {response.status_code}"
    response_data = response.json()
    assert 'token' in response_data, "Ответ не содержит токен авторизации"
    assert isinstance(response_data['token'], str), "Токен должен быть строкой"
    assert len(response_data['token']) > 0, "Токен не должен быть пустым"
    if 'id' in response_data:
        assert isinstance(response_data['id'], int), "ID пользователя должен быть числом"
    print("Успешная авторизация. Получен токен:", response_data['token'])

if __name__ == "__main__":
    print("Запуск тестов API...")
    test_get_users_list()
    test_get_single_user()
    test_create_user()
    test_update_user_put()
    test_update_user_patch()
    test_delete_user()
    test_get_nonexistent_user()
    test_create_user_invalid_data()
    test_register_user_successful()
    test_register_user_unsuccessful()
    print("\nВсе тесты выполнены")