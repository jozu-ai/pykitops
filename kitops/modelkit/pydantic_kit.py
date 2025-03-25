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
Define the PydanticKitfile class as parent to Kitfile.
"""

from pathlib import Path
from typing import Any, Optional, Self

from pydantic import BaseModel, DirectoryPath, Field, FilePath, model_validator


class BasePathModel(BaseModel):
    """Base class for validating paths."""

    path: FilePath | DirectoryPath

    @model_validator(mode="after")
    def validate_path(self) -> Self:
        """Validate that the path exists."""
        if not Path(self.path).exists():
            raise FileNotFoundError(f"Path '{self.path}' not found.")
        if Path(self.path).is_absolute():
            try:
                self.path = Path(self.path).relative_to(Path.cwd())
            except ValueError:
                raise ValueError("Path must be relative to the current working directory.")
        return self


class Package(BaseModel):
    """
    This section provides general information about the AI/ML project.

    Args:
        name (Optional[str]): The name of the AI/ML project.
        version (Optional[str]): The current version of the project.
        description (Optional[str]): A brief overview of the project's purpose and capabilities.
        authors (list[str]): A list of individuals or entities that have contributed to the project.
    """

    name: Optional[str] = ""
    version: Optional[str] = Field(default="", examples=["1.2.3", "0.13a"], coerce_numbers_to_str=True)
    description: Optional[str] = ""
    authors: Optional[list[str]] = []


class CodeEntry(BasePathModel):
    """
    Single entry with information about the source code.

    Args:
        path (FilePath): Location of the source code file or directory relative to the context.
        description (Optional[str]): Description of what the code does.
        license (Optional[str]): SPDX license identifier for the code.
    """

    description: Optional[str] = ""
    license: Optional[str] = ""


class DatasetEntry(BasePathModel):
    """
    Single entry with information about the datasets used.

    Args:
        name (str): Name of the dataset.
        path (FilePath): Location of the dataset file or directory relative to the context.
        description (str): Overview of the dataset.
        license (str): SPDX license identifier for the dataset.
    """

    name: Optional[str] = ""
    description: Optional[str] = ""
    license: Optional[str] = ""


class DocsEntry(BasePathModel):
    """
    Single entry with information about included documentation for the model.

    Args:
        path (FilePath): Location of the documentation relative to the context.
        description (Optional[str]): Description of the documentation.
    """

    description: Optional[str] = ""


class ModelPart(BasePathModel):
    """
    One entry of the related files for the model, e.g. model weights.

    Args:
        path (FilePath): Location of the file or a directory relative to the context.
        name (Optional[str]): Identifier for the part.
        type (Optional[str]): The type of the part (e.g. LoRA weights).
    """

    name: Optional[str] = ""
    type: Optional[str] = ""


class ModelSection(BasePathModel):
    """
    Details of the trained models included in the package.

    Args:
        path (FilePath): Location of the model file or directory relative to the context.
        name (Optional[str]): Name of the model.
        framework (Optional[str]): AI/ML framework.
        version (Optional[str]): Version of the model.
        description (Optional[str]): Overview of the model.
        license (Optional[str]): SPDX license identifier for the model.
        parts (Optional[list[ModelPart]]): List of related files for the model (e.g. LoRA weights).
        parameters (Optional[Any]): An arbitrary section of YAML that can be used to store any additional data that may
            be relevant to the current model.
    """

    name: Optional[str] = ""
    framework: Optional[str] = Field(default="", examples=["tensorflow", "pytorch", "onnx", "TensorRT"])
    version: Optional[str] = Field(default="", examples=["0.0a13", "1.8.0"], coerce_numbers_to_str=True)
    description: Optional[str] = ""
    license: Optional[str] = ""
    parts: Optional[list[ModelPart]] = []
    parameters: Optional[Any] = Field(
        default=None,
        description=(
            "An arbitrary section of YAML that can be used to store any additional data that may be relevant to the"
            " current model, with a few caveats. Only a json-compatible subset of YAML is supported. Strings will be "
            "serialized without flow parameters. Numbers will be converted to decimal representations (0xFF -> 255, "
            "1.2e+3 -> 1200). Maps will be sorted alphabetically by key."
        ),
    )


class PydanticKitfile(BaseModel):
    """
    Base class for the Pydantic Kitfile model.

    Args:
        manifestVersion (str): Specifies the manifest format version.
        package (Package): This section provides general information about the AI/ML project.
        code (Optional[list[CodeEntry]]): Information about the source code.
        datasets (Optional[list[DatasetEntry]]): Information about the datasets used.
        docs (Optional[list[DocsEntry]]): Information about included documentation for the model.
        model (Optional[ModelSection]): Details of the trained models included in the package.
    """

    manifestVersion: str = Field(default=..., examples=["1.0.0", "0.13a"], coerce_numbers_to_str=True)
    package: Optional[Package] = Package()
    code: Optional[list[CodeEntry]] = []
    datasets: Optional[list[DatasetEntry]] = []
    docs: Optional[list[DocsEntry]] = []
    model: Optional[ModelSection] = None


ALLOWED_KEYS = set(PydanticKitfile.model_fields)
