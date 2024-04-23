import os
import rsa
import pathlib
from base64 import b64encode
from cryptography.fernet import Fernet
from hybrid_crypto.addon import get_SHA256, get_text_SHA256


class FileNotCreateError(Exception):
    """Exception raise for file not create errors."""


# File encryption (hybrid_encription)
def file_encryption(
    input_file_path: str | bytes | pathlib.Path | os.PathLike,
    output_file_path: str | bytes | pathlib.Path | os.PathLike,
    pub_key_file_path: str | bytes | pathlib.Path | os.PathLike,
    priv_key_file_path: str | bytes | pathlib.Path | os.PathLike,
) -> str | os.PathLike:
    """
    Encryption file using hybrid cryptography and return encrypt file path

    :param input_file_path: Input file path
    :param output_file_path: Output or Encrypt file name with location
    :param pub_key_file_path: Reciver public key file path
    :param priv_key_file_path: Sender private key file path

    :type input_file_path: str|bytes|pathlib.Path
    :type output_file_path: str|bytes|pathlib.Path
    :type pub_key_file_path: str|bytes|pathlib.Path
    :type priv_key_file_path: str|bytes|pathlib.Path

    :raise TypeError: If input_file_path, output_file_path pub_key_file_path and priv_key_file_path is not valid os path
    :raise FileNotFoundError: If input_file_path, pub_key_file_path and priv_key_file_path is not found
    :raise FileNotCreateError: If encrypted file not create
    :raise FileNotFoundError: If no such encrypted file path directory

    :rtype: str
    """

    # Get public key
    try:
        with open(pathlib.Path(pub_key_file_path), "rb") as public_file:
            public_key = rsa.PublicKey.load_pkcs1(public_file.read())
    except TypeError:
        raise TypeError("Public Key path expected str, bytes or os.PathLike object.")
    except FileNotFoundError:
        raise FileNotFoundError("Public Key not found.")

    # Get private key
    try:
        with open(pathlib.Path(priv_key_file_path), "rb") as private_file:
            private_key = rsa.PrivateKey.load_pkcs1(private_file.read())
    except TypeError:
        raise TypeError("Private Key path expected str, bytes or os.PathLike object.")
    except FileNotFoundError:
        raise FileNotFoundError("Private Key not found.")

    # Get input file data
    try:
        with open(pathlib.Path(input_file_path), "rb") as input_file:
            file_data = input_file.read()
    except TypeError:
        raise TypeError("Input file path expected str, bytes or os.PathLike object.")
    except FileNotFoundError:
        raise FileNotFoundError("Input file not found.")

    # Get symmetric key
    symmetric_key = Fernet.generate_key()

    # Encrypt file data and file extension using AES
    f = Fernet(symmetric_key)
    encrypt_data = f.encrypt(file_data)
    encrypt_file_extension = f.encrypt(
        os.path.splitext(input_file_path)[1].encode("utf-8")
    )

    # Encrypt symmetric key using RSA
    encrypt_symmetric_key = rsa.encrypt(symmetric_key, public_key)

    # Get file hash and signatus file hash
    file_hash = get_SHA256(file_path=input_file_path, file_extension=True)
    signature = rsa.sign(file_hash.encode("utf-8"), private_key, "SHA-256")

    try:
        with open(pathlib.Path(output_file_path), "wb") as output_file:
            output_file.write("-----BEGIN ENCRYPT DATA-----\n".encode("utf-8"))
            output_file.write(encrypt_data)
            # output_file.write(b64encode(encrypt_data))
            output_file.write("\n-----END ENCRYPT DATA-----\n".encode("utf-8"))

            output_file.write("\n-----BEGIN FILE EXTENSION-----\n".encode("utf-8"))
            output_file.write(encrypt_file_extension)
            # output_file.write(b64encode(encrypt_file_extension))
            output_file.write("\n-----END FILE EXTENSION-----\n".encode("utf-8"))

            output_file.write("\n-----BEGIN SYMMETRIC KEY-----\n".encode("utf-8"))
            output_file.write(b64encode(encrypt_symmetric_key))
            output_file.write("\n-----END SYMMETRIC KEY-----\n".encode("utf-8"))

            output_file.write("\n-----BEGIN SIGNATURE-----\n".encode("utf-8"))
            output_file.write(b64encode(signature))
            output_file.write("\n-----END SIGNATURE-----".encode("utf-8"))
    except TypeError:
        raise TypeError("Output file path expected str, bytes or os.PathLike object.")
    except FileNotFoundError:
        raise FileNotFoundError("No such output directory.")
    except OSError:
        raise FileNotCreateError("Encryption file not create.")

    return output_file_path


