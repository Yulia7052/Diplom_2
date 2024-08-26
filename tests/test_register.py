import requests
import random
import allure
import test_data


class TestRegister:

    @allure.description('Можно зарегистрировать нового пользователя')
    @allure.title('Проверка на регистрацию нового пользователя')
    def test_register_new_user(self):
        response = requests.post(test_data.register_url,
                                 data={"email": test_data.user_email + str(random.randint(100000, 1000000)), "password": test_data.user_password, "name": test_data.user_name})
        data = response.json()

        assert response.status_code == 200
        assert data["success"] == True

    @allure.description('Существующего пользователя нельзя зарегистрировать')
    @allure.title('Проверка на невозможность регистрации существующего пользователя')
    def test_register_exists_user(self):
        response = requests.post(test_data.register_url,
                                 data={"email": test_data.user_email, "password": test_data.user_password, "name": test_data.user_name})
        data = response.json()

        assert response.status_code == 403
        assert data["success"] == False
        assert data["message"] == test_data.message_incorrect_register_user

    @allure.description('Нельзя зарегистрировать нового пользователя без заполнения обязательных полей')
    @allure.title('Проверка на невозможность регистрации пользователя без заполнения обязательных полей')
    def test_register_user_without_fields(self):
        response = requests.post(test_data.register_url,
                                 data={"email": test_data.user_email, "password": test_data.user_password})
        data = response.json()
        assert response.status_code == 403
        assert data["success"] == False
        assert data["message"] == test_data.message_incorrect_register_data
