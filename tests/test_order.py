import requests
import allure


class TestOrder:
    login_url = "https://stellarburgers.nomoreparties.site/api/auth/login"
    login_email = "bulochka@yandex.ru"
    login_password = "5469"
    ingredients_url = "https://stellarburgers.nomoreparties.site/api/ingredients"
    orders_url = "https://stellarburgers.nomoreparties.site/api/orders"

    @allure.description('Можно сделать заказ с авторизацией на сайте и с указанием ингредиентов')
    @allure.title('Проверка на создание заказа с авторизацией и выбором ингредиентов ')
    def test_order_with_ingredients_auth(self):
        response = requests.post(self. login_url,
                                 data={"email": self.login_email, "password": self.login_password})
        data = response.json()
        token = data["accessToken"]
        response = requests.get(self.ingredients_url)
        data = response.json()
        ingredient = data["data"][0]
        id = ingredient["_id"]
        response = requests.post(self.orders_url, data={"ingredients": [id]}, headers={"authorization": token})
        data = response.json()

        assert response.status_code == 200
        assert data["success"] == True

    @allure.description('Можно сделать заказ без авторизации на сайте, но с указанием ингредиентов')
    @allure.title('Проверка на создание заказа без авторизации и выбором ингредиентов ')
    def test_order_with_ingredients_no_auth(self):
        response = requests.get(self.ingredients_url)
        data = response.json()
        ingredient = data["data"][0]
        id = ingredient["_id"]
        response = requests.post(self.orders_url, data={"ingredients": [id]})
        data = response.json()

        assert response.status_code == 200
        assert data["success"] == True

    @allure.description('Нельзя сделать заказ с авторизацией на сайте, но без выбора ингредиентов')
    @allure.title('Проверка на невозможность создания заказа с авторизацией без выбора ингредиентов')
    def test_order_without_ingredients_auth(self):
        response = requests.post(self.login_url,
                                 data={"email": self.login_email, "password": self.login_password})
        data = response.json()
        token = data["accessToken"]
        response = requests.post(self.orders_url, data={"ingredients": []}, headers={"authorization": token})
        data = response.json()

        assert response.status_code == 400
        assert data["success"] == False
        assert data["message"] == "Ingredient ids must be provided"

    @allure.description('Нельзя сделать заказ без авторизации на сайте и без выбора ингредиентов'
                        '(обязателен выбор ингредиентов)')
    @allure.title('Проверка на невозможность создания заказа без авторизации и без выбора ингредиентов')
    def test_order_without_ingredients_no_auth(self):
        response = requests.post(self.orders_url, data={"ingredients": []})
        data = response.json()

        assert response.status_code == 400
        assert data["success"] == False
        assert data["message"] == "Ingredient ids must be provided"

    @allure.description('Нельзя сделать заказ с авторизацией на сайте и с некорректным хэшем ингредиентов')
    @allure.title('Проверка на невозможность создания заказа с авторизацией и с указанием неверного хэша ингредиентов')
    def test_order_incorrect_hash_auth(self):
        response = requests.post(self.login_url,
                                 data={"email": self.login_email, "password": self.login_password})
        data = response.json()
        token = data["accessToken"]
        response = requests.post(self.orders_url,
                                 data={"ingredients": ["ia ne verniy hash"]}, headers={"authorization": token})

        assert response.status_code == 500

    @allure.description('Нельзя сделать заказ без авторизации на сайте и с некорректным хэшем ингредиентов '
                        '(хэш ингредиентов должен быть корректным)')
    @allure.title('Проверка на невозможность создания заказа без авторизации и с указанием неверного хэша ингредиентов')
    def test_order_incorrect_hash_no_auth(self):
        response = requests.post(self.orders_url,
                                 data={"ingredients": ["qwerty"]})

        assert response.status_code == 500
