# Crypto50 : Secure Your Data with Hybrid Encryption 

 ![Crypto50 GUI](https://github.com/me50/codebysumit/assets/87431704/a1c6674d-55e6-433b-ab87-fed4c0035f72)


### Description 📜:

Crypto50 is user-friendly data encryption softwer build with python. that empowers you to encript and decript sensitive file and text data using a pawerful hybrid encryption aprroach. Crypto50 specially design to securely share your sensitive data through the internet i.e. email, cloud stroage etc. it offers both graphical (GUI) and command-line (CLI) interfaces and adheres to the Model-View-Presenter softwer design pattern.

------------------------------------------

### Crypto50 🔐:
- **Interfaces :** GUI and CLI
- **Softwer Architectural Pattern :** MVP
- **Encryption Tecnology :** Hybrid Cryptography
- **Version :** 1.0

------------------------------------------


### Crypto50 Hybrid Encryption and Decryption Diagram 📈:

![Hybrid Cryptography Diagram](https://github.com/me50/codebysumit/assets/87431704/1ea554cb-f913-4f4e-9110-fda5b58a1fdd)

------------------------------------------

### Dependencies 📦:
- Python - 3.11.1
- Packages :
    - cryptography - 42.0.2
    - Pillow - 10.2.0
    - pytest - 8.0.0
    - rsa - 4.9

------------------------------------------

### Setup 🛠️:
1. Clone GitHub repositories :
    - Open Terminal/CMD to a specific directory
    - Install `git` softwer (if already install skip this step)
    - Run this command : `git clone https://github.com/codebysumit/Crypto50.git`
2. Change working directory to project directory
    - Run this command : `cd Crypto50`
3. Install dependencies:
    - Install `Python` and `pip` (if already install skip this step)
    - Run this command : `pip intall -r requirements.txt`

------------------------------------------

### Unit Testing 🧪: 
- Open project root directory `Crypto50`
- Run this command : `python test_project.py`
- After unit testing some cache file automaticlly generated `__testfiles__/testing_module` this folder due to testing process \(you can **delete** this folder\).

------------------------------------------

### Run Crypto50 GUI Interfaces 🖥️:
- Open project root directory `Crypto50`
- Run this command : `python project.py`

 ![Crypto50 GUI](https://github.com/me50/codebysumit/assets/87431704/a1c6674d-55e6-433b-ab87-fed4c0035f72)


------------------------------------------

### Run Crypto50 CLI Interfaces ⌨️:
Open project root directory `Crypto50` and according to your requirment run flowing command.

1. Generate RSA Private key + Public :
    - Generate RSA keys set : `python crypto50.py --generate_key "OUTPUT_FOLDER_PATH"`


   - ``` python
     >>> python crypto50.py --generate_key "OUTPUT_FOLDER_PATH"
     Keys successfully save to: OUTPUT_FOLDER_PATH/KEYS_20240307_201805_425722
     ```

2. **Encryption :**
    - Encryption text : `python crypto50.py --encryption_text "INPUT_TEXT" --output "OUTPUT_FILE_PATH" --pub_key "RECIVER_PUBLIC_KEY_FILE_PATH" --priv_key "SENDER_PRIVET_KEY_FILE_PATH"`

    - ``` python
      >>> python crypto50.py --encryption_text "INPUT_TEXT" --output "OUTPUT_FILE_PATH/ENCRYPTION_FILE_NAME.enc" --pub_key "RECIVER_PUBLIC_KEY_FILE_PATH/public.pem" --priv_key "SENDER_PRIVET_KEY_FILE_PATH/private.pem"
      Encription text successfully save to: OUTPUT_FILE_PATH/ENCRYPTION_FILE_NAME.enc
      ```

    - Encryption File : `python crypto50.py --encryption_file "INPUT_FILE_PATH" --output "OUTPUT_FILE_PATH" --pub_key "RECIVER_PUBLIC_KEY_FILE_PATH" --priv_key "SENDER_PRIVET_KEY_FILE_PATH"`

    - ```python
      >>> python crypto50.py --encryption_file "INPUT_FILE_PATH/INPUT_FILE.txt" --output "OUTPUT_FILE_PATH/ENCRYPTION_FILE_NAME.enc" --pub_key "RECIVER_PUBLIC_KEY_FILE_PATH/public.pem" --priv_key "SENDER_PRIVET_KEY_FILE_PATH/private.pem"
      Encription file successfully save to: OUTPUT_FILE_PATH/ENCRYPTION_FILE_NAME.enc
      ```

    - Encryption Folder : `python crypto50.py --encryption_folder "INPUT_FOLDER_PATH" --output_dir "OUTPUT_FOLDER_PATH" --pub_key "RECIVER_PUBLIC_KEY_FILE_PATH" --priv_key "SENDER_PRIVET_KEY_FILE_PATH"`

    - ```python
      >>> python crypto50.py --encryption_folder "INPUT_FOLDER_PATH" --output_dir "OUTPUT_FOLDER_PATH" --pub_key "RECIVER_PUBLIC_KEY_FILE_PATH/public.pem" --priv_key "SENDER_PRIVET_KEY_FILE_PATH/private.pem"
      [1/4] : Successfully encripted "OUTPUT_FOLDER_PATH/INPUT_FILE_1.mp4" ==> "OUTPUT_FOLDER_PATH/ENCRYPTION_1.enc"
      [2/4] : Successfully encripted "OUTPUT_FOLDER_PATH/INPUT_FILE_2.jpg" ==> "OUTPUT_FOLDER_PATH/ENCRYPTION_2.enc"
      [3/4] : Successfully encripted "OUTPUT_FOLDER_PATH/INPUT_FILE_3.mp3" ==> "OUTPUT_FOLDER_PATH/ENCRYPTION_3.enc"
      [4/4] : Successfully encripted "OUTPUT_FOLDER_PATH/INPUT_FILE_4.txt" ==> "OUTPUT_FOLDER_PATH/ENCRYPTION_4.enc"
      Successfully encripted 4 files.
      ```


3. **Decryption :**
    - Decryption File : `python crypto50.py --decryption_file "ENCRYPTED_FILES_PATH" --output_dir "OUTPUT_FOLDER_PATH" --priv_key "RECIVER_PRIVET_KEY_FILE_PATH" --pub_key "SENDER_PUBLIC_KEY_FILE_PATH"`

    - ```python
      >>> python crypto50.py --decryption_file "ENCRYPTED_FILES_PATH/ENCRYPTION_FILE_NAME.enc" --output_dir "OUTPUT_FOLDER_PATH" --priv_key "RECIVER_PRIVET_KEY_FILE_PATH/private.pem" --pub_key "SENDER_PUBLIC_KEY_FILE_PATH/public.pem"
      Decription file successfully save to: OUTPUT_FOLDER_PATH/DECRYPT_20240307_212528_345110.txt
      ```

    - Decryption Folder : `python crypto50.py --decryption_folder "ENCRYPTED_FILES_FOLDER_PATH" --output_dir "OUTPUT_FOLDER_PATH" --priv_key "RECIVER_PRIVET_KEY_FILE_PATH" --pub_key "SENDER_PUBLIC_KEY_FILE_PATH"`

    - ```python
      >>> python crypto50.py --decryption_folder "ENCRYPTED_FILES_FOLDER_PATH" --output_dir "OUTPUT_FOLDER_PATH" --priv_key "RECIVER_PRIVET_KEY_FILE_PATH/private.pem" --pub_key "SENDER_PUBLIC_KEY_FILE_PATH/public.pem"

      [1/4] : Successfully decripted "ENCRYPTED_FILES_FOLDER_PATH/ENCRYPTION_1.enc" ==> "OUTPUT_FOLDER_PATH/DECRYPT_20240307_213118_115599.mp4"
      [2/4] : Successfully decripted "ENCRYPTED_FILES_FOLDER_PATH/ENCRYPTION_2.enc" ==> "OUTPUT_FOLDER_PATH/DECRYPT_20240307_213118_386111.jpg"
      [3/4] : Successfully decripted "ENCRYPTED_FILES_FOLDER_PATH/ENCRYPTION_3.enc" ==> "OUTPUT_FOLDER_PATH/DECRYPT_20240307_213118_897642.mp3"
      [4/4] : Successfully decripted "ENCRYPTED_FILES_FOLDER_PATH/ENCRYPTION_4.enc" ==> "OUTPUT_FOLDER_PATH/DECRYPT_20240307_213118_975783.txt"
      Successfully decripted 4 files.
      ```

------------------------------------------

### Command-line Argument List ⌨️:
| Argument | Description |
| -------- | ----------- |
| --generate_keys, -GENKEYS | Get output folder path and generate new public and private key file. |
| --encryption_file, -ENCFILE | Get input file path and encrypt this file |
| --encryption_text, -ENCTEXT | Get input text and encrypt this text |
| --encryption_folder, -ENCFOLDER | Get input folder and encrypt all file from the folder. |
| --decryption_file, -DECFILE | Get encrypt file path and decrypt this file |
| --decryption_folder, -DECFOLDER | Get encrypt folder path and decrypt all file from the folder |
| --output, -O | Get output file path |
| --output_dir, -ODIR | Get output folder path. |
| --pub_key, -PUB | Get public key file path. |
| --priv_key, -PRIV | Get private key file path. |


------------------------------------------

###  Features 🕹️:
| Features | Crypto50 CLI | Crypto50 GUI  | hybrid_crypto (Crypto50 Module) |
| :------: | :----------: | :----------:  | :-----------------------------: |
| Generate RSA Keys | ✅ | ✅ | ✅ |
| Encryption Texts | ✅ | ✅ | ✅ | ✅ |
| Encryption File | ✅ |  ✅ |  ✅ |
| Encryption Files From Folder | ✅ |  ✅ | ❌ |
| Decryption File | ✅ | ✅ | ✅ |
| Decryption Files from Folder | ✅ | ✅ | ❌ |
| My Keys Manager | ❌ | ✅ | ❌ |
| Public Keys Manager | ❌ | ✅ | ❌ | 

------------------------------------------

### Tested OS 📝:
| OS Name | Test Result |
| :-----: | :---------: |
| Windows 11 | ✅ |


------------------------------------------

### Tested Python Version 📝:
| Python Version | Test Result |
| :------------: | :---------: |
| 3.11.1 | ✅ |
