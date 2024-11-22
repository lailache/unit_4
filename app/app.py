from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "user1": "password1",
    "user2": "password2"
}


@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username


products = [
    {"id": 1, "name": "Product 1", "price": 100},
    {"id": 2, "name": "Product 2", "price": 200}
]


# Получение списка всех продуктов
@app.route('/products', methods=['GET'])
@auth.login_required
def get_products():
    return jsonify(products)


# Создание нового продукта
@app.route('/products', methods=['POST'])
@auth.login_required
def create_product():
    new_product = request.get_json()
    new_product['id'] = len(products) + 1
    products.append(new_product)
    return jsonify(new_product), 201


# Получение продукта по ID
@app.route('/products/<int:product_id>', methods=['GET'])
@auth.login_required
def get_product(product_id):
    product = next((product for product in products if product['id'] == product_id), None)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)


# Обновление продукта по ID
@app.route('/products/<int:product_id>', methods=['PUT'])
@auth.login_required
def update_product(product_id):
    product = next((product for product in products if product['id'] == product_id), None)
    if product is None:
        return jsonify({"error": "Product not found"}), 404

    update_data = request.get_json()
    product.update(update_data)
    return jsonify(product)


# Удаление продукта по ID
@app.route('/products/<int:product_id>', methods=['DELETE'])
@auth.login_required
def delete_product(product_id):
    product = next((product for product in products if product['id'] == product_id), None)
    if product is None:
        return jsonify({"error": "Product not found"}), 404

    products.remove(product)
    return '', 204


if __name__ == '__main__':
    app.run(debug=True)
