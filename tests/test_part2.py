import pytest


# Тесты для GET /products
def test_get_products(client):
    response = client.get('/products')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


# Тесты для POST /products
def test_create_product(client):
    new_product = {"name": "Product 3", "price": 300}
    response = client.post('/products', json=new_product)
    assert response.status_code == 201
    created_product = response.get_json()
    assert created_product['name'] == new_product['name']
    assert created_product['price'] == new_product['price']


# Тесты для GET /products/<product_id>
def test_get_product(client):
    product_id = 1
    response = client.get(f'/products/{product_id}')
    assert response.status_code == 200
    product = response.get_json()
    assert product['id'] == product_id


def test_get_product_not_found(client):
    product_id = 999
    response = client.get(f'/products/{product_id}')
    assert response.status_code == 404


# Тесты для PUT /products/<product_id>
def test_update_product(client):
    product_id = 1
    update_data = {"name": "Updated Product", "price": 150}
    response = client.put(f'/products/{product_id}', json=update_data)
    assert response.status_code == 200
    updated_product = response.get_json()
    assert updated_product['name'] == update_data['name']
    assert updated_product['price'] == update_data['price']


def test_update_product_not_found(client):
    product_id = 999
    update_data = {"name": "Updated Product", "price": 150}
    response = client.put(f'/products/{product_id}', json=update_data)
    assert response.status_code == 404


# Тесты для DELETE /products/<product_id>
def test_delete_product(client):
    product_id = 2
    response = client.delete(f'/products/{product_id}')
    assert response.status_code == 204


def test_delete_product_not_found(client):
    product_id = 999
    response = client.delete(f'/products/{product_id}')
    assert response.status_code == 404


if __name__ == '__main__':
    pytest.main()
