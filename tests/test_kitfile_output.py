# Usage
import os

from kitops.modelkit.kitfile import Kitfile
from kitops.modelkit.pydantic_kit import Package


def test_everything(fixtures: dict[str, str]):
    current_directory = os.getcwd()
    print(current_directory)

    path = fixtures["Kitfile_full"]
    kitfile = Kitfile(path=str(path))

    print("kitfile.manifestVersion: " + kitfile.manifestVersion)
    print("kitfile.package: ")
    print(kitfile.package)
    print("=======================================================")

    # Serialize to YAML
    yaml_data = kitfile.to_yaml()
    print(yaml_data)
    print("=======================================================")

    kitfile.manifestVersion = "2.0"
    kitfile.package = Package.model_validate(
        {
            "name": "New-Package",
            "version": "2.0.0",
            "description": "New description",
            "authors": ["Author"],
        }
    )

    print("kitfile.manifestVersion: " + kitfile.manifestVersion)
    print("kitfile.package: ")
    print(kitfile.package)
    print("=======================================================")
    # Serialize to YAML
    yaml_data = kitfile.to_yaml()
    print(yaml_data)
    print("=======================================================")

    # Create an empty Kitfile and update attributes
    kitfile = Kitfile()

    print("=======================================================")
    # Serialize to YAML
    yaml_data = kitfile.to_yaml()
    print(yaml_data)
    print("=======================================================")

    kitfile.manifestVersion = "3.0"
    kitfile.package = Package.model_validate(
        {
            "name": "Another-Package",
            "version": "3.0.0",
            "description": "Another description",
            "authors": ["Someone"],
        }
    )

    print("=======================================================")
    # Serialize to YAML
    yaml_data = kitfile.to_yaml()
    print(yaml_data)
    print("=======================================================")
