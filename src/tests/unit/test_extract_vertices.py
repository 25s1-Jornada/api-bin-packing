from packingsolver_layer import extract_vertices

# Testa a função extract_vertices, responsável por extrair os vértices de cada item a partir de uma estrutura de saída complexa
def test_extract_vertices():
    # Simula uma estrutura de dados que representa a saída do algoritmo de empacotamento (packing)
    sample_output = {
        "bins": [
            {
                "items": [
                    {
                        "id": "item1",
                        "item_shapes": [
                            {
                                "shape": [
                                    {"xs": 0, "ys": 0, "xe": 1, "ye": 0},
                                    {"xs": 1, "ys": 0, "xe": 1, "ye": 1},
                                    {"xs": 1, "ys": 1, "xe": 0, "ye": 1},
                                    {"xs": 0, "ys": 1, "xe": 0, "ye": 0}
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }

    # Executa a função que deve extrair os vértices dos itens
    result = extract_vertices(sample_output)

    # Verifica se o retorno é uma lista (estrutura esperada)
    assert isinstance(result, list)

    # Verifica se o primeiro item retornado tem o ID esperado
    assert result[0]['id'] == 'item1'

    # Verifica se os vértices foram extraídos corretamente da forma, ignorando os pontos duplicados
    # Neste caso, o último ponto (0, 0) foi removido por estar repetido
    assert result[0]['vertices'] == [(0, 0), (1, 0), (1, 1), (0, 1)]
