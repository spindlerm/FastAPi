"""Example pytest tests"""
from app.main import app
from fastapi.testclient import TestClient
from pydantic_mongo import ObjectIdField

client = TestClient(app)

def test_create():
    """Example test use case"""

    item_to_create = {
    "name": "joes Bloggs",
    "description": "This is joes item",
    "price": 10,
    "tax": 1.6
    }

    retrived_item = item_to_create

    response = client.post("/test", json=item_to_create)
    assert response.status_code == 201

   
    #Fetch th eitem with the return id to check it was created"
    id = ObjectIdField(response.json()["_id"])

    response = client.get(f"/test/{id}")
    assert response.status_code == 200

    #Add the returned id to the retrived_Item
    retrived_item["_id"] = id
    assert response.json() == retrived_item
   
