import json
from types import SimpleNamespace
from Utils import Utils

# Testa a função 'mount_table_return' da classe Utils
def test_mount_table_return():
    # Simula uma mesa (table) com valores simples usando SimpleNamespace
    table = SimpleNamespace(
        width=1000,
        height=800,
        bin_maxrects=[{"x": 0, "y": 0}],  # Apenas um retângulo simples
        bin_skyline=None,                 # Não usado nesse teste
        bin_guillotine=None               # Não usado nesse teste
    )

    # Executa a função para montar o retorno JSON da mesa
    result_json = Utils.mount_table_return(table)

    # Converte a string JSON de volta para dicionário Python
    result = json.loads(result_json)

    # Verifica se os dados foram corretamente montados
    assert result["width"] == 1000            
    assert result["height"] == 800            
    assert isinstance(result["maxRects"], list)  
