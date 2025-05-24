import json
from sqlalchemy import create_engine
from body_dto import addManyShirt, newTable
from models import Base
import populate
from fastapi.testclient import TestClient
from main import add_many, app, create_table
from unittest.mock import patch, MagicMock

# iniciar DB
engine = create_engine("sqlite:///database.db", echo=True)

Base.metadata.create_all(bind=engine)

def test_add_many_success(mock_services):
    payload = {
        "type": "basic",
        "p": 2,
        "m": 3,
        "g": 1
    }
    response = client.post("/table/1/addMany", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["table_id"] == 1

async def test_add_many_error():
    populate.populate_data()
    
    addTable = newTable(width=800, height=600)
    
    idRetjurn = await create_table(addTable)
    idReturn = json.loads(idRetjurn)["id"]
    
    response = await add_many(idReturn, addManyShirt(type="T-SHIRT", p=3, m=1, g=1) )
    
    assert response.status_code == 200
    data = response.json()
    assert "error" in data
    
import asyncio
if __name__ == "__main__":
    asyncio.run(test_add_many_error())