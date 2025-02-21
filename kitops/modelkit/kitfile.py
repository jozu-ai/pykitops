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
from typing import Any, Dict, List, Set
from warnings import warn

import yaml

from .utils import IS_A_TTY, Color, clean_empty_items, validate_dict
from .validators.code_validator import CodeValidator
from .validators.datasets_validator import DatasetsValidator
from .validators.docs_validator import DocsValidator
from .validators.manifest_version_validator import ManifestVersionValidator
from .validators.model_validator import ModelValidator
from .validators.package_validator import PackageValidator


class Kitfile:
    """
    Kitfile class to manage KitOps ModelKits and Kitfiles.

    Attributes:
        path (str): Path to the Kitfile.
    """

    def __init__(self, path: str | None = None) -> None:
        """
        Initialize the Kitfile from a path to an existing Kitfile, or
        create an empty Kitfile.

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

        Args:
            path (str, optional): Path to existing Kitfile to load. Defaults to None.

        Returns:
            Kitfile (Kitfile): Kitfile object.
        """
        self._data: Dict = {}
        self._kitfile_allowed_keys: Set[str] = {
            "manifestVersion",
            "package",
            "code",
            "datasets",
            "docs",
            "model",
        }

        # initialize the kitfile section validators
        self._initialize_kitfile_section_validators()

        # initialize an empty kitfile object
        self.manifestVersion = ""
        self.package = {"name": "", "version": "", "description": "", "authors": []}
        self.code = []
        self.datasets = []
        self.docs = []
        self.model = {
            "name": "",
            "path": "",
            "description": "",
            "framework": "",
            "license": "",
            "version": "",
            "parts": [],
            "parameters": "",
        }

        if path:
            self.load(path)

    def _initialize_kitfile_section_validators(self) -> None:
        """
        Initialize validators for Kitfile sections.
        """
        self._manifestVersion_validator = ManifestVersionValidator(section="manifestVersion", allowed_keys=set())
        self._package_validator = PackageValidator(
            section="package",
            allowed_keys={"name", "version", "description", "authors"},
        )
        self._code_validator = CodeValidator(section="code", allowed_keys={"path", "description", "license"})
        self._datasets_validator = DatasetsValidator(
            section="datasets", allowed_keys={"name", "path", "description", "license"}
        )
        self._docs_validator = DocsValidator(section="docs", allowed_keys={"path", "description"})
        self._model_validator = ModelValidator(
            section="model",
            allowed_keys={
                "name",
                "path",
                "framework",
                "version",
                "description",
                "license",
                "parts",
                "parameters",
            },
        )

    def _validate_and_set_attributes(self, data: Dict[str, Any]) -> None:
        """
        Validate and set attributes from the provided data.

        Args:
            data (Dict[str, Any]): Data to validate and set.
        """
        for key, value in data.items():
            self.__setattr__(key, value)

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
            data = yaml.safe_load(kitfile_path.read_text(encoding="utf-8"))

        except yaml.YAMLError as e:
            if mark := getattr(e, "problem_mark", None):
                raise yaml.YAMLError(
                    "Error parsing Kitfile at " + f"line{mark.line + 1}, " + f"column:{mark.column + 1}."
                ) from e
            else:
                raise

        try:
            validate_dict(value=data, allowed_keys=self._kitfile_allowed_keys)
        except ValueError as e:
            raise ValueError(
                "Kitfile must be a dictionary with allowed " + f"keys: {', '.join(self._kitfile_allowed_keys)}"
            ) from e
        # kitfile has been successfully loaded into data
        self._validate_and_set_attributes(data)

    @property
    def manifestVersion(self) -> str:
        """
        Get the manifest version.

        Returns:
            str: Manifest version.
        """
        return self._data["manifestVersion"]

    @manifestVersion.setter
    def manifestVersion(self, value: str) -> None:
        """
        Set the manifest version.

        Args:
            value (str): Manifest version.
        """
        self._manifestVersion_validator.validate(data=value)
        self._data["manifestVersion"] = value

    @property
    def package(self) -> Dict[str, Any]:
        """
        Get the package information.

        Returns:
            Dict[str, Any]: Package information.
        """
        return self._data["package"]

    @package.setter
    def package(self, value: Dict[str, Any]) -> None:
        """
        Set the package information.

        Args:
            value (Dict[str, Any]): Package information.
        """
        self._package_validator.validate(data=value)
        self._data["package"] = value

    @property
    def code(self) -> List[Dict[str, Any]]:
        """
        Get the code section.

        Returns:
            List[Dict[str, Any]]: Code section.
        """
        return self._data["code"]

    @code.setter
    def code(self, value: List[Dict[str, Any]]) -> None:
        """
        Set the code section.

        Args:
            value (List[Dict[str, Any]]): Code section.
        """
        self._code_validator.validate(data=value)
        self._data["code"] = value

    @property
    def datasets(self) -> List[Dict[str, Any]]:
        """
        Get the datasets section.

        Returns:
            List[Dict[str, Any]]: Datasets section.
        """
        return self._data["datasets"]

    @datasets.setter
    def datasets(self, value: List[Dict[str, Any]]) -> None:
        """
        Set the datasets section.

        Args:
            value (List[Dict[str, Any]]): Datasets section.
        """
        self._datasets_validator.validate(data=value)
        self._data["datasets"] = value

    @property
    def docs(self) -> List[Dict[str, Any]]:
        """
        Get the docs section.

        Returns:
            List[Dict[str, Any]]: Docs section.
        """
        return self._data["docs"]

    @docs.setter
    def docs(self, value: List[Dict[str, Any]]) -> None:
        """
        Set the docs section.

        Args:
            value (List[Dict[str, Any]]): Docs section.
        """
        self._docs_validator.validate(data=value)
        self._data["docs"] = value

    @property
    def model(self) -> Dict[str, Any]:
        """
        Get the model section.

        Returns:
            Dict[str, Any]: Model section.
        """
        return self._data["model"]

    @model.setter
    def model(self, value: Dict[str, Any]) -> None:
        """
        Set the model section.

        Args:
            value (Dict[str, Any]): Model section.
        """
        self._model_validator.validate(data=value)
        self._data["model"] = value

    def to_yaml(self, suppress_empty_values: bool = True) -> str:
        """
        Serialize the Kitfile to YAML format.

        Args:
            suppress_empty_values (bool, optional): Whether to suppress
                empty values. Defaults to True.
        Returns:
            str: YAML representation of the Kitfile.
        """
        dict_to_print: Dict = self._data
        if suppress_empty_values:
            dict_to_print = copy.deepcopy(self._data)
            dict_to_print = clean_empty_items(dict_to_print)

        return yaml.safe_dump(data=dict_to_print, sort_keys=False, default_flow_style=False)

    def print(self) -> None:
        """
        Print the Kitfile to the console.

        Returns:
            None
        """
        warn(
            "Kitfile.print() is going to be deprecated. " \
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
                "print argument is going to be deprecated. " \
                "To print Kitfile use to_yaml() and your favorite way to log/print; date=2025-02-21",
                DeprecationWarning,
                stacklevel=2,
            )
            self.print()
