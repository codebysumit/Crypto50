import pytest
import pathlib
from hybrid_crypto import genarate_keys, encryption, decryption
from hybrid_crypto import addon

TESTING_DIR = "__testfiles__/testing_module/"

TEST_FILES = {
    "txt": "__testfiles__/inputs/massages.txt",
    "audio": "__testfiles__/inputs/house-chords-12112.mp3",
    "image": "__testfiles__/inputs/cat-551554_1280.jpg",
    "vedio": "__testfiles__/inputs/145308_(1080p).mp4",
}

TEST_SENDER_KEYS_DIR = "__testfiles__/keys/KEYS_20240305_110825_858294"
TEST_RECIVER_KEYS_DIR = "__testfiles__/keys/KEYS_20240305_110840_641535"


def test_genarate_keys():
    if not pathlib.Path(TESTING_DIR).exists():
        pathlib.Path(TESTING_DIR).mkdir(exist_ok=True)

    # Testing genarate keys
    key_dir_name = genarate_keys.genarate_RSA_key(
        pathlib.Path(TESTING_DIR).joinpath("genarate_keys")
    )
    keys_dir_path = pathlib.Path(TESTING_DIR).joinpath("genarate_keys", key_dir_name)

    assert keys_dir_path.exists() == True
    assert keys_dir_path.joinpath("private.pem").exists() == True
    assert keys_dir_path.joinpath("public.pem").exists() == True

    # Testing Exception Validation
    with pytest.raises(TypeError):
        genarate_keys.genarate_RSA_key()

    with pytest.raises(TypeError):
        genarate_keys.genarate_RSA_key(1234)


def test_encryption_file():
    if not pathlib.Path(TESTING_DIR).exists():
        pathlib.Path(TESTING_DIR).mkdir(exist_ok=True)

    enc_test_path = pathlib.Path(TESTING_DIR).joinpath("encryption")

    if not enc_test_path.exists():
        enc_test_path.mkdir(exist_ok=True)

    # Testing encryption file
    enc_file_path = encryption.file_encryption(
        pathlib.Path(TEST_FILES["txt"]),
        enc_test_path.joinpath("encryption_file.enc"),
        pathlib.Path(TEST_RECIVER_KEYS_DIR).joinpath("public.pem"),
        pathlib.Path(TEST_SENDER_KEYS_DIR).joinpath("private.pem"),
    )

    assert pathlib.Path(enc_file_path).exists() == True

    # Testing Exception Validation
    with pytest.raises(FileNotFoundError):
        encryption.file_encryption(
            "filenotfound.txt",
            enc_test_path.joinpath("encryption_file.enc"),
            pathlib.Path(TEST_RECIVER_KEYS_DIR).joinpath("public.pem"),
            pathlib.Path(TEST_SENDER_KEYS_DIR).joinpath("private.pem"),
        )

    with pytest.raises(FileNotFoundError):
        encryption.file_encryption(
            pathlib.Path(TEST_FILES["txt"]),
            enc_test_path.joinpath("dir_not_exist/encryption_file.enc"),
            pathlib.Path(TEST_RECIVER_KEYS_DIR).joinpath("public.pem"),
            pathlib.Path(TEST_SENDER_KEYS_DIR).joinpath("private.pem"),
        )

    with pytest.raises(FileNotFoundError):
        encryption.file_encryption(
            pathlib.Path(TEST_FILES["txt"]),
            enc_test_path.joinpath("encryption_file.enc"),
            pathlib.Path(TEST_RECIVER_KEYS_DIR).joinpath("publickeyfilenotfound.pem"),
            pathlib.Path(TEST_SENDER_KEYS_DIR).joinpath("private.pem"),
        )

    with pytest.raises(FileNotFoundError):
        encryption.file_encryption(
            pathlib.Path(TEST_FILES["txt"]),
            enc_test_path.joinpath("encryption_file.enc"),
            pathlib.Path(TEST_RECIVER_KEYS_DIR).joinpath("public.pem"),
            pathlib.Path(TEST_SENDER_KEYS_DIR).joinpath("privatekeyfilenotfound.pem"),
        )


def test_encryption_text():
    if not pathlib.Path(TESTING_DIR).exists():
        pathlib.Path(TESTING_DIR).mkdir(exist_ok=True)

    enc_test_path = pathlib.Path(TESTING_DIR).joinpath("encryption")

    # Testing encryption text
    if not enc_test_path.exists():
        enc_test_path.mkdir(exist_ok=True)

    enc_text_file_path = encryption.text_encryption(
        "Maow maow mmmaaaoowwwww",
        pathlib.Path(enc_test_path).joinpath("encryption_text.enc"),
        pathlib.Path(TEST_RECIVER_KEYS_DIR).joinpath("public.pem"),
        pathlib.Path(TEST_SENDER_KEYS_DIR).joinpath("private.pem"),
    )

    assert pathlib.Path(enc_text_file_path).exists() == True

    # Testing exception validation
    with pytest.raises(FileNotFoundError):
        encryption.text_encryption(
            "Maow maow mmmaaaoowwwww",
            pathlib.Path(enc_test_path).joinpath(
                "dir_not_exist", "encryption_text.enc"
            ),
            pathlib.Path(TEST_RECIVER_KEYS_DIR).joinpath("public.pem"),
            pathlib.Path(TEST_SENDER_KEYS_DIR).joinpath("private.pem"),
        )

    with pytest.raises(FileNotFoundError):
        encryption.text_encryption(
            "Maow maow mmmaaaoowwwww",
            pathlib.Path(enc_test_path).joinpath("encryption_text.enc"),
            pathlib.Path(TEST_RECIVER_KEYS_DIR).joinpath("public_not_found.pem"),
            pathlib.Path(TEST_SENDER_KEYS_DIR).joinpath("private.pem"),
        )

    with pytest.raises(FileNotFoundError):
        encryption.text_encryption(
            "Maow maow mmmaaaoowwwww",
            pathlib.Path(enc_test_path).joinpath("encryption_text.enc"),
            pathlib.Path(TEST_RECIVER_KEYS_DIR).joinpath("public.pem"),
            pathlib.Path(TEST_SENDER_KEYS_DIR).joinpath("private_not_found.pem"),
        )


