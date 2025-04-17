import re
import os


def split_file_name(file_name: str) -> tuple[str, str]:
    base_name = os.path.splitext(file_name)[0]
    extension = os.path.splitext(file_name)[1]
    return base_name, extension


def add_file_version(file_name: str) -> str:
    base_name, extension = split_file_name(file_name)
    # Match one or more digits at the end of the string
    match = re.search(r'ver_(\d+)$', base_name)
    if match:
        next_number = int(match.group(1)) + 1
        return re.sub(r'ver_\d+$', f"ver_{next_number}", base_name) + extension
    else:
        return base_name + "_ver_1" + extension
