import requests
import random
import allure


class TestRegister:
    register_url = "https://stellarburgers.nomoreparties.site/api/auth/register"
    user_email = "bulochka@yandex.ru"
    user_password = "5469"
    user_name = "bulka56"

    @allure.description('Можно зарегистрировать нового пользователя')
    @allure.title('Проверка на регистрацию нового пользователя')
    def test_register_new_user(self):
        response = requests.post(self.register_url,
                                 data={"email": self.user_email + str(random.randint(100000, 1000000)), "password": self.user_password, "name": self.user_name})
        data = response.json()

        assert response.status_code == 200
        assert data["success"] == True

    @allure.description('Существующего пользователя нельзя зарегистрировать')
    @allure.title('Проверка на невозможность регистрации существующего пользователя')
    def test_register_exists_user(self):
        response = requests.post(self.register_url,
                                 data={"email": self.user_email, "password": self.user_password, "name": self.user_name})
        data = response.json()

        assert response.status_code == 403
        assert data["success"] == False
        assert data["message"] == "User already exists"

    @allure.description('Нельзя зарегистрировать нового пользователя без заполнения обязательных полей')
    @allure.title('Проверка на невозможность регистрации пользователя без заполнения обязательных полей')
    def test_register_user_without_fields(self):
        response = requests.post(self.register_url,
                                 data={"email": self.user_email, "password": self.user_password})
        data = response.json()
        assert response.status_code == 403
        assert data["success"] == False
        assert data["message"] == "Email, password and name are required fields"
