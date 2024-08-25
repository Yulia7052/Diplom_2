import requests
import allure
import test_data


class TestOrderList:

    @allure.description('Можно получить список заказов, если пользователь авторизовался')
    @allure.title('Проверка на получение списка заказов авторизованного пользователя')
    def test_get_order_list_auth(self):
        response = requests.post(test_data.login_url, data={"email": test_data.user_email, "password": test_data.user_password})
        data = response.json()
        token = data["accessToken"]
        response = requests.get(test_data.orders_url, headers={"authorization": token})
        data = response.json()

        assert response.status_code == 200
        assert data["success"] == True
        assert "orders" in data
        assert "total" in data
        assert "totalToday" in data

    @allure.description('Нельзя получить список заказов, если пользователь не авторизовался')
    @allure.title('Проверка на невозможность получения списка заказов пользователя без авторизации')
    def test_get_order_list_no_auth(self):
        response = requests.get(test_data.orders_url)
        data = response.json()

        assert response.status_code == 401
        assert data["success"] == False
        assert data["message"] == test_data.message_incorrect_user
