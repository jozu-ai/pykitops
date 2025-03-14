import os
import shutil

from kitops.modelkit.manager import ModelKitManager
from kitops.modelkit.pydantic_kit import ModelSection


def clean_temp_dir():
    # Remove the temp directory if they already exist
    directory = "temp"
    if os.path.exists(directory):
        shutil.rmtree("temp")


def setup():
    # delete the temp directory and its contents
    clean_temp_dir()

    # remove the "titanic-survivability:latest" ModelKit from the
    # local and remote registries
    modelkit_tag = "jozu.ml/brett/titanic-survivability:latest"
    manager = ModelKitManager(modelkit_tag=modelkit_tag)
    manager.remove_modelkit(local=True, remote=True)

    # remove the "titanic-survivability:processed-data-v5" ModelKit
    # from the local registry, only.
    modelkit_tag = "jozu.ml/brett/titanic-survivability:processed-data-v5"
    manager = ModelKitManager(modelkit_tag=modelkit_tag)
    manager.remove_modelkit(local=True, remote=False)

    # remove the "titanic-survivability:trained_model_v2" ModelKit
    # from the local registry, only.
    modelkit_tag = "jozu.ml/brett/titanic-survivability:trained_model_v2"
    manager = ModelKitManager(modelkit_tag=modelkit_tag)
    manager.remove_modelkit(local=True, remote=False)

    # pull and unpack a clean version of the
    # "titanic-survivability:trained_model_v2" ModelKit
    manager.working_directory = "temp/titanic-full"
    manager.pull_and_unpack_modelkit(load_kitfile=False)


# kit.logout(registry = manager.user_credentials.registry)
def build_model():
    # Define the source and destination directories
    source_dir = "temp/titanic-full/model"
    destination_dir = "temp/titanic-partial/model"

    # Remove the destination directory if it already exists
    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)

    # Copy the directory
    shutil.copytree(source_dir, destination_dir)

    print(f"Directory copied from {source_dir} to {destination_dir}")


#####################################################################

setup()

# get a fresh copy of the "titanic-survivability:processed-data-v5" ModelKit
modelkit_tag = "jozu.ml/brett/titanic-survivability:processed-data-v5"
manager = ModelKitManager(
    working_directory="temp/titanic-partial", modelkit_tag=modelkit_tag
)
manager.pull_and_unpack_modelkit(load_kitfile=True)
manager.kitfile.print()

build_model()

# update the Kitfile
kitfile = manager.kitfile
kitfile.model = ModelSection.model_validate({
        "name": "titanic-survivability-predictor",
        "path": "model/model.joblib",
        "license": "Apache 2.0",
        "framework": "scikit-learn",
        "version": "1.0",
        "description": "RandomForestClassifier",
    }
)
manager.kitfile.print()

# update the ModelKit's tag to "latest"
manager.modelkit_reference.tag = "latest"
# pack and push the ModelKit to Jozu.ml
manager.pack_and_push_modelkit(save_kitfile=True)
