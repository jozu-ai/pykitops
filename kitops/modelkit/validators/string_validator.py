"""
Copyright 2024 The KitOps Authors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

SPDX-License-Identifier: Apache-2.0
"""

from typing import Any, Set


class StringValidator:
    def __init__(self, section: str, allowed_keys: Set[str]):
        self.section = section
        self.allowed_keys = allowed_keys

    @property
    def section(self):
        return self._section

    @section.setter
    def section(self, value):
        self._section = value

    @property
    def allowed_keys(self):
        return self._allowed_keys

    @allowed_keys.setter
    def allowed_keys(self, values):
        self._allowed_keys = values

    def validate(self, data: Any):
        if not isinstance(data, str):
            raise TypeError(
                f"Problem processing '{self.section}'. "
                + f"Expected a string but got {type(data).__name__}"
            )