def text_encryption(
    input_str: str,
    output_file_path: str | bytes | pathlib.Path | os.PathLike,
    pub_key_file_path: str | bytes | pathlib.Path | os.PathLike,
    priv_key_file_path: str | bytes | pathlib.Path | os.PathLike,
) -> str | os.PathLike:
    """
    Encryption text using hybrid cryptography and return encrypt file path

    :param input_str: Input texts as a string
    :param output_file_path: Output or Encrypted file name with location
    :param pub_key_file_path: Reciver public key file path
    :param priv_key_file_path: Sender private key file path

    :type input_str: str
    :type output_file_path: str|bytes|pathlib.Path
    :type pub_key_file_path: str|bytes|pathlib.Path
    :type priv_key_file_path: str|bytes|pathlib.Path

    :raise TypeError: If output_file_path, pub_key_file_path and priv_key_file_path is not valid os path
    :raise FileNotFoundError: If  pub_key_file_path and priv_key_file_path is not found
    :raise FileNotCreateError: If encrypted file not create
    :raise FileNotFoundError: If no such encrypted file path directory

    :rtype: str
    """

    # Get public key
    try:
        with open(pathlib.Path(pub_key_file_path), "rb") as public_file:
            public_key = rsa.PublicKey.load_pkcs1(public_file.read())
    except TypeError:
        raise TypeError("Public key path expected str, bytes or os.PathLike object.")
    except FileNotFoundError:
        raise FileNotFoundError("Public Key not found.")

    # Get private key
    try:
        with open(pathlib.Path(priv_key_file_path), "rb") as private_file:
            private_key = rsa.PrivateKey.load_pkcs1(private_file.read())
    except TypeError:
        raise TypeError("Private key path expected str, bytes or os.PathLike object.")
    except FileNotFoundError:
        raise FileNotFoundError("Private Key not found.")

    # Get symmetric key
    symmetric_key = Fernet.generate_key()

    # Get input file data
    if input_str != None:
        # Encrypt file data and file extension using AES
        f = Fernet(symmetric_key)
        encrypt_data = f.encrypt(str(input_str).encode("utf-8"))
        encrypt_file_extension = f.encrypt(".text".encode("utf-8"))

    # Encrypt symmetric key using RSA
    encrypt_symmetric_key = rsa.encrypt(symmetric_key, public_key)

    # Get text hash and signatus file hash
    signature = rsa.sign(
        get_text_SHA256(input_str.encode("utf-8"), ".text".encode("utf-8")).encode(
            "utf-8"
        ),
        private_key,
        "SHA-256",
    )

    try:
        with open(pathlib.Path(output_file_path), "wb") as output_file:
            output_file.write("-----BEGIN ENCRYPT DATA-----\n".encode("utf-8"))
            output_file.write(encrypt_data)
            output_file.write("\n-----END ENCRYPT DATA-----\n".encode("utf-8"))

            output_file.write("\n-----BEGIN FILE EXTENSION-----\n".encode("utf-8"))
            output_file.write(encrypt_file_extension)
            output_file.write("\n-----END FILE EXTENSION-----\n".encode("utf-8"))

            output_file.write("\n-----BEGIN SYMMETRIC KEY-----\n".encode("utf-8"))
            output_file.write(b64encode(encrypt_symmetric_key))
            output_file.write("\n-----END SYMMETRIC KEY-----\n".encode("utf-8"))

            output_file.write("\n-----BEGIN SIGNATURE-----\n".encode("utf-8"))
            output_file.write(b64encode(signature))
            output_file.write("\n-----END SIGNATURE-----".encode("utf-8"))
    except TypeError:
        raise TypeError("Output file path expected str, bytes or os.PathLike object.")
    except FileNotFoundError:
        raise FileNotFoundError("No such output directory.")
    except OSError:
        raise FileNotCreateError("Encryption file not create.")

    return output_file_path
