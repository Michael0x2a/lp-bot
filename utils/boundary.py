from typing import Any
from utils.custom_types import JsonDict

def check_is_str(obj: Any) -> str:
    assert isinstance(obj, str)
    return obj

def check_is_json_dict(obj: Any) -> JsonDict:
    assert isinstance(obj, dict)
    return obj

