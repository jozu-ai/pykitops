# Copyright 2024 The KitOps Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

"""
Define the Kitfile class to manage KitOps ModelKits and Kitfiles.
"""

import copy
from pathlib import Path
from typing import Any, Dict, List

import yaml

from .utils import IS_A_TTY, Color, clean_empty_items, validate_dict
from .pydantic_kit import PydanticKitfile


class Kitfile(PydanticKitfile):
    """
    Kitfile class now uses Pydantic for validation.
    """

    def __init__(self, path: str | None = None, **kwargs):
        """
        Initialize the Kitfile from a path to an existing Kitfile, or
        create an empty Kitfile.

        Examples:
            >>> kitfile = Kitfile(path="path/to/Kitfile")
            >>> kitfile.yaml()

            >>> kitfile = Kitfile()
            >>> kitfile.manifestVersion = "1.0"
            >>> kitfile.package = {"name": "my_package", "version": "0.1.0",
            ...                    "description": "My package description",
            ...                    "authors": ["Author 1", "Author 2"]}
            >>> kitfile.code = [{"path": "code/", "description": "Code description",
            ...                  "license": "Apache-2.0"}]
            >>> kitfile.datasets = [{"name": "my_dataset", "path": "datasets/",
            ...                      "description": "Dataset description",
            ...                      "license": "Apache-2.0"}]
            >>> kitfile.docs = [{"path": "docs/", "description": "Docs description"}]
            >>> kitfile.model = {"name": "my_model", "path": "model/",
            ...                  "framework": "tensorflow", "version": "2.0.0",
            ...                  "description": "Model description",
            ...                  "license": "Apache-2.0", "parts": [],
            ...                  "parameters": ""}
            >>> kitfile.yaml()
            'manifestVersion: 1.0
             package:
                 name: my_package
                 version: 0.1.0
                 description: My package description
                 authors:
                 - Author 1
                 - Author 2
             code:
             - path: code/
               description: Code description
               license: Apache-2.0
             datasets:
             - name: my_dataset
               path: datasets/
               description: Dataset description
               license: Apache-2.0
             docs:
             - path: docs/
               description: Docs description
             model:
                 name: my_model
                 path: model/
                 framework: tensorflow
                 version: 2.0.0
                 description: Model description
                 license: Apache-2.0'

        Args:
            path (str, optional): Path to existing Kitfile to load. Defaults to None.

        Returns:
            Kitfile (Kitfile): Kitfile object.
        """
        super().__init__(**kwargs)
        self._kitfile_allowed_keys = {
            "manifestVersion",
            "package",
            "code",
            "datasets",
            "docs",
            "model",
        }

        if path:
            self.load(path)

    def load(self, path):
        """
        Load Kitfile data from a yaml-formatted file and set the
        corresponding attributes.

        Args:
            path (str): Path to the Kitfile.
        """
        kitfile_path = Path(path)
        if not kitfile_path.exists():
            raise ValueError(f"Path '{kitfile_path}' does not exist.")

        # try to load the kitfile
        try:
            with open(kitfile_path, "r") as kitfile:
                # Load the yaml data
                data = yaml.safe_load(kitfile)
        except yaml.YAMLError as e:
            if hasattr(e, "problem_mark"):
                mark = e.problem_mark
                raise yaml.YAMLError(
                    "Error parsing Kitfile at "
                    + f"line{mark.line + 1}, "
                    + f"column:{mark.column + 1}."
                ) from e
            else:
                raise

        try:
            validate_dict(value=data, allowed_keys=self._kitfile_allowed_keys)
        except ValueError as e:
            raise ValueError(
                "Kitfile must be a dictionary with allowed "
                + f"keys: {', '.join(self._kitfile_allowed_keys)}"
            ) from e
        # kitfile has been successfully loaded into data
        for key, value in data.items():
            setattr(self, key, value)

    def to_yaml(self, suppress_empty_values: bool = True) -> str:
        """
        Serialize the Kitfile to YAML format.

        Args:
            suppress_empty_values (bool, optional): Whether to suppress
                empty values. Defaults to True.
        Returns:
            str: YAML representation of the Kitfile.
        """
        dict_to_print = self.dict(exclude_unset=True)
        if suppress_empty_values:
            dict_to_print = clean_empty_items(dict_to_print)

        return yaml.safe_dump(
            data=dict_to_print, sort_keys=False, default_flow_style=False
        )

    def print(self) -> None:
        """
        Print the Kitfile to the console.

        Returns:
            None
        """
        print("\n\nKitfile Contents...")
        print("===================\n")
        output = self.to_yaml()
        if IS_A_TTY:
            output = f"{Color.GREEN.value}{output}{Color.RESET.value}"
        print(output)

    def save(self, path: str = "Kitfile", print: bool = True) -> None:
        """
        Save the Kitfile to a file.

        Args:
            path (str): Path to save the Kitfile. Defaults to "Kitfile".
            print (bool): If True, print the Kitfile to the console.
                Defaults to True.

        Returns:
            None

        Examples:
            >>> kitfile = Kitfile()
            >>> kitfile.save("path/to/Kitfile")
        """
        with open(path, "w") as file:
            file.write(self.yaml())

        if print:
            self.print()

    def yaml(self) -> str:
        """
        Use Pydantic's dict() or json() to generate YAML.

        Returns:
            str: YAML representation of the Kitfile.
        """
        return yaml.safe_dump(self.dict(exclude_unset=True), sort_keys=False)
