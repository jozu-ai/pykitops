from pathlib import Path
from typing import Any, Optional, Self

from pydantic import BaseModel, Field, model_validator


class BasePathModel(BaseModel):
    """Base class for validating paths."""

    path: str

    @model_validator(mode="after")
    def validate_path(self) -> Self:
        """Validate that the path exists."""
        if not Path(self.path).exists():
            raise FileNotFoundError(f"Path '{self.path}' not found.")
        if Path(self.path).is_absolute():
            try:
                self.path = Path(self.path).relative_to(Path.cwd()).as_posix()
            except ValueError:
                raise ValueError("Path must be relative to the current working directory.")
        return self


class Package(BaseModel):
    """
    This section provides general information about the AI/ML project.

    Args:
        name (str): The name of the AI/ML project.
        version (str): The current version of the project.
        description (str): A brief overview of the project's purpose and capabilities.
        authors (list[str]): A list of individuals or entities that have contributed to the project.
    """

    name: str = Field(..., description="The name of the AI/ML project.")
    version: str = Field(
        ...,
        description="The current version of the project.",
        examples=["1.2.3", "0.13a"],
        coerce_numbers_to_str=True,
    )
    description: str = Field(..., description="A brief overview of the project's purpose and capabilities.")
    authors: list[str] = Field(
        ..., description="A list of individuals or entities that have contributed to the project.", min_length=1
    )

    @model_validator(mode="after")
    def validate_authors(self) -> Self:
        """Validate that authors is a list of strings."""
        if not all(isinstance(a, str) for a in self.authors):
            raise ValueError("Authors must be a list of strings.")
        return self


class CodeEntry(BasePathModel):
    """
    Single entry with information about the source code.

    Args:
        path (str): Location of the source code file or directory relative to the context.
        description (str): Description of what the code does.
        license (str): SPDX license identifier for the code.
    """

    path: str = Field(..., description="Location of the source code file or directory relative to the context.")
    description: str = Field(..., description=" Description of what the code does.")
    license: str = Field(..., description="SPDX license identifier for the code.")


class DatasetEntry(BasePathModel):
    """
    Single entry with information about the datasets used.

    Args:
        name (str): Name of the dataset.
        path (str): Location of the dataset file or directory relative to the context.
        description (str): Overview of the dataset.
        license (str): SPDX license identifier for the dataset.
    """

    name: str = Field(..., description=" Name of the dataset.")
    path: str = Field(..., description="Location of the dataset file or directory relative to the context.")
    description: str = Field(..., description="Overview of the dataset.")
    license: str = Field(..., description="SPDX license identifier for the dataset.")


class DocsEntry(BasePathModel):
    """
    Single entry with information about included documentation for the model.

    Args:
        description (str): Description of the documentation.
        path (str): Location of the documentation relative to the context.
    """

    description: str = Field(..., description="Description of the documentation.")
    path: str = Field(..., description="Location of the documentation relative to the context.")


class ModelPart(BasePathModel):
    """
    One entry of the related files for the model, e.g. model weights.

    Args:
        name (str): Identifier for the part.
        path (str): Location of the file or a directory relative to the context.
        type (str): The type of the part (e.g. LoRA weights).
    """

    name: str = Field(..., description="Identifier for the part.")
    path: str = Field(..., description="Location of the file or a directory relative to the context.")
    type: str = Field(..., description="The type of the part (e.g. LoRA weights).")


class ModelSection(BasePathModel):
    """
    Details of the trained models included in the package.

    Args:
        name (str): Name of the model.
        path (str): Location of the model file or directory relative to the context.
        framework (str): AI/ML framework.
        version (str): Version of the model.
        description (str): Overview of the model.
        license (str): SPDX license identifier for the model.
        parts (list[ModelPart]): List of related files for the model (e.g. LoRA weights).
        parameters (Any): An arbitrary section of YAML that can be used to store any additional data that may be 
            relevant to the current model.
    """

    name: str = Field(..., description="Name of the model.")
    path: str = Field(..., description="Location of the model file or directory relative to the context.")
    framework: str = Field(..., description="AI/ML framework.", examples=["tensorflow", "pytorch", "onnx", "TensorRT"])
    version: str = Field(
        ...,
        description="Version of the model.",
        examples=["0.0a13", "1.8.0"],
        coerce_numbers_to_str=True,
    )
    description: str = Field(..., description="Overview of the model.")
    license: str = Field(..., description="SPDX license identifier for the model.")
    parts: Optional[list[ModelPart]] = Field(
        default_factory=lambda: [], description="List of related files for the model (e.g. LoRA weights)."
    )
    parameters: Optional[Any] = Field(
        None,
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

    manifestVersion: str = Field(
        ...,
        description="Specifies the manifest format version.",
        examples=["1.0.0", "0.13a"],
        coerce_numbers_to_str=True,
    )
    package: Package = Field(..., description="This section provides general information about the AI/ML project.")
    code: Optional[list[CodeEntry]] = Field(
        default_factory=lambda: [], description="Information about the source code."
    )
    datasets: Optional[list[DatasetEntry]] = Field(
        default_factory=lambda: [], description="Information about the datasets used."
    )
    docs: Optional[list[DocsEntry]] = Field(
        default_factory=lambda: [], description="Information about included documentation for the model."
    )
    model: Optional[ModelSection] = Field(None, description="Details of the trained models included in the package.")

    @model_validator(mode="after")
    def check_attrs(self) -> Self:
        if not any(getattr(self, e, None) for e in set(self.model_fields)):
            raise AttributeError("At least one of 'code', 'datasets', 'docs', or 'model' is required.")
        return self


ALLOWED_KEYS = set(PydanticKitfile.model_fields)
