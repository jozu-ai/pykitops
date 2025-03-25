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

from pathlib import Path
from typing import Optional
from warnings import warn

import yaml

from .pydantic_kit import (
    ALLOWED_KEYS,
    CodeEntry,
    DatasetEntry,
    DocsEntry,
    ModelSection,
    Package,
    PydanticKitfile,
)
from .utils import IS_A_TTY, Color


class Kitfile(PydanticKitfile):
    """
    Kitfile class using Pydantic for validation.
    """

    def __init__(
        self,
        path: Optional[str | None] = None,
    ) -> None:
        """
        Initialize the Kitfile from a path to an existing Kitfile, or
        create an empty Kitfile.

        Args:
            path (str, optional): Path to existing Kitfile to load. Defaults to None.

        Returns:
            None

        Examples:
            >>> from kitops.modelkit import Kitfile
            ...
            >>> kitfile = Kitfile(path="path/to/Kitfile")
            >>> kitfile.to_yaml()

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
            >>> kitfile.to_yaml()
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
        """
        if path:
            self.load(path)

    def build(
        self,
        manifestVersion: str,
        package: Package | dict,
        code: Optional[list[CodeEntry | dict]] = None,
        datasets: Optional[list[DatasetEntry | dict]] = None,
        docs: Optional[list[DocsEntry | dict]] = None,
        model: Optional[ModelSection | dict] = None,
    ) -> None:
        """
        Build a Kitfile from the provided data.

        Args:
            manifestVersion (str): Specifies the manifest format version.
            package (Package | dict): This section provides general information about the AI/ML project.
            code (Optional[list[CodeEntry | dict]], optional): Information about the source code. Defaults to None.
            datasets (Optional[list[DatasetEntry | dict]], optional): Information for the datasets. Defaults to None.
            docs (Optional[list[DocsEntry | dict]], optional): Included documentation for the model. Defaults to None.
            model (Optional[ModelSection | dict], optional): Details of the models included. Defaults to None.
        """
        super().__init__(
            manifestVersion=manifestVersion,
            package=Package.model_validate(package),
            code=[CodeEntry.model_validate(c) for c in code] if code is not None else [],
            datasets=[DatasetEntry.model_validate(d) for d in datasets] if datasets is not None else [],
            docs=[DocsEntry.model_validate(d) for d in docs] if docs is not None else [],
            model=ModelSection.model_validate(model) if model is not None else None,
        )

    def load(self, path: str) -> None:
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
            data: dict = yaml.safe_load(kitfile_path.read_text(encoding="utf-8"))
        except yaml.YAMLError as e:
            if mark := getattr(e, "problem_mark", None):
                raise yaml.YAMLError(f"Error parsing Kitfile at line{mark.line + 1}, column:{mark.column + 1}.") from e
            else:
                raise

        if any(ALLOWED_KEYS.difference(data.keys())):
            raise ValueError("Kitfile must be a dictionary with allowed " + f"keys: {', '.join(ALLOWED_KEYS)}")
        # kitfile has been successfully loaded into data
        self.build(**data)

    def to_yaml(self, suppress_empty_values: bool = True) -> str:
        """
        Serialize the Kitfile to YAML format.

        Args:
            suppress_empty_values (bool, optional): Whether to suppress
                empty values. Defaults to True.
        Returns:
            str: YAML representation of the Kitfile.
        """
        return yaml.safe_dump(
            data=self.model_dump(exclude_unset=suppress_empty_values, exclude_none=suppress_empty_values),
            sort_keys=False,
            default_flow_style=False,
        )

    def print(self) -> None:
        """
        Print the Kitfile to the console.

        Returns:
            None
        """
        warn(
            "Kitfile.print() is going to be deprecated. "
            "To print Kitfile use to_yaml() and your favorite way to log/print; date=2025-02-21",
            DeprecationWarning,
            stacklevel=2,
        )
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
        Path(path).write_text(self.to_yaml(), encoding="utf-8")

        if print:
            warn(
                "print argument is going to be deprecated. "
                "To print Kitfile use to_yaml() and your favorite way to log/print; date=2025-02-21",
                DeprecationWarning,
                stacklevel=2,
            )
            self.print()
