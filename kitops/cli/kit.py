import subprocess
from typing import Any, List, Optional
from ..modelkit.utils import Color, IS_A_TTY
from .utils import _process_command_flags


def info(repo_path_with_tag: str, 
         filters: Optional[List[str]] = None, **kwargs):
    """
    Retrieve information about a kit repository.

    Args:
        repo_path_with_tag (str): The path to the repository along with the tag.
        remote (Optional[bool]): If True, include the remote flag in the command. Defaults to True.

    Returns:
        None
    """
    command = ["kit", "info",  
               repo_path_with_tag]
    if filters:
        for filter in filters:
            command.append("--filter")
            command.append(filter)
 
    command.extend(_process_command_flags(kit_cmd_name="info", **kwargs))
    _run(command=command)

def inspect(repo_path_with_tag: str, remote: Optional[bool] = True, **kwargs):
    """
    Inspect a repository using the 'kit' command.

    Parameters:
    repo_path_with_tag (str): The path to the repository along with the tag.
    remote (Optional[bool]): Flag to indicate if the inspection should be done remotely. Defaults to True.
        Otherwise, the inspection will be done locally.

    Returns:
        None
    """
    command = ["kit", "inspect", 
                repo_path_with_tag]

    command.extend(_process_command_flags(kit_cmd_name="inspect", **kwargs))
    _run(command=command)

def list(repo_path_without_tag: Optional[str] = None, **kwargs):
    """
    Lists the ModelKits available in the specified repository path.

    Args:
        repo_path_without_tag (Optional[str]): The path to the repository without the tag. 
                                               If not provided, lists kits from the local registry.

    Returns:
        None
    """
    command = ["kit", "list"]
    if repo_path_without_tag:
        command.append(repo_path_without_tag)

    command.extend(_process_command_flags(kit_cmd_name="list", **kwargs))
    _run(command=command)

def login(user: str, passwd: str, registry: str = "jozu.ml", **kwargs):
    """
    Logs in to the specified registry using the provided username and password.

    Args:
        user (str): The username for the registry.
        passwd (str): The password for the registry.
        registry (str, optional): The registry URL. Defaults to "jozu.ml".

    Returns:
        None
    """
    command = [
        "kit", "login", registry,
        "--username", user,
        "--password-stdin"
    ]

    command.extend(_process_command_flags(kit_cmd_name="login", **kwargs))
    _run(command=command, input=passwd)

def logout(registry: str = "jozu.ml", **kwargs):
    """
    Logs out from the specified registry.

    Args:
        registry (str, optional): The registry to log out from. Defaults to "jozu.ml".

    Returns:
        None
    """
    command = ["kit", "logout", registry]

    command.extend(_process_command_flags(kit_cmd_name="logout", **kwargs))
    _run(command=command)

def pack(repo_path_with_tag: str, **kwargs):
    """
    Packs the current directory into a ModelKit package with a specified tag.

    Args:
        repo_path_with_tag (str): The repository path along with the tag to be used for the package.

    Returns:
        None
    """
    command = ["kit", "pack", ".", 
               "--tag", repo_path_with_tag]

    command.extend(_process_command_flags(kit_cmd_name="pack", **kwargs))
    _run(command=command)

def pull(repo_path_with_tag: str, **kwargs):
    """
    Pulls the specified ModelKit from the remote registry.

    Args:
        repo_path_with_tag (str): The path to the repository along with the tag to pull.

    Returns:
        None
    """
    command = ["kit", "pull", 
               repo_path_with_tag]

    command.extend(_process_command_flags(kit_cmd_name="pull", **kwargs))
    _run(command=command)

def push(repo_path_with_tag: str, **kwargs):
    """
    Pushes the specified ModelKit to the remote registry.

    Args:
        repo_path_with_tag (str): The path to the repository along with the tag to be pushed.

    Returns:
        None
    """
    command = ["kit", "push", 
               repo_path_with_tag]

    command.extend(_process_command_flags(kit_cmd_name="push", **kwargs))
    _run(command=command)

def remove(repo_path_with_tag: str, **kwargs):
    """
    Remove a ModelKit from the registry.

    Args:
        repo_path_with_tag (str): The path to the repository with its tag.

    Returns:
        None
    """
    command = ["kit", "remove",  
               repo_path_with_tag]

    command.extend(_process_command_flags(kit_cmd_name="remove", **kwargs))

    try:
        _run(command=command)
    except subprocess.CalledProcessError as e:
        # If the repository is not found in the registry, ignore the error
        pass

def unpack(repo_path_with_tag: str, dir: str, 
           filters: Optional[List[str]], **kwargs):
    """
    Unpacks a ModelKit to the specified directory from the remote registry.

    This function constructs a command to unpack a ModelKit and 
    calls an internal function to execute the command.

    Args:
        repo_path_with_tag (str): The path to the repository along with 
            the tag to be unpacked.
        dir (str): The directory to unpack the ModelKit to.

    Returns:
        None
    """
    command = ["kit", "unpack", 
               "--dir", dir, 
               repo_path_with_tag]
    if filters:
        for filter in filters:
            command.append("--filter")
            command.append(filter)

    command.extend(_process_command_flags(kit_cmd_name="unpack", **kwargs))
    _run(command=command)

def version(**kwargs):
    """
    Lists the version of the KitOps Command-line Interface (CLI).

    Args:
        None

    Returns:
        None
    """
    command = ["kit", "version"]

    command.extend(_process_command_flags(kit_cmd_name="version", **kwargs))
    _run(command=command)


def _run(command: List[Any], input: Optional[str] = None, 
         verbose: bool = True, **kwargs):
    """
    Executes a command in the system shell.

    Args:
        command (List[Any]): The command to be executed as a list of strings.
        input (Optional[str]): Optional input to be passed to the command.
        verbose (bool): If True, print the command before executing. Defaults to True.

    Returns:
        None

    Raises:
        subprocess.CalledProcessError: If the command returns a non-zero exit status.
    """
    if verbose:
        output = '% ' + ' '.join(command)
        if IS_A_TTY:
            output = f"{Color.CYAN.value}{output}{Color.RESET.value}"
        print(output, flush=True)

    subprocess.run(command, input=input, text=True, check=True)