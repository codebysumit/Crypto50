import os
import argparse
import pathlib
from hybrid_crypto import genarate_keys, encryption, decryption


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--generate_keys",
        "-GENKEYS",
        help="Generate public and private key file.",
    )
    parser.add_argument("--encryption_file", "-ENCFILE", help="Encription file.")
    parser.add_argument("--encryption_text", "-ENCTEXT", help="Encription text.")
    parser.add_argument(
        "--encryption_folder", "-ENCFOLDER", help="Encription files from folder."
    )
    parser.add_argument("--decryption_file", "-DECFILE", help="Decription file.")
    parser.add_argument("--decryption_folder", "-DECFOLDER", help="Decription file.")
    parser.add_argument("--output_dir", "-ODIR", help="Output directory path.")
    parser.add_argument("--output", "-O", help="Output file path.")
    parser.add_argument("--pub_key", "-PUB", help="Public key file path.")
    parser.add_argument("--priv_key", "-PRIV", help="Private key file path.")

    argument = parser.parse_args()

    # Generate new RSA keys set
    if argument.generate_keys is not None:
        if (
            (argument.encryption_file != None)
            or (argument.encryption_text != None)
            or (argument.encryption_folder != None)
            or (argument.decryption_file != None)
            or (argument.decryption_folder != None)
            or (argument.output != None)
            or (argument.output_dir != None)
            or (argument.pub_key != None)
            or (argument.priv_key != None)
        ):
            parser.error("You give one or mode invalide argument.")

        keys_dir = generate_new_keys(argument.generate_keys)
        if keys_dir[0]:
            print("Keys successfully save to:", keys_dir[1])
        else:
            parser.error(keys_dir[1])

    # Encription text
    elif argument.encryption_text is not None:
        if (
            (argument.encryption_file != None)
            or (argument.generate_keys != None)
            or (argument.encryption_folder != None)
            or (argument.decryption_file != None)
            or (argument.decryption_folder != None)
            or (argument.output_dir != None)
        ):
            parser.error("You give one or more invalide argument.")

        if argument.output == None:
            parser.error("You do not give [--output]")
        elif argument.pub_key == None:
            parser.error("You do not give [--pub_key]")
        elif argument.priv_key == None:
            parser.error("You do not give [--priv_key]")

        enc_file = encryption_text(
            argument.encryption_text,
            argument.output,
            argument.pub_key,
            argument.priv_key,
        )
        if enc_file[0]:
            print("Encription text successfully save to:", enc_file[1])
        else:
            parser.error(enc_file[1])

    # Encription file
    elif argument.encryption_file is not None:
        if (
            (argument.generate_keys != None)
            or (argument.encryption_text != None)
            or (argument.encryption_folder != None)
            or (argument.decryption_file != None)
            or (argument.decryption_folder != None)
            or (argument.output_dir != None)
        ):
            parser.error("You give one or more invalide argument.")

        if argument.output == None:
            parser.error("You do not give [--output]")
        elif argument.pub_key == None:
            parser.error("You do not give [--pub_key]")
        elif argument.priv_key == None:
            parser.error("You do not give [--priv_key]")

        enc_file = encryption_file(
            argument.encryption_file,
            argument.output,
            argument.pub_key,
            argument.priv_key,
        )
        if enc_file[0]:
            print("Encription file successfully save to:", enc_file[1])
        else:
            parser.error(enc_file[1])

    # Encription files from folder
    elif argument.encryption_folder is not None:
        if (
            (argument.generate_keys != None)
            or (argument.encryption_file != None)
            or (argument.encryption_text != None)
            or (argument.decryption_file != None)
            or (argument.decryption_folder != None)
            or (argument.output != None)
        ):
            parser.error("You give one or more invalide argument.")

        if argument.output_dir == None:
            parser.error("You do not give [--output_dir]")
        elif argument.pub_key == None:
            parser.error("You do not give [--pub_key]")
        elif argument.priv_key == None:
            parser.error("You do not give [--priv_key]")

        enc_file_from_folder = encryption_folder(
            argument.encryption_folder,
            argument.output_dir,
            argument.pub_key,
            argument.priv_key,
        )
        if enc_file_from_folder[0]:
            print("Successfully encripted", enc_file_from_folder[1], "files.")
        else:
            parser.error(enc_file_from_folder[1])

    # Decryption File
    elif argument.decryption_file is not None:
        if (
            (argument.generate_keys != None)
            or (argument.encryption_file != None)
            or (argument.encryption_text != None)
            or (argument.encryption_folder != None)
            or (argument.decryption_folder != None)
            or (argument.output != None)
        ):
            parser.error("You give one or more invalide argument.")

        if argument.output_dir == None:
            parser.error("You do not give [--output_dir]")
        elif argument.pub_key == None:
            parser.error("You do not give [--pub_key]")
        elif argument.priv_key == None:
            parser.error("You do not give [--priv_key]")

        dec_file = decryption_file(
            argument.decryption_file,
            argument.output_dir,
            argument.priv_key,
            argument.pub_key,
        )
        if dec_file[0]:
            print("Decription file successfully save to:", dec_file[1])
        else:
            parser.error(dec_file[1])

    # Decryption files from folder
    elif argument.decryption_folder is not None:
        if (
            (argument.generate_keys != None)
            or (argument.encryption_file != None)
            or (argument.encryption_text != None)
            or (argument.encryption_folder != None)
            or (argument.decryption_file != None)
            or (argument.output != None)
        ):
            parser.error("You give one or more invalide argument.")

        if argument.output_dir == None:
            parser.error("You do not give [--output_dir]")
        elif argument.pub_key == None:
            parser.error("You do not give [--pub_key]")
        elif argument.priv_key == None:
            parser.error("You do not give [--priv_key]")

        dec_files_from_folder = decryption_folder(
            argument.decryption_folder,
            argument.output_dir,
            argument.priv_key,
            argument.pub_key,
        )
        if dec_files_from_folder[0]:
            print("Successfully decripted", dec_files_from_folder[1], "files.")
        else:
            parser.error(dec_files_from_folder[1])
    else:
        parser.error(
            "Missing any argument following this list : [--generate_keys] [--encryption_file] [--encryption_text] [--encryption_folder] [--decryption_file] [--decryption_folder]"
        )


