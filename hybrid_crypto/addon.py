import os
import re
import hashlib


def get_SHA256(file_path: str | os.PathLike, file_extension: bool = False) -> str:
    """
    Get SHA256 hash from file

    :param file_path: file location path
    :param file_extension: get hash including file extension
    :raise FileNotFoundError: if file path is not found
    :rtype: string
    """
    SHA256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while True:
            f_data = f.read(4096)
            if not f_data:
                break
            SHA256.update(f_data)
        if file_extension == True:
            extension = os.path.splitext(file_path)[1]
            SHA256.update(extension.encode())
        return SHA256.hexdigest()


def get_text_SHA256(*string: bytes) -> str:
    """
    Get SHA256 hash from text

    :param string: Input bytes string

    :raise AttributeError: if input byte string is empty
    :rtype: string
    """
    SHA256 = hashlib.sha256()

    if len(string) == 0:
        raise AttributeError("Attribute is empty.")

    for data in string:
        if type(data) != bytes:
            raise TypeError("Attribute should be bytes.")

        SHA256.update(data)
    return SHA256.hexdigest()


def get_inside(inp_str: str, init_str: str, end_str: str) -> str:
    """
    This function extracts text content between two specified string within a larger input string.
    :param inp_str: The input string from which the content to  extracted.
    :param init_str: The starting string that marks the beginning of the content to extract.
    :param end_str: The end string that marks the end of the content to extract.

    :rtype : string or int
    """
    if match := re.search(
        r"" + re.escape(init_str) + "(.*?)" + re.escape(end_str), inp_str, re.DOTALL
    ):
        return match.group(1)
    else:
        return -1
