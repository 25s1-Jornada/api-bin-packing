import os
import json
import time
import unittest
from types import SimpleNamespace
from main import create_table, add_many
from json_reader import get_total_item_area, get_table_area, get_item_count
from body_dto import addManyShirt

class GarmentTableTest(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        from populate import populate_data
        populate_data()

    async def test_full_flow(self):
        # Cria a mesa
        testTable = SimpleNamespace(width=800, height=660)
        table_data = json.loads(await create_table(testTable))
        table_id = table_data.get("id")

        # Marca o tempo de início
        start = time.time()

        # Cria DTO simulado
        addShirtDTO = addManyShirt(type="T-SHIRT", p=10, m=10, g=9)

        # Chama a função com o objeto correto
        result = json.loads(await add_many(table_id, addShirtDTO))

        # Marca o tempo final
        duration = time.time() - start

        # Verificações básicas
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0, "O resultado da solução não retornou peças.")

        # Caminhos para input/output
        data_dir = f"/data/{table_id}"
        input_path = os.path.join(data_dir, "input.json")
        output_path = os.path.join(data_dir, "output.json")

        # Verifica existência dos arquivos
        self.assertTrue(os.path.exists(input_path), f"input.json não foi criado em {input_path}")
        self.assertTrue(os.path.exists(output_path), f"output.json não foi criado em {output_path}")

        # Validação da quantidade de peças
        total_input_items = get_item_count(input_path)
        total_output_items = len(result)
        self.assertEqual(total_input_items, total_output_items, f"Qtd input ({total_input_items}) != output ({total_output_items})")

        # Validação de aproveitamento da mesa (mínimo 95%)
        total_item_area = get_total_item_area(input_path)
        table_area = get_table_area(input_path)
        aproveitamento = total_item_area / table_area
        self.assertGreaterEqual(aproveitamento, 0.95, f"Aproveitamento insuficiente: {aproveitamento:.2%}")


if __name__ == "__main__":
    unittest.main()
