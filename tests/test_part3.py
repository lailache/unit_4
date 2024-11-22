import pytest


def test_get_products_with_api_client(api_client):
    response = api_client.get('/products')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert 'id' in data[0]
        assert 'name' in data[0]
        assert 'price' in data[0]


def test_create_product_with_api_client(api_client):
    new_product = {"name": "Product 4", "price": 400}
    response = api_client.post('/products', json=new_product)
    assert response.status_code == 201
    created_product = response.json()
    assert created_product['name'] == new_product['name']
    assert created_product['price'] == new_product['price']
    assert 'id' in created_product


def test_get_product_with_api_client(api_client):
    product_id = 1
    response = api_client.get(f'/products/{product_id}')
    assert response.status_code == 200
    product = response.json()
    assert product['id'] == product_id
    assert 'name' in product
    assert 'price' in product


def test_update_product_with_api_client(api_client):
    product_id = 1
    update_data = {"name": "Updated Product 1", "price": 150}
    response = api_client.put(f'/products/{product_id}', json=update_data)
    assert response.status_code == 200
    updated_product = response.json()
    assert updated_product['name'] == update_data['name']
    assert updated_product['price'] == update_data['price']


def test_delete_product_with_api_client(api_client):
    product_id = 2
    response = api_client.delete(f'/products/{product_id}')
    assert response.status_code == 204


def test_product_not_found_with_api_client(api_client):
    product_id = 999
    response = api_client.get(f'/products/{product_id}')
    assert response.status_code == 404
    error_message = response.json()
    assert 'error' in error_message


if __name__ == '__main__':
    pytest.main()
