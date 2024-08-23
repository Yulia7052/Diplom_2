import requests
import allure


class TestOrderList:
    login_url = "https://stellarburgers.nomoreparties.site/api/auth/login"
    login_email = "bulochka@yandex.ru"
    login_password = "5469"
    orders_url = "https://stellarburgers.nomoreparties.site/api/orders"

    @allure.description('Можно получить список заказов, если пользователь авторизовался')
    @allure.title('Проверка на получение списка заказов авторизованного пользователя')
    def test_get_order_list_auth(self):
        response = requests.post(self.login_url, data={"email": self.login_email, "password": self.login_password})
        data = response.json()
        token = data["accessToken"]
        response = requests.get(self.orders_url, headers={"authorization": token})
        data = response.json()

        assert response.status_code == 200
        assert data["success"] == True
        assert "orders" in data
        assert "total" in data
        assert "totalToday" in data

    @allure.description('Нельзя получить список заказов, если пользователь не авторизовался')
    @allure.title('Проверка на невозможность получения списка заказов пользователя без авторизации')
    def test_get_order_list_no_auth(self):
        response = requests.get(self.orders_url)
        data = response.json()

        assert response.status_code == 401
        assert data["success"] == False
        assert data["message"] == "You should be authorised"
