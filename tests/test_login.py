import requests
import allure
import test_data


class TestLogin:

    @allure.description('Проверяем, что пользователь с существующим логином может авторизоваться')
    @allure.title('Проверка на корректность входа с существующим логином')
    def test_login_user(self):
        response = requests.post(test_data.login_url,
                                 data={"email": test_data.user_email, "password": test_data.user_password})
        data = response.json()

        assert response.status_code == 200
        assert data["success"] == True
        assert "accessToken" in data
        assert "refreshToken" in data
        assert "user" in data

    @allure.description('Проверяем, что пользователь с некорректными данными не может авторизоваться')
    @allure.title('Проверка на ошибку при использовании неверных данных')
    def test_login_incorrect_data_user(self):
        response = requests.post(test_data.login_url,
                                 data={"email": test_data.user_email + "dvjnd", "password": test_data.user_password + "22656"})
        data = response.json()

        assert response.status_code == 401
        assert data["success"] == False
        assert data["message"] == test_data.message_incorrect_data_user
