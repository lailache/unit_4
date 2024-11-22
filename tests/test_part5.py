import pytest
import requests
import responses


@responses.activate
def test_get_products_mocked():
    responses.add(
        responses.GET, 'http://127.0.0.1:5000/products',
        json=[{"id": 1, "name": "Product 1", "price": 100}],
        status=200
    )
    response = requests.get('http://127.0.0.1:5000/products')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert 'id' in data[0]
        assert 'name' in data[0]
        assert 'price' in data[0]


@responses.activate
def test_create_product_mocked():
    responses.add(
        responses.POST, 'http://127.0.0.1:5000/products',
        json={"id": 3, "name": "Product 3", "price": 300},
        status=201
    )
    new_product = {"name": "Product 3", "price": 300}
    response = requests.post('http://127.0.0.1:5000/products', json=new_product)
    assert response.status_code == 201
    created_product = response.json()
    assert created_product['name'] == new_product['name']
    assert created_product['price'] == new_product['price']
    assert 'id' in created_product


@responses.activate
def test_get_product_mocked():
    product_id = 1
    responses.add(
        responses.GET, f'http://127.0.0.1:5000/products/{product_id}',
        json={"id": 1, "name": "Product 1", "price": 100},
        status=200
    )
    response = requests.get(f'http://127.0.0.1:5000/products/{product_id}')
    assert response.status_code == 200
    product = response.json()
    assert product['id'] == product_id
    assert 'name' in product
    assert 'price' in product


@responses.activate
def test_update_product_mocked():
    product_id = 1
    responses.add(
        responses.PUT, f'http://127.0.0.1:5000/products/{product_id}',
        json={"id": 1, "name": "Updated Product 1", "price": 150},
        status=200
    )
    update_data = {"name": "Updated Product 1", "price": 150}
    response = requests.put(f'http://127.0.0.1:5000/products/{product_id}', json=update_data)
    assert response.status_code == 200
    updated_product = response.json()
    assert updated_product['name'] == update_data['name']
    assert updated_product['price'] == update_data['price']


@responses.activate
def test_delete_product_mocked():
    product_id = 2
    responses.add(
        responses.DELETE, f'http://127.0.0.1:5000/products/{product_id}',
        status=204
    )
    response = requests.delete(f'http://127.0.0.1:5000/products/{product_id}')
    assert response.status_code == 204


@responses.activate
def test_product_not_found_mocked():
    product_id = 999
    responses.add(
        responses.GET, f'http://127.0.0.1:5000/products/{product_id}',
        json={"error": "Product not found"},
        status=404
    )
    response = requests.get(f'http://127.0.0.1:5000/products/{product_id}')
    assert response.status_code == 404
    error_message = response.json()
    assert 'error' in error_message


if __name__ == '__main__':
    pytest.main()
