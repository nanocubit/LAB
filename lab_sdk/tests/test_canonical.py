import math
import pytest
from lab_sdk.canonical import canonical_json_bytes, digest_json

def test_key_order_and_unicode_nfc_are_canonical():
    a={"z":"e\u0301","a":1}
    b={"a":1,"z":"é"}
    assert canonical_json_bytes(a)==canonical_json_bytes(b)
    assert digest_json(a)==digest_json(b)

def test_negative_zero_normalizes():
    assert canonical_json_bytes({"x":-0.0})==canonical_json_bytes({"x":0})

@pytest.mark.parametrize("v", [math.nan, math.inf, -math.inf])
def test_non_finite_float_rejected(v):
    with pytest.raises(ValueError): canonical_json_bytes({"x":v})
