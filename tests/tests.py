import pytest
from fastapi.testclient import TestClient
from main import app
from models.products import Product
from models.orders import Order
from models.order_items import OrderItem


# Инициализация клиента
client = TestClient(app)

products_db = []
orders_db = []


@pytest.fixture
def get_products_db():
    return products_db


@pytest.fixture
def get_orders_db():
    return orders_db


@pytest.fixture
def sample_product(get_products_db):
    product = Product(
        name="Test Product",
        description="A product for testing",
        price=10.0,
        quantity_in_stock=100,
    )
    get_products_db.append(product)
    return product


# @pytest.fixture
# def sample_order(sample_product):
#     order = Order(
#         id=1,
#         status="in_process",
#         order_items=[OrderItem(product_id=sample_product.id, quantity=1)]
#     )
#     orders_db.append(order)
#     return order


def test_create_product(sample_product):
    new_product = {
        "id": sample_product.id,
        "name": sample_product.name,
        "description": sample_product.description,
        "price": sample_product.price,
        "quantity_in_stock": sample_product.quantity_in_stock,
    }
    response = client.post("/products/", json=new_product)
    assert response.status_code == 200
    assert response.json()["name"] == sample_product.name
    assert response.json()["quantity_in_stock"] == sample_product.quantity_in_stock


def test_get_products(sample_product, get_products_db):
    response = client.get("/products/")
    assert response.status_code == 200
    assert len(response.json()["products"]) > 0
    assert response.json()["products"][-1]["name"] == sample_product.name
    get_products_db.append(response.json()["products"][-1])


# def test_update_product(get_products_db):
#     update_data = {
#         "price": 15.0
#     }
#     response = client.put(f"/products/{get_products_db[0]}", json=update_data)
#     assert response.status_code == 200
#     assert response.json()["price"] == update_data["price"]
#
# def test_delete_product(sample_product):
#     response = client.delete(f"/products/{sample_product.id}")
#     assert response.status_code == 204
#
# def test_create_order(sample_product):
#     order_data = {
#         "status": "in_process",
#         "order_items": [
#             {"product_id": sample_product.id, "quantity": 1}
#         ]
#     }
#     response = client.post("/orders/", json=order_data)
#     assert response.status_code == 200
#     assert response.json()["status"] == order_data["status"]
#
# def test_get_orders(sample_order):
#     response = client.get("/orders/")
#     assert response.status_code == 200
#     assert len(response.json()["orders"]) > 0
#     assert response.json()["orders"][0]["status"] == sample_order.status
#
# def test_update_order(sample_order):
#     update_data = {
#         "status": "completed",
#         "order_items": [
#             {"product_id": sample_order.order_items[0].product_id, "quantity": 1}
#         ]
#     }
#     response = client.put(f"/orders/{sample_order.id}", json=update_data)
#     assert response.status_code == 200
#     assert response.json()["status"] == update_data["status"]
#
# def test_delete_order(sample_order):
#     response = client.delete(f"/orders/{sample_order.id}")
#     assert response.status_code == 204
#
# def test_create_order_not_enough_stock(sample_product):
#     order_data = {
#         "status": "in_process",
#         "order_items": [
#             {"product_id": sample_product.id, "quantity": 200}  # Превышаем количество на складе
#         ]
#     }
#     response = client.post("/orders/", json=order_data)
#     assert response.status_code == 400
#     assert response.json()["detail"] == f"Not enough stock for product {sample_product.name}"
#
# def test_client_initialization():
#     response = client.get("/products/")
#     assert response.status_code in (200, 404)
