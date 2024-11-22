import pytest
from pytest_httpserver import HTTPServer


def test_get_products(httpserver: HTTPServer, api_client_with_httpserver):
    httpserver.expect_request("/products", method="GET").respond_with_json([
        {"id": 1, "name": "Product 1", "price": 100},
        {"id": 2, "name": "Product 2", "price": 200}
    ])
    response = api_client_with_httpserver.get('/products')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert 'id' in data[0]
        assert 'name' in data[0]
        assert 'price' in data[0]


def test_create_product(httpserver: HTTPServer, api_client_with_httpserver):
    new_product = {"name": "Product 3", "price": 300}
    httpserver.expect_request("/products", method="POST", json=new_product).respond_with_json(
        {"id": 3, "name": "Product 3", "price": 300}, status=201
    )
    response = api_client_with_httpserver.post('/products', json=new_product)
    assert response.status_code == 201
    created_product = response.json()
    assert created_product['name'] == new_product['name']
    assert created_product['price'] == new_product['price']
    assert 'id' in created_product


def test_get_product(httpserver: HTTPServer, api_client_with_httpserver):
    product_id = 1
    httpserver.expect_request(f'/products/{product_id}', method="GET").respond_with_json(
        {"id": 1, "name": "Product 1", "price": 100}
    )
    response = api_client_with_httpserver.get(f'/products/{product_id}')
    assert response.status_code == 200
    product = response.json()
    assert product['id'] == product_id
    assert 'name' in product
    assert 'price' in product


def test_update_product(httpserver: HTTPServer, api_client_with_httpserver):
    product_id = 1
    update_data = {"name": "Updated Product 1", "price": 150}
    httpserver.expect_request(f'/products/{product_id}', method="PUT", json=update_data).respond_with_json(
        {"id": 1, "name": "Updated Product 1", "price": 150}
    )
    response = api_client_with_httpserver.put(f'/products/{product_id}', json=update_data)
    assert response.status_code == 200
    updated_product = response.json()
    assert updated_product['name'] == update_data['name']
    assert updated_product['price'] == update_data['price']


def test_delete_product(httpserver: HTTPServer, api_client_with_httpserver):
    product_id = 2
    httpserver.expect_request(f'/products/{product_id}', method="DELETE").respond_with_data(status=204)
    response = api_client_with_httpserver.delete(f'/products/{product_id}')
    assert response.status_code == 204


def test_product_not_found(httpserver: HTTPServer, api_client_with_httpserver):
    product_id = 999
    httpserver.expect_request(f'/products/{product_id}', method="GET").respond_with_json(
        {"error": "Product not found"}, status=404
    )
    response = api_client_with_httpserver.get(f'/products/{product_id}')
    assert response.status_code == 404
    error_message = response.json()
    assert 'error' in error_message


if __name__ == '__main__':
    pytest.main()