# Generate new keys
def generate_new_keys(output_dir_path: str) -> tuple[bool, str]:
    # Validation Argument
    output_dir_path = pathlib.Path(output_dir_path)
    if (not output_dir_path.exists()) or (not output_dir_path.is_dir()):
        return (False, "Output folder not found.")
    try:
        key_dir_name = genarate_keys.genarate_RSA_key(output_dir_path)
    except genarate_keys.FileNotCreateError:
        return (False, "Keys file not Create")

    return (True, str(output_dir_path.joinpath(key_dir_name)))


# Encryption Fie
def encryption_file(
    input_file_path: str,
    output_file_path: str,
    res_pub_key_file_path: str,
    sen_priv_key_file_path: str,
) -> tuple[bool, str]:

    # Validation Argument
    if (not pathlib.Path(input_file_path).exists()) or (
        not pathlib.Path(input_file_path).is_file()
    ):
        return (False, "Input file not found.")

    if (
        (not pathlib.Path(os.path.split(output_file_path)[0]).exists())
        or (os.path.split(output_file_path)[1] == "")
        or (
            os.path.split(output_file_path)[0] == ""
            and os.path.split(output_file_path)[1] != ""
            and pathlib.Path(os.path.split(output_file_path)[1]).is_dir()
        )
    ):
        return (False, "Output file not found.")

    if (not pathlib.Path(res_pub_key_file_path).exists()) or (
        pathlib.Path(res_pub_key_file_path).suffix.lower() != ".pem"
    ):
        return (False, "Public key file not found.")

    if (not pathlib.Path(sen_priv_key_file_path).exists()) or (
        pathlib.Path(sen_priv_key_file_path).suffix.lower() != ".pem"
    ):
        return (False, "Private key file not found.")

    return (
        True,
        encryption.file_encryption(
            input_file_path,
            output_file_path,
            res_pub_key_file_path,
            sen_priv_key_file_path,
        ),
    )