def test_decryption_file():
    if not pathlib.Path(TESTING_DIR).exists():
        pathlib.Path(TESTING_DIR).mkdir(exist_ok=True)

    dec_test_path = pathlib.Path(TESTING_DIR).joinpath("decryption")

    if not dec_test_path.exists():
        dec_test_path.mkdir(exist_ok=True)

    # decrypt text
    enc_text_file_path = encryption.text_encryption(
        "Maow maow mmmaaaoowwwww",
        pathlib.Path(dec_test_path).joinpath("encryption.enc"),
        pathlib.Path(TEST_RECIVER_KEYS_DIR).joinpath("public.pem"),
        pathlib.Path(TEST_SENDER_KEYS_DIR).joinpath("private.pem"),
    )

    dec_text_file_path = decryption.file_decryption(
        pathlib.Path(enc_text_file_path),
        dec_test_path,
        pathlib.Path(TEST_RECIVER_KEYS_DIR).joinpath("private.pem"),
        pathlib.Path(TEST_SENDER_KEYS_DIR).joinpath("public.pem"),
    )

    assert pathlib.Path(dec_text_file_path).exists() == True

    with open(dec_text_file_path, "r") as dec_text_file:
        text_data = dec_text_file.read()

    assert addon.get_text_SHA256(
        "Maow maow mmmaaaoowwwww".encode("utf-8")
    ) == addon.get_text_SHA256(text_data.encode("utf-8"))

    # Decrept file
    enc_file_path = encryption.file_encryption(
        pathlib.Path(TEST_FILES["image"]),
        pathlib.Path(dec_test_path).joinpath("encryption_file.enc"),
        pathlib.Path(TEST_RECIVER_KEYS_DIR).joinpath("public.pem"),
        pathlib.Path(TEST_SENDER_KEYS_DIR).joinpath("private.pem"),
    )

    dec_file_path = decryption.file_decryption(
        pathlib.Path(enc_file_path),
        dec_test_path,
        pathlib.Path(TEST_RECIVER_KEYS_DIR).joinpath("private.pem"),
        pathlib.Path(TEST_SENDER_KEYS_DIR).joinpath("public.pem"),
    )

    assert pathlib.Path(enc_file_path).exists() == True
    assert addon.get_SHA256(
        pathlib.Path(TEST_FILES["image"]), True
    ) == addon.get_SHA256(pathlib.Path(dec_file_path), True)

    # Exception Validation
    with pytest.raises(
        decryption.KeyNotDecryptedError,
    ):
        enc_text_file_wrong_key_path = encryption.text_encryption(
            "Maow maow mmmaaaoowwwww",
            pathlib.Path(dec_test_path).joinpath("encryption_wrong_key.enc"),
            pathlib.Path(TEST_SENDER_KEYS_DIR).joinpath("public.pem"),
            pathlib.Path(TEST_RECIVER_KEYS_DIR).joinpath("private.pem"),
        )

        decryption.file_decryption(
            pathlib.Path(enc_text_file_wrong_key_path),
            dec_test_path,
            pathlib.Path(TEST_RECIVER_KEYS_DIR).joinpath("private.pem"),
            pathlib.Path(TEST_SENDER_KEYS_DIR).joinpath("public.pem"),
        )

    with pytest.raises(FileNotFoundError):
        decryption.file_decryption(
            "not_valid_path.enc",
            dec_test_path,
            pathlib.Path(TEST_RECIVER_KEYS_DIR).joinpath("private.pem"),
            pathlib.Path(TEST_SENDER_KEYS_DIR).joinpath("public.pem"),
        )

    with pytest.raises(FileNotFoundError):
        decryption.file_decryption(
            pathlib.Path(enc_text_file_path),
            dec_test_path.joinpath("dir_not_exist"),
            pathlib.Path(TEST_RECIVER_KEYS_DIR).joinpath("private.pem"),
            pathlib.Path(TEST_SENDER_KEYS_DIR).joinpath("public.pem"),
        )

    with pytest.raises(FileNotFoundError):
        decryption.file_decryption(
            pathlib.Path(enc_text_file_path),
            dec_test_path,
            pathlib.Path(TEST_RECIVER_KEYS_DIR).joinpath("private_not_found.pem"),
            pathlib.Path(TEST_SENDER_KEYS_DIR).joinpath("public.pem"),
        )

    with pytest.raises(FileNotFoundError):
        decryption.file_decryption(
            pathlib.Path(enc_text_file_path),
            dec_test_path,
            pathlib.Path(TEST_RECIVER_KEYS_DIR).joinpath("private.pem"),
            pathlib.Path(TEST_SENDER_KEYS_DIR).joinpath("public_not_found.pem"),
        )
