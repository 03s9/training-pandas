def validar_desconto(valor: int) -> int:
    return valor - 10

def test_validar_desconto() -> None:
    assert validar_desconto(100) == 90
