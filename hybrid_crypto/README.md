# hybrid-crypto

`hybrid-crypto` directory is a python module and it is the improtent module of Crypto50 softwer. So, do not delete** any files and `hybrid-crypto` directory 🙅. If delete Crypto50 give some errors.

Please readme before delete any files 🥺 and do not delete .

### Directory Stucture 🗃️:

```bash
    addon.py
    decryption.py
    encryption.py
    genarate_keys.py
    requirements.txt
    __init__.py
```
#### Files 📄:
- `addon.py` file contains some helping function for hybrid-crypto module.
- `encryption.py` file contains encrypt file and text function.
- `decryption.py` file decrypt only encrypted file text.
- `genarate_keys.py` file genarate RSA keys.
- `__init__.py` file define this directory is a module.
- `requirements.txt` file contains all dependencies.

### Install Dependencies 📦:
- Install `Python` and `pip` (if already install skip this step)
- Run this command : `pip intall -r requirements.txt`

### Genarate RSA Keys 🔑:
```python
>>> from hybrid_crypto import genarate_keys
>>> key_dir_name = genarate_keys.genarate_RSA_key("OUTPUT_DIRECTORY_PATH")
>>> print(key_dir_name) 
KEYS_20240305_110825_858294
```

### Encryption File 🔒📄:
```python
>>> from hybrid_crypto import encryption
>>> enc_file_path = encryption.file_encryption(
            "INPUT_FILE_PATH/INPUT_FILE.txt",
            "OUTPUT_FILE_PATH/ENCRYPTION_FILE_NAME.enc",
            "RECIVER_PUBLIC_KEY_FILE_PATH/public.pem",
            "SENDER_PRIVET_KEY_FILE_PATH/private.pem",
    )
>>> print(enc_file_path)
OUTPUT_FILE_PATH/ENCRYPTION_FILE_NAME.enc
```
### Encryption Text 🔒📝:

```python
>>> from hybrid_crypto import encryption
>>> enc_file_path = encryption.text_encryption(
            "INPUT_TEXT",
            "OUTPUT_FILE_PATH/ENCRYPTION_FILE_NAME.enc",
            "RECIVER_PUBLIC_KEY_FILE_PATH/public.pem",
            "SENDER_PRIVET_KEY_FILE_PATH/private.pem",
    )
>>> print(enc_file_path)
OUTPUT_FILE_PATH/ENCRYPTION_FILE_NAME.enc
```

### Decryption File 🔓📄:

```python
>>> from hybrid_crypto import decryption
>>> dec_file_path = decryption.file_decryption(
                "ENCRYPTED_FILES_PATH/ENCRYPTION_FILE_NAME.enc",
                "OUTPUT_DIRECTORY_PATH",
                "RECIVER_PRIVET_KEY_FILE_PATH/private.pem",
                "SENDER_PUBLIC_KEY_FILE_PATH/public.pem",
    )
>>> print(dec_file_path)
OUTPUT_DIRECTORY_PATH/DECRYPT_20240307_015036_690327.text
```

