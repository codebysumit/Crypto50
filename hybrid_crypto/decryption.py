import os
import rsa
import pathlib
from base64 import b64decode
from datetime import datetime
from cryptography.fernet import Fernet
from hybrid_crypto.addon import get_inside, get_text_SHA256
from cryptography.fernet import InvalidToken
from rsa.pkcs1 import VerificationError, DecryptionError


class EncryptionDataNotFoundError(Exception):
    """Encription File Data Stucture Not Match Error"""


class InvalidTokenError(Exception):
    """Invalid Token Error"""


class SignatureVerificationError(Exception):
    """Signature Validation Error"""


class KeyNotDecryptedError(Exception):
    """Key Not Error Decripted"""


class FileNotCreateError(Exception):
    """Exception raise for file not create errors."""


def file_decryption(
    encrypt_file_path: str | bytes | pathlib.Path | os.PathLike,
    output_folder_path: str | bytes | pathlib.Path | os.PathLike,
    priv_key_file_path: str | bytes | pathlib.Path | os.PathLike,
    pub_key_file_path: str | bytes | pathlib.Path | os.PathLike,
) -> str | os.PathLike:
    """
    Decryption file using hybrid cryptography and return decrypt file path

    :param encrypt_file_path: Encrypted file path
    :param output_folder_path: Output or Encrypted file name with location
    :param priv_key_file_path: Reciver private key file path
    :param pub_key_file_path: Sender public key file path

    :type encrypt_file_path: str|bytes|pathlib.Path
    :type output_folder_path: str|bytes|pathlib.Path
    :type pub_key_file_path: str|bytes|pathlib.Path
    :type priv_key_file_path: str|bytes|pathlib.Path

    :raise TypeError: If encrypt_file_path, output_folder_path, pub_key_file_path and priv_key_file_path is not valid os path
    :raise FileNotFoundError: If encrypt_file_path, output_folder_path pub_key_file_path and priv_key_file_path is not found
    :raise FileNotCreateError: If output file not create

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

    # Get encrypted file data
    try:
        with open(pathlib.Path(encrypt_file_path), "r") as input_file:
            encrypt_file_data = input_file.read()
    except TypeError:
        raise TypeError(
            "Encryption file path expected str, bytes or os.PathLike object."
        )
    except FileNotFoundError:
        raise FileNotFoundError("Encryption file not found.")

    # Get encrypted data
    enc_data = get_inside(
        encrypt_file_data,
        "-----BEGIN ENCRYPT DATA-----\n",
        "\n-----END ENCRYPT DATA-----",
    )

    if enc_data == -1:
        raise EncryptionDataNotFoundError("Encryption data not found in encript filre.")

    # Get encripted file extention
    enc_file_ext = get_inside(
        encrypt_file_data,
        "-----BEGIN FILE EXTENSION-----\n",
        "\n-----END FILE EXTENSION-----",
    )

    if enc_file_ext == -1:
        raise EncryptionDataNotFoundError(
            "Encryption file extension not found in encript filre."
        )

    # Get encrypted key
    enc_key = get_inside(
        encrypt_file_data,
        "-----BEGIN SYMMETRIC KEY-----\n",
        "\n-----END SYMMETRIC KEY-----",
    )

    if enc_key == -1:
        raise EncryptionDataNotFoundError("Encryption key not found in encript filre.")

    # Get signature
    signature = get_inside(
        encrypt_file_data,
        "-----BEGIN SIGNATURE-----\n",
        "\n-----END SIGNATURE-----",
    )

    if signature == -1:
        raise EncryptionDataNotFoundError(
            "Encryption signature not found in encript filre."
        )

    try:
        # Decripted ASE key
        de_key = rsa.decrypt(b64decode(enc_key), private_key)

        f = Fernet(de_key)
        # Decripted data
        de_data = f.decrypt(enc_data)
        # Decripted extention
        de_file_ext = f.decrypt(enc_file_ext)

        # Get hash from decrypted data
        hash = get_text_SHA256(de_data, de_file_ext)

        # Signature varify
        signature_validation = rsa.verify(
            hash.encode("utf-8"), b64decode(signature), public_key
        )
        if signature_validation == "SHA-256":
            file_name = (
                "DECRYPT_"
                + datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                + de_file_ext.decode("utf-8")
            )
            with open(
                pathlib.Path(output_folder_path).joinpath(file_name), "wb"
            ) as output_file:
                output_file.write(de_data)

    except InvalidToken:
        raise InvalidTokenError("Token is not valide.")
    except VerificationError:
        raise SignatureVerificationError("Signature not match.")
    except DecryptionError:
        raise KeyNotDecryptedError("Private key not decrypt.")
    except TypeError:
        raise TypeError("Output file path expected str, bytes or os.PathLike object.")

    except FileNotFoundError:
        raise FileNotFoundError("No such output directory.")
    except OSError:
        raise FileNotCreateError("File not decrypted.")

    return pathlib.Path(output_folder_path).joinpath(file_name).as_posix()
