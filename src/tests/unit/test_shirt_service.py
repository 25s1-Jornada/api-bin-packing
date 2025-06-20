import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Shirt, PackerModel
from services import ShirtService, PackerService
from packing_layer import Packer

# Configura o banco de dados SQLite em memória para uso nos testes
engine = create_engine("sqlite:///:memory:", echo=False)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

# Cria uma fixture do SQLAlchemy para fornecer sessões de banco em cada teste
@pytest.fixture
def db_session():
    session = SessionLocal()
    yield session
    session.close()

# Fixture que fornece uma instância do serviço de camisetas
@pytest.fixture
def shirt_service():
    return ShirtService(engine)

# Fixture que fornece uma instância do serviço de empacotamento
@pytest.fixture
def packer_service():
    return PackerService(engine)

# Testa se o método get_by_size_type retorna corretamente uma camiseta do banco
def test_get_by_size_type(shirt_service, db_session):
    # Insere uma camiseta no banco manualmente
    new_shirt = Shirt(size="M", type="T-SHIRT")
    db_session.add(new_shirt)
    db_session.commit()

    # Chama o método que deve recuperar a camiseta
    result = shirt_service.get_by_size_type("M", "T-SHIRT")

    # Verifica se os atributos da camiseta estão corretos
    assert result is not None
    assert result.size == "M"
    assert result.type == "T-SHIRT"

# Testa se o método get_one recupera uma camiseta pelo ID corretamente
def test_get_one(shirt_service, db_session):
    # Insere uma camiseta no banco
    shirt = Shirt(size="G", type="TANK")
    db_session.add(shirt)
    db_session.commit()

    # Busca a camiseta pelo ID
    result = shirt_service.get_one(shirt.id)

    # Verifica se os atributos estão corretos
    assert result is not None
    assert result.size == "G"
    assert result.type == "TANK"

# Testa a serialização e desserialização de um objeto Packer via PackerService
def test_set_and_get_packer_instance():
    # Cria um mock do objeto Packer com valores de texto (simples para facilitar teste)
    original_packer = Packer(packer_max="max", packer_sky="sky", packer_gui="gui")

    # Cria um modelo de banco representando o estado do empacotador
    model = PackerModel(original_packer)

    # Serializa o objeto Packer e salva no modelo
    updated_model = PackerService.set_packer_instance(original_packer, model)

    # Desserializa o modelo para recriar o objeto original
    recovered = PackerService.get_packer_instance(updated_model)

    # Verifica se a desserialização reconstrói corretamente os campos
    # Note que a ordem foi invertida propositalmente pela lógica do método
    assert recovered._packer_max == "sky"
    assert recovered._packer_sky == "gui"
    assert recovered._packer_gui == "max"