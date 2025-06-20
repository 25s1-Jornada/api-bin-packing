from packingsolver_layer import generate_json
from types import SimpleNamespace

# Testa a função generate_json, que transforma uma lista de vértices em uma estrutura JSON usada pelo algoritmo de empacotamento
def test_generate_json():
    # Cria uma lista simulada de vértices, com dois tipos de peças: 'corpo' e 'manga'
    # Cada item usa SimpleNamespace para simular objetos com atributos `.vertices` e `.type`
    mock_vertices_list = [
        (2, [SimpleNamespace(vertices=[[0, 0], [1, 0], [1, 1], [0, 1]], type='corpo')]),  # 2 cópias
        (1, [SimpleNamespace(vertices=[[0, 0], [2, 0], [2, 1], [0, 1]], type='manga')])   # 1 cópia
    ]

    # Chama a função que deve gerar o dicionário JSON a partir da lista de vértices
    json_data = generate_json(mock_vertices_list, width=100, height=100)

    # Verifica se a estrutura de saída contém a chave 'bin_types', indicando a presença da definição do espaço de empacotamento
    assert 'bin_types' in json_data

    # Verifica se foram criados dois tipos de itens (corpo e manga)
    assert len(json_data['item_types']) == 2

    # Verifica se o primeiro item tem a quantidade de cópias correta (2)
    assert json_data['item_types'][0]['copies'] == 2
