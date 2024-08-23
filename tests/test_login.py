import requests
import allure


class TestLogin:
    login_url = "https://stellarburgers.nomoreparties.site/api/auth/login"
    email = "bulochka@yandex.ru"
    password = "5469"
    message_incorrect_data_user = "email or password are incorrect"

    @allure.description('Проверяем, что пользователь с существующим логином может авторизоваться')
    @allure.title('Проверка на корректность входа с существующим логином')
    def test_login_user(self):
        response = requests.post(self.login_url,
                                 data={"email": self.email, "password": self.password})
        data = response.json()

        assert response.status_code == 200
        assert data["success"] == True
        assert "accessToken" in data
        assert "refreshToken" in data
        assert "user" in data

    @allure.description('Проверяем, что пользователь с некорректными данными не может авторизоваться')
    @allure.title('Проверка на ошибку при использовании неверных данных')
    def test_login_incorrect_data_user(self):
        response = requests.post(self.login_url,
                                 data={"email": self.email + "dvjnd", "password": self.password + "22656"})
        data = response.json()

        assert response.status_code == 401
        assert data["success"] == False
        assert data["message"] == self.message_incorrect_data_user
