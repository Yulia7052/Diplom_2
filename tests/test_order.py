import requests
import allure
import test_data


class TestOrder:

    @allure.description('Можно сделать заказ с авторизацией на сайте и с указанием ингредиентов')
    @allure.title('Проверка на создание заказа с авторизацией и выбором ингредиентов ')
    def test_order_with_ingredients_auth(self):
        response = requests.post(test_data.login_url,
                                 data={"email": test_data.user_email, "password": test_data.user_password})
        data = response.json()
        token = data["accessToken"]
        response = requests.get(test_data.ingredients_url)
        data = response.json()
        ingredient = data["data"][0]
        id = ingredient["_id"]
        response = requests.post(test_data.orders_url, data={"ingredients": [id]}, headers={"authorization": token})
        data = response.json()

        assert response.status_code == 200
        assert data["success"] == True

    @allure.description('Можно сделать заказ без авторизации на сайте, но с указанием ингредиентов')
    @allure.title('Проверка на создание заказа без авторизации и выбором ингредиентов ')
    def test_order_with_ingredients_no_auth(self):
        response = requests.get(test_data.ingredients_url)
        data = response.json()
        ingredient = data["data"][0]
        id = ingredient["_id"]
        response = requests.post(test_data.orders_url, data={"ingredients": [id]})
        data = response.json()

        assert response.status_code == 200
        assert data["success"] == True

    @allure.description('Нельзя сделать заказ с авторизацией на сайте, но без выбора ингредиентов')
    @allure.title('Проверка на невозможность создания заказа с авторизацией без выбора ингредиентов')
    def test_order_without_ingredients_auth(self):
        response = requests.post(test_data.login_url,
                                 data={"email": test_data.user_email, "password": test_data.user_password})
        data = response.json()
        token = data["accessToken"]
        response = requests.post(test_data.orders_url, data={"ingredients": []}, headers={"authorization": token})
        data = response.json()

        assert response.status_code == 400
        assert data["success"] == False
        assert data["message"] == test_data.message_incorrect_order

    @allure.description('Нельзя сделать заказ без авторизации на сайте и без выбора ингредиентов'
                        '(обязателен выбор ингредиентов)')
    @allure.title('Проверка на невозможность создания заказа без авторизации и без выбора ингредиентов')
    def test_order_without_ingredients_no_auth(self):
        response = requests.post(test_data.orders_url, data={"ingredients": []})
        data = response.json()

        assert response.status_code == 400
        assert data["success"] == False
        assert data["message"] == test_data.message_incorrect_order

    @allure.description('Нельзя сделать заказ с авторизацией на сайте и с некорректным хэшем ингредиентов')
    @allure.title('Проверка на невозможность создания заказа с авторизацией и с указанием неверного хэша ингредиентов')
    def test_order_incorrect_hash_auth(self):
        response = requests.post(test_data.login_url,
                                 data={"email": test_data.user_email, "password": test_data.user_password})
        data = response.json()
        token = data["accessToken"]
        response = requests.post(test_data.orders_url,
                                 data={"ingredients": ["ia ne verniy hash"]}, headers={"authorization": token})

        assert response.status_code == 500

    @allure.description('Нельзя сделать заказ без авторизации на сайте и с некорректным хэшем ингредиентов '
                        '(хэш ингредиентов должен быть корректным)')
    @allure.title('Проверка на невозможность создания заказа без авторизации и с указанием неверного хэша ингредиентов')
    def test_order_incorrect_hash_no_auth(self):
        response = requests.post(test_data.orders_url,
                                 data={"ingredients": ["qwerty"]})

        assert response.status_code == 500
