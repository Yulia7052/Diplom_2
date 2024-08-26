import requests
import allure
import test_data


class TestUser:

    @allure.description('Проверка, что можно изменить данные авторизованного пользователя')
    @allure.title('Успешное изменение данных пользователя')
    def test_change_data_user_auth(self):
        response = requests.post(test_data.login_url, data={"email": test_data.user_email, "password": test_data.user_password})
        data = response.json()
        response = requests.patch(test_data.user_url, data={"name": test_data.new_name}, headers={"authorization": data["accessToken"]})
        data = response.json()

        assert data["success"] == True
        assert "user" in data
        assert data["user"]["name"] == test_data.new_name

    @allure.description('Изменение данных пользователя невозможно без входа в аккаунт')
    @allure.title('Проверка, что нельзя изменить данные пользователя без авторизации')
    def test_change_data_user_no_auth(self):
        response = requests.patch(test_data.user_url, data={"name": test_data.new_name})
        data = response.json()

        assert data["success"] == False
        assert data["message"] == test_data.message_incorrect_user
