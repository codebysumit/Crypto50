import rsa
import pathlib
from datetime import datetime


class FileNotCreateError(Exception):
    """Exception raise for file not create errors."""


def genarate_RSA_key(output_dir_path: str | bytes | pathlib.Path) -> str:
    """
    Genarates RAS public key and private key and return directory name

    :param output_dir_path: Keys file save directory path location
    :type output_dir_path: str|bytes|pathlib.Path

    :raise FileNotCreateError: If key file not create
    :rtype: str
    """

    public_key, private_key = rsa.newkeys(2048)

    dir_name = "KEYS_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    try:
        dir_path = pathlib.Path(output_dir_path).joinpath(dir_name)
        dir_path.mkdir(parents=True, exist_ok=True)
        # Save public key
        with open(dir_path.joinpath("public.pem"), "wb") as public_file:
            public_file.write(public_key.save_pkcs1())

        # Save private key
        with open(dir_path.joinpath("private.pem"), "wb") as private_file:
            private_file.write(private_key.save_pkcs1())
    except TypeError:
        raise TypeError("Output folder path expected str, bytes or os.PathLike object.")
    except OSError:
        raise FileNotCreateError("File Not Create.")

    return dir_name
