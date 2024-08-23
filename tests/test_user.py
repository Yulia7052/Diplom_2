import requests
import allure


class TestUser:
    login_url = "https://stellarburgers.nomoreparties.site/api/auth/login"
    user_url = "https://stellarburgers.nomoreparties.site/api/auth/user"
    login_email = "bulochka@yandex.ru"
    login_password = "5469"
    new_name = "NewName"

    @allure.description('Проверка, что можно изменить данные авторизованного пользователя')
    @allure.title('Успешное изменение данных пользователя')
    def test_change_data_user_auth(self):
        response = requests.post(self.login_url, data={"email": self.login_email, "password": self.login_password})
        data = response.json()
        response = requests.patch(self.user_url, data={"name": self.new_name}, headers={"authorization": data["accessToken"]})
        data = response.json()

        assert data["success"] == True
        assert "user" in data
        assert data["user"]["name"] == self.new_name

    @allure.description('Изменение данных пользователя невозможно без входа в аккаунт')
    @allure.title('Проверка, что нельзя изменить данные пользователя без авторизации')
    def test_change_data_user_no_auth(self):
        response = requests.patch(self.user_url, data={"name": self.new_name})
        data = response.json()

        assert data["success"] == False
        assert data["message"] == "You should be authorised"
