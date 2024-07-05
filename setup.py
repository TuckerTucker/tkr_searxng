import subprocess
import logging
from typing import Optional, List, Tuple
import configparser
from pathlib import Path
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_submodule_paths() -> List[Tuple[Path, str]]:
    """
    Retrieve submodule paths and URLs from the .gitmodules file.

    :return: List of tuples containing submodule paths and URLs.
    """
    logging.info("Retrieving submodule paths and URLs from .gitmodules.")
    submodule_info = []
    config = configparser.ConfigParser()
    config.read('.gitmodules')
    
    for section in config.sections():
        if section.startswith('submodule'):
            path = config[section].get('path')
            url = config[section].get('url')
            if path and url:
                submodule_info.append((Path(path), url))
    
    logging.info(f"Found submodule info: {submodule_info}")
    return submodule_info

def is_submodule_cloned(submodule_path: Path, check_file: Optional[str] = None) -> bool:
    """
    Check if a submodule has been cloned.

    :param submodule_path: Path to the submodule directory.
    :param check_file: Optional specific file to check within the submodule directory.
    :return: True if the submodule is cloned, False otherwise.
    """
    logging.info(f"Checking if submodule at '{submodule_path}' is cloned.")
    
    if not submodule_path.is_dir():
        logging.warning(f"Submodule directory '{submodule_path}' does not exist.")
        return False
    
    if not any(submodule_path.iterdir()):
        logging.warning(f"Submodule directory '{submodule_path}' is empty.")
        return False
    
    if check_file:
        check_file_path = submodule_path / check_file
        if not check_file_path.is_file():
            logging.warning(f"Expected file '{check_file}' not found in submodule directory.")
            return False
    
    logging.info(f"Submodule at '{submodule_path}' is cloned.")
    return True

def clone_submodule(submodule_path: Path, submodule_url: str):
    """
    Clone the submodule.

    :param submodule_path: Path to the submodule directory.
    :param submodule_url: URL of the submodule repository.
    """
    logging.info(f"Cloning submodule at '{submodule_path}' from URL '{submodule_url}'.")
    try:
        subprocess.run(['git', 'submodule', 'add', submodule_url, str(submodule_path)], check=True)
        logging.info(f"Submodule at '{submodule_path}' cloned successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to clone submodule at '{submodule_path}': {e}")

def copy_settings_file(src: Path, dest: Path):
    """
    Copy the settings file to the specified destination.

    :param src: Source file path.
    :param dest: Destination file path.
    """
    logging.info(f"Copying settings file from '{src}' to '{dest}'.")
    try:
        shutil.copyfile(src, dest)
        logging.info(f"Settings file copied successfully from '{src}' to '{dest}'.")
    except IOError as e:
        logging.error(f"Failed to copy settings file from '{src}' to '{dest}': {e}")

# Example usage
submodule_info = get_submodule_paths()
check_file = 'expected_file_in_submodule.txt'  # Optional

for submodule_path, submodule_url in submodule_info:
    if is_submodule_cloned(submodule_path, check_file):
        logging.info(f"Submodule '{submodule_path}' is already cloned.")
    else:
        logging.info(f"Submodule '{submodule_path}' is not cloned. Cloning now...")
        clone_submodule(submodule_path, submodule_url)

# Copy the settings file after cloning the submodules
src_settings_file = Path('tkr.searxng.settings.yml')
dest_settings_file = Path('searxng-docker/searxng/settings.yml')
copy_settings_file(src_settings_file, dest_settings_file)

# src_settings_file = Path('tkr.docker-compose.yaml')
# dest_settings_file = Path('searxng-docker/docker-compose.yaml')
# copy_settings_file(src_settings_file, dest_settings_file)