# Encryption Folder
def encryption_folder(
    input_dir_path: str,
    output_dir_path: str,
    res_pub_key_file_path: str,
    sen_priv_key_file_path: str,
) -> tuple[bool, str]:

    # Validation Argument
    if (not pathlib.Path(input_dir_path).exists()) or (
        not pathlib.Path(input_dir_path).is_dir()
    ):
        return (False, "Input folder not found.")

    if (not pathlib.Path(output_dir_path).exists()) or (
        not pathlib.Path(output_dir_path).is_dir()
    ):
        return (False, "Output folder not found.")

    if (not pathlib.Path(res_pub_key_file_path).exists()) or (
        pathlib.Path(res_pub_key_file_path).suffix.lower() != ".pem"
    ):
        return (False, "Public key file not found.")

    if (not pathlib.Path(sen_priv_key_file_path).exists()) or (
        pathlib.Path(sen_priv_key_file_path).suffix.lower() != ".pem"
    ):
        return (False, "Private key file not found.")

    all_files_and_dir_path = list(pathlib.Path(input_dir_path).rglob("*"))

    all_files_path = list()
    for p in all_files_and_dir_path:
        if not pathlib.Path(p).is_dir():
            all_files_path.append(p)


    count = 1
    for file in all_files_path:
        try:
            enc_file = encryption.file_encryption(
                input_file_path=file,
                output_file_path=pathlib.Path(output_dir_path).joinpath(
                    f"ENCRYPTION_{count}.enc"
                ),
                pub_key_file_path=res_pub_key_file_path,
                priv_key_file_path=sen_priv_key_file_path,
            )
            print(
                f'[{count}/{len(all_files_path)}] : Successfully encripted "{pathlib.Path(file)}" ==> "{enc_file}"'
            )
        except PermissionError:
            print(
                f'[{count}/{len(all_files_path)}] : File not encripted "{pathlib.Path(file)}" ==> Permission denied'
            )
        count += 1
    return (True, f"{count-1}")


# Encryption text
def encryption_text(
    plain_texts: str,
    output_file_path: str,
    res_pub_key_file_path: str,
    sen_priv_key_file_path: str,
) -> tuple[bool, str]:

    # Argument Validation
    if (
        (not pathlib.Path(os.path.split(output_file_path)[0]).exists())
        or (os.path.split(output_file_path)[1] == "")
        or (
            os.path.split(output_file_path)[0] == ""
            and os.path.split(output_file_path)[1] != ""
            and pathlib.Path(os.path.split(output_file_path)[1]).is_dir()
        )
    ):
        return (False, "Output file not exist.")

    if (not pathlib.Path(res_pub_key_file_path).exists()) or (
        pathlib.Path(res_pub_key_file_path).suffix.lower() != ".pem"
    ):
        return (False, "Public key file not exist.")

    if (not pathlib.Path(sen_priv_key_file_path).exists()) or (
        pathlib.Path(sen_priv_key_file_path).suffix.lower() != ".pem"
    ):
        return (False, "Private key file not exist.")

    return (
        True,
        encryption.text_encryption(
            plain_texts,
            output_file_path,
            res_pub_key_file_path,
            sen_priv_key_file_path,
        ),
    )


