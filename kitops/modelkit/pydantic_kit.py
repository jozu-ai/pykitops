from pydantic import BaseModel, model_validator
from typing import Any, Dict, List, Optional, Set, Self


class Package(BaseModel):
    name: str
    version: str
    description: str
    authors: List[str]

    @model_validator(mode="after")
    def validate_authors(self) -> Self:
        if not isinstance(self.authors, list):
            raise ValueError("Authors must be a list of strings.")
        return Self


class CodeEntry(BaseModel):
    path: str
    description: str
    license: str


class DatasetEntry(BaseModel):
    name: str
    path: str
    description: str
    license: str


class DocsEntry(BaseModel):
    path: str
    description: str


class ModelPart(BaseModel):
    name: str
    path: str
    type: str


class ModelSection(BaseModel):
    name: str
    path: str
    framework: str
    version: str
    description: str
    license: str
    parts: List[ModelPart]
    parameters: Any


class PydanticKitfile(BaseModel):
    manifestVersion: str
    package: Package
    code: List[CodeEntry]
    datasets: List[DatasetEntry]
    docs: List[DocsEntry]
    model: ModelSection
