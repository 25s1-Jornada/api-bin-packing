import json
import unittest
from unittest import IsolatedAsyncioTestCase

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from types import SimpleNamespace

from body_dto import addManyShirt, newTable
from models import GartmentTable, Shirt
from main import create_table, add_many, remove_shirt
from services import GartmentTableService
from unittest.mock import patch



# Criação da engine global para reuso nos testes
engine = create_engine("sqlite:///database.db", echo=True)

def fake_output_json(client_id):
    import os, json
    dirname = os.path.join("data", str(client_id))
    os.makedirs(dirname, exist_ok=True)

    with open(os.path.join(dirname, "output.json"), "w") as f:
        json.dump({
            "bins": [{
                "items": [{
                    "id": f"shirt.{client_id}",
                    "item_shapes": [{
                        "shape": [{"xs": 0, "ys": 0, "xe": 10, "ye": 10}]
                    }]
                }]
            }]
        }, f)

class GarmentTableTest(IsolatedAsyncioTestCase):
    
    async def test_create(self):
        testTable = SimpleNamespace(width=800, height=600)
        id = json.loads(await create_table(testTable))
        id = id.get("id")

        with Session(engine) as session:
            table = session.get(GartmentTable, id)
            self.assertEqual(id, table.id)

    @patch("main.execute_action")
    async def test_addShirt(self, mock_execute):
        mock_execute.return_value = {
            "maxRects": ["shirt.1"],
            "skyline": ["shirt.1"],
            "guillotine": ["shirt.1"]
        }

        # Garante que existem camisetas
        with Session(engine) as session:
            for size in ["P", "M", "G"]:
                if not session.query(Shirt).filter_by(type="P", size=size).first():
                    session.add(Shirt(type="P", size=size))
            session.commit()

        addStmt = addManyShirt(p=1, m=1, g=1, type="P")
        tableId = 1

        with Session(engine) as session:
            table = session.get(GartmentTable, tableId)

        table_updated = json.loads(await add_many(tableId, addStmt))

        assert table_updated["maxRects"]

"""     @patch("main.execute_action")
    async def test_removeShirt(self, mock_execute):
        mock_execute.return_value = {
            "maxRects": ["shirt.1"],
            "skyline": ["shirt.1"],
            "guillotine": ["shirt.1"]
        }

        # Garante que existem camisetas
        with Session(engine) as session:
            for size in ["P", "M", "G"]:
                if not session.query(Shirt).filter_by(type="P", size=size).first():
                    session.add(Shirt(type="P", size=size))
            session.commit()

        tableId = 1
        addStmt = addManyShirt(p=1, m=1, g=1, type="P")

        # Simula a adição de camisetas
        table_updated = json.loads(await add_many(tableId, addStmt))

        # Extrai um ID de camisa para remover (simulado)
        shirt_id = table_updated["maxRects"][0].split('.')[-1]

        # Remove a camisa
        table_updated = await remove_shirt(tableId, shirt_id)

        # Verifica que o ID removido não está mais presente (simulação também)
        assert shirt_id not in table_updated["maxRects"]
        assert shirt_id not in table_updated["skyline"]
        assert shirt_id not in table_updated["guillotine"] """


if __name__ == '__main__':
    unittest.main()