# Decription File
def decryption_file(
    enc_file_path: str,
    output_dir_path: str,
    res_pri_key_file_path: str,
    sen_pub_key_file_path: str,
) -> tuple[bool, str]:

    # Argument Validation
    if (not pathlib.Path(enc_file_path).exists()) or (
        not pathlib.Path(enc_file_path).is_file()
    ):
        return (False, "Encryption file not found.")

    if (not pathlib.Path(output_dir_path).exists()) or (
        not pathlib.Path(output_dir_path).is_dir()
    ):
        return (False, "Output folder not found")

    if (not pathlib.Path(res_pri_key_file_path).exists()) or (
        pathlib.Path(res_pri_key_file_path).suffix.lower() != ".pem"
    ):
        return (False, "Reciver private key file not found.")

    if (not pathlib.Path(sen_pub_key_file_path).exists()) or (
        pathlib.Path(sen_pub_key_file_path).suffix.lower() != ".pem"
    ):
        return (False, "Sender public key file not found.")

    try:
        dec_file_path = decryption.file_decryption(
            enc_file_path, output_dir_path, res_pri_key_file_path, sen_pub_key_file_path
        )
        return (True, dec_file_path)

    except decryption.EncryptionDataNotFoundError:
        return (False, "This is not valide encryption file.")

    except decryption.InvalidTokenError:
        return (False, "Encrypted token is not valid.")

    except decryption.SignatureVerificationError:
        return (False, "File signature is not valid.")

    except decryption.KeyNotDecryptedError:
        return (False, "Encription file not decrypt.")


# Dencription Folder
def decryption_folder(
    enc_folder_path: str,
    output_dir_path: str,
    res_pri_key_file_path: str,
    sen_pub_key_file_path: str,
) -> tuple[bool, str]:
    if not pathlib.Path(enc_folder_path).exists() or (
        not pathlib.Path(enc_folder_path).is_dir()
    ):
        return (False, "Encryption folder not found.")
    
    if not pathlib.Path(output_dir_path).exists() or (
        not pathlib.Path(output_dir_path).is_dir()
    ):
        return (False, "Output folder not found.")

    if (not pathlib.Path(res_pri_key_file_path).exists()) or (
        pathlib.Path(res_pri_key_file_path).suffix.lower() != ".pem"
    ):
        return (False, "Reciver private key file not found.")

    if (not pathlib.Path(sen_pub_key_file_path).exists()) or (
        pathlib.Path(sen_pub_key_file_path).suffix.lower() != ".pem"
    ):
        return (False, "Sender public key file not found.")

    all_files_path = list(pathlib.Path(enc_folder_path).rglob("*.enc"))

    count = 1
    dec_file_count = 1
    for file in all_files_path:
        try:
            dec_file_path = decryption.file_decryption(
                encrypt_file_path=file,
                output_folder_path=output_dir_path,
                priv_key_file_path=res_pri_key_file_path,
                pub_key_file_path=sen_pub_key_file_path,
            )
            print(
                f'[{count}/{len(all_files_path)}] : Successfully decripted "{pathlib.Path(file)}" ==> "{dec_file_path}"'
            )
            dec_file_count += 1

        except decryption.EncryptionDataNotFoundError:
            print(
                f'[{count}/{len(all_files_path)}] : File not decripted "{pathlib.Path(file).name}" ==> Encription data not valid.'
            )

        except decryption.InvalidTokenError:
            print(
                f'[{count}/{len(all_files_path)}] : File not decripted "{pathlib.Path(file).name}" ==> Invalid token not valid.'
            )

        except decryption.SignatureVerificationError:
            print(
                f'[{count}/{len(all_files_path)}] : File not decripted "{pathlib.Path(file).name}" ==> Signature not valid.'
            )

        except decryption.KeyNotDecryptedError:
            print(
                f'[{count}/{len(all_files_path)}] : File not decripted "{pathlib.Path(file).name}" ==>  Data not decripted.'
            )

        count += 1

    return (True, f"{dec_file_count-1}")


if __name__ == "__main__":
    main()
