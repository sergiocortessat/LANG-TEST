from src.tools import lookup_supplier


def test_lookup_known_supplier() -> None:
    result = lookup_supplier.invoke({"name": "Flower Export Ltd."})
    assert "Net 30" in result
    assert "trusted" in result


def test_lookup_unknown_supplier() -> None:
    result = lookup_supplier.invoke({"name": "Missing GmbH"})
    assert "No registry entry" in result
