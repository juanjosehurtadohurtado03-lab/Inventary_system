def test_add_product(client):
    response = client.post('/api/routers/product', json={
        "name": "cafe",
        "price": 4,
        "stock": 8
    })
    print(response.status_code, response.json())
    assert response.status_code == 201

def test_create_sale(client):
    response = client.post('/api/routers/sale', json={
        "customer_ci": "12345678",
        "items": [
            {"name": "cafe", "quantity": 2}
        ]
    })
    assert response.status_code in [200, 201]