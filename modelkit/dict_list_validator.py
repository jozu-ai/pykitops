from typing import Any, Set
from .dict_validator import DictValidator

class DictListValidator(DictValidator):
    def __init__(self, section: str,  allowed_keys: Set[str]):
        super().__init__(section, allowed_keys)

    def validate(self, data: Any):
        if not isinstance(data, list):
            raise TypeError(
                f"Problem processing '{self.section}'." +
                f"Expected a list but got {type(data).__name__}")

        # process the list of items
        for item in data:
            super().validate(item)
