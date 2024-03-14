from __future__ import annotations
from typing import Protocol
import re
import pathlib
from model import Model
from os import startfile
import configuration as con
from datetime import datetime
from hybrid_crypto import encryption
from hybrid_crypto import decryption
from hybrid_crypto import genarate_keys


class View(Protocol):
    def mainWindow(self, presenter: Presenter) -> None: ...

    def set_my_keys_table_data(self, data: list[tuple]) -> None: ...

    def set_pub_keys_table_data(self, data: list[tuple]) -> None: ...

    def lodingWindow(self, massage: str, target: object) -> None: ...

    def error_messagebox(title: str, massage: str) -> None: ...

    def info_messagebox(self, title: str, massage: str) -> None: ...

    def askyesno_messagebox(self, title: str, massage: str) -> None: ...

    def mainloop(self) -> None: ...


class Presenter:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view

    def gen_my_keys(self) -> None:
        self.update_progressber(0)

        file_path = pathlib.Path(con.MY_KEYS_DIRECTORY)

        if not file_path.exists():
            file_path.mkdir()

        self.update_progressber(10)

        dir_name = genarate_keys.genarate_RSA_key(file_path)

        self.update_progressber(30)

        self.model.insert_my_key_data(
            {
                "id": None,
                "folder_name": dir_name,
                "date_string": str(datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")),
                "total_encryption_file_no": 0,
                "key_folder_path": file_path.joinpath(dir_name).as_posix(),
            }
        )

        self.update_progressber(20)

        data = self.model.get_last_row_from_my_key()

        self.update_progressber(20)

        self.view.my_keys_table.insert(parent="", index="end", values=data)

        self.update_progressber(15)

        self.view.loding_window.destroy()

    def set_my_keys_table_data(self) -> None:
        data = self.model.get_my_keys_data()
        self.view.set_my_keys_table_data(data)

    def del_my_keys(self) -> None:
        """Delete MY Owne Key From Treeview"""
        self.update_progressber(0)
        selection = self.view.my_keys_table.selection()
        count = 1
        for item in selection:
            # Get selection item value
            item_value = self.view.my_keys_table.item(item)["values"]
            # Delets Public Key Folder
            key_dir = pathlib.Path(item_value[4])
            key_dir.joinpath("private.pem").unlink()
            key_dir.joinpath("public.pem").unlink()
            key_dir.rmdir()
            # Delets entry from database
            self.model.del_my_keys_table_data(item_value[0])
            # Delets entry from treeview
            self.view.my_keys_table.delete(item)
            self.update_progressber((count / len(selection)) * 100)
            count += 1

        self.view.loding_window.destroy()

    def open_my_keys_folder(self) -> None:
        item = self.view.my_keys_table.focus()
        startfile(pathlib.Path(self.view.my_keys_table.item(item)["values"][4]))

    def set_pub_keys_table_data(self) -> None:
        data = self.model.get_pub_keys_data()
        self.view.set_pub_keys_table_data(data)

    def del_pub_keys(self) -> None:

        self.update_progressber(0)
        selection = self.view.pub_keys_table.selection()
        count = 1
        for item in selection:
            item_value = self.view.pub_keys_table.item(item)["values"]
            # Delets Public Key Folder
            dir_path = pathlib.Path(item_value[4])
            # Remove public key
            dir_path.joinpath("public.pem").unlink()
            # Remove folder
            dir_path.rmdir()
            # Deleate last entry from database
            self.model.del_pub_keys_table_data(item_value[0])
            # Delets same entry on GUI
            self.view.pub_keys_table.delete(item)
            self.update_progressber((count / len(selection)) * 100)
            count += 1
        self.view.loding_window.destroy()

    def open_pub_keys_folder(self) -> None:
        """Open public keys foulder"""
        item = self.view.pub_keys_table.focus()
        startfile(pathlib.Path(self.view.pub_keys_table.item(item)["values"][4]))

    def save_pub_key_file(self) -> None:
        """This function get user given public key and save it"""
        input_file_path = pathlib.Path(self.view.pub_key_file_path_textbox.get())
        output_folder_path = con.PUBLIC_KEYS_DIRECTORY
        if not pathlib.Path(output_folder_path).exists():
            pathlib.Path(output_folder_path).mkdir()

        key_owner_name = self.view.name_textbox.get()

        try:
            self.update_progressber(0)

            with open(input_file_path, "r") as file:
                file_data = file.read()

            self.update_progressber(16.6666667)

            dir_name = "PUB_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            dir_path = pathlib.Path(output_folder_path).joinpath(dir_name)
            dir_path.mkdir(parents=True, exist_ok=True)

            self.update_progressber(16.6666667)
            with open(dir_path.joinpath("public.pem"), "w") as file:
                file.write(file_data)

            self.update_progressber(16.6666667)

            self.model.insert_pub_key_data(
                {
                    "id": None,
                    "key_owner_name": key_owner_name,
                    "date_string": str(datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")),
                    "key_folder_name": dir_name,
                    "key_folder_path": dir_path.as_posix(),
                }
            )
            self.update_progressber(16.6666667)

            data = self.model.get_last_row_from_pub()
            self.update_progressber(16.6666667)

            self.view.pub_keys_table.insert(parent="", index="end", values=data)
            self.update_progressber(16.6666667)

            self.view.loding_window.destroy()

        except Exception as e:
            print(e)

    def update_pub_key_file(self) -> None:
        """This function get user given public key and save it"""

        input_file_path = pathlib.Path(self.view.update_pub_key_file_path_textbox.get())
        output_folder_path = con.PUBLIC_KEYS_DIRECTORY
        key_owner_name = self.view.update_name_textbox.get()

        treeview_id = self.view.pub_keys_table.focus()
        old_item = self.view.pub_keys_table.item(treeview_id)["values"]

        try:
            self.update_progressber(0)

            with open(input_file_path, "r") as file:
                file_data = file.read()
            self.update_progressber(14.2857143)

            # Delets old public key folder
            old_dir_path = pathlib.Path(old_item[4])
            old_dir_path.joinpath("public.pem").unlink()
            old_dir_path.rmdir()
            self.update_progressber(14.2857143)

            dir_name = "PUB_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            dir_path = pathlib.Path(output_folder_path).joinpath(dir_name)
            dir_path.mkdir(parents=True, exist_ok=True)
            self.update_progressber(14.2857143)

            with open(dir_path.joinpath("public.pem"), "w") as file:
                file.write(file_data)
            self.update_progressber(14.2857143)

            self.model.update_pub_keys_data(
                {
                    "id": old_item[0],
                    "key_owner_name": key_owner_name,
                    "date_string": str(datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")),
                    "key_folder_name": dir_name,
                    "key_folder_path": dir_path.as_posix(),
                }
            )
            self.update_progressber(14.2857143)

            new_data = (
                old_item[0],
                key_owner_name,
                str(datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")),
                dir_name,
                dir_path.as_posix(),
            )

            # Update new data
            self.view.pub_keys_table.item(treeview_id, text="", values=new_data)
            self.update_progressber(14.2857143)

            self.view.loding_window.destroy()

        except Exception as e:
            print("somthing is wrongs")
            print(e)

    def get_private_key_id_and_folder_name(self) -> list[str]:
        data = self.model.get_id_and_folder_name_from_private_keys()
        new_data = list()
        for row in data:
            new_data.append(f"{row[0]} - [{row[1]}]")
        return new_data

    def get_public_key_id_and_folder_name(self) -> list[str]:
        data = self.model.get_id_and_folder_name_from_public_keys()
        new_data = list()

        for row in data:
            new_data.append(f"{row[0]} - [{row[1]}]")

        return new_data

    # Encription Text
    def encryption_text(self) -> None:
        plain_text = self.view.plain_textbox.get(1.0, "end")
        privet_key = self.view.privet_key_drop_drown.get()
        public_key = self.view.public_key_drop_drown.get()
        output_dir_path = self.view.show_output_folder_path_textbox.get()
        self.update_progressber(20)
        privet_key_data = self.model.find_private_key_by_id(
            self.get_key_id(privet_key)
        )[0]
        self.update_progressber(20)
        public_key_data = self.model.find_public_key_by_id(self.get_key_id(public_key))[
            0
        ]
        self.update_progressber(20)

        enc_file_name = "OUTPUT_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f")

        enc_file_path = encryption.text_encryption(
            input_str=plain_text,
            output_file_path=pathlib.Path(output_dir_path).joinpath(
                f"{enc_file_name}.enc"
            ),
            pub_key_file_path=pathlib.Path(public_key_data[4]).joinpath("public.pem"),
            priv_key_file_path=pathlib.Path(privet_key_data[4]).joinpath("private.pem"),
        )
        self.update_progressber(20)

        self.model.update_total_encryption_file_no_from_my_key(
            privet_key_data[0], int(privet_key_data[3] + 1)
        )
        self.update_progressber(20)

        self.view.loding_window.destroy()
        self.view.info_messagebox(
            "File Saved Successfully", f"Your Encription File Save to {enc_file_path}"
        )

    # Encription File
    def encryption_file(self) -> None:
        input_file_path = self.view.show_input_file_path.get()
        privet_key_id_and_name = self.view.privet_key_drop_drown.get()
        public_key_id_and_name = self.view.public_key_drop_drown.get()
        output_dir_path = self.view.show_output_folder_path.get()

        privet_key_data = self.model.find_private_key_by_id(
            self.get_key_id(privet_key_id_and_name)
        )[0]
        self.update_progressber(25)
        public_key_data = self.model.find_public_key_by_id(
            self.get_key_id(public_key_id_and_name)
        )[0]
        self.update_progressber(25)

        enc_file_name = "OUTPUT_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        self.update_progressber(25)

        enc_file_path = encryption.file_encryption(
            input_file_path=pathlib.Path(input_file_path),
            output_file_path=pathlib.Path(output_dir_path).joinpath(
                f"{enc_file_name}.enc"
            ),
            pub_key_file_path=pathlib.Path(public_key_data[4]).joinpath("public.pem"),
            priv_key_file_path=pathlib.Path(privet_key_data[4]).joinpath("private.pem"),
        )
        self.update_progressber(25)

        self.model.update_total_encryption_file_no_from_my_key(
            privet_key_data[0], int(privet_key_data[3] + 1)
        )
        self.update_progressber(25)

        self.view.loding_window.destroy()
        self.view.info_messagebox(
            "File Saved Successfully", f"Encription File Save to {enc_file_path}"
        )

    # Encription Folder
    def encryption_folder(self) -> None:
        input_folder_path = pathlib.Path(self.view.show_input_folder_path.get())
        privet_key = self.view.privet_key_drop_drown.get()
        public_key = self.view.public_key_drop_drown.get()
        output_dir_path = pathlib.Path(self.view.show_output_folder_path.get())
        privet_key_data = self.model.find_private_key_by_id(
            self.get_key_id(privet_key)
        )[0]
        public_key_data = self.model.find_public_key_by_id(self.get_key_id(public_key))[
            0
        ]

        all_files_and_dir_path = list(input_folder_path.rglob("*"))

        all_files_path = list()
        for p in all_files_and_dir_path:
            if not pathlib.Path(p).is_dir():
                all_files_path.append(p)

        out_dir = output_dir_path.joinpath("ENCRYPTION_FILES")
        out_dir.mkdir(exist_ok=True)

        count = 1
        for file in all_files_path:
            encryption.file_encryption(
                input_file_path=file,
                output_file_path=out_dir.joinpath(f"ENCRYPTION_{count}.enc"),
                pub_key_file_path=pathlib.Path(public_key_data[4]).joinpath(
                    "public.pem"
                ),
                priv_key_file_path=pathlib.Path(privet_key_data[4]).joinpath(
                    "private.pem"
                ),
            )
            self.model.update_total_encryption_file_no_from_my_key(
                privet_key_data[0], int(privet_key_data[3] + 1)
            )
            total_files = len(all_files_path)
            self.update_progressber((count / total_files) * 100)
            count += 1
        self.view.loding_window.destroy()
        self.view.info_messagebox(
            "Encryption Successfully",
            f"Total {count} encription files save to: {out_dir}",
        )

    # Decryption file
    def decryption_file(self) -> None:
        input_file_path = self.view.show_input_file_path.get()
        privet_key = self.view.privet_key_drop_drown.get()
        public_key = self.view.public_key_drop_drown.get()
        output_dir_path = self.view.show_output_folder_path.get()
        self.update_progressber(25)

        privet_key_data = self.model.find_private_key_by_id(
            self.get_key_id(privet_key)
        )[0]
        self.update_progressber(25)
        public_key_data = self.model.find_public_key_by_id(self.get_key_id(public_key))[
            0
        ]
        self.update_progressber(25)
        try:
            dec_file_path = decryption.file_decryption(
                encrypt_file_path=pathlib.Path(input_file_path),
                output_folder_path=pathlib.Path(output_dir_path),
                priv_key_file_path=pathlib.Path(privet_key_data[4]).joinpath(
                    "private.pem"
                ),
                pub_key_file_path=pathlib.Path(public_key_data[4]).joinpath(
                    "public.pem"
                ),
            )
            self.update_progressber(25)

            self.view.loding_window.destroy()
            self.view.info_messagebox(
                "File Saved Successfully",
                f"Your decripted file save to: {dec_file_path}",
            )
        except decryption.EncryptionDataNotFoundError:
            self.view.loding_window.destroy()
            self.view.error_messagebox(
                "Decription Error", "This is not valide encryption file."
            )
        except decryption.InvalidTokenError:
            self.view.loding_window.destroy()
            self.view.error_messagebox(
                "Decription Error", "Encrypted token is not valid."
            )
        except decryption.SignatureVerificationError:
            self.view.loding_window.destroy()
            self.view.error_messagebox(
                "Decription Error", "File signature is not valid."
            )
        except decryption.KeyNotDecryptedError:
            self.view.loding_window.destroy()
            self.view.error_messagebox(
                "Decription Error", "Encription file not decrypt."
            )

    # Decryption folder
    def decryption_folder(self) -> None:
        input_folder_path = pathlib.Path(self.view.show_input_folder_path.get())
        privet_key = self.view.privet_key_drop_drown.get()
        public_key = self.view.public_key_drop_drown.get()
        output_dir_path = pathlib.Path(self.view.show_output_folder_path.get())
        privet_key_data = self.model.find_private_key_by_id(
            self.get_key_id(privet_key)
        )[0]
        public_key_data = self.model.find_public_key_by_id(self.get_key_id(public_key))[
            0
        ]

        all_files_path = list(input_folder_path.rglob("*.enc"))

        out_dir = output_dir_path.joinpath("DECRYPTION_FILES")
        out_dir.mkdir(exist_ok=True)

        count = 1
        error_file = 0
        for file in all_files_path:
            try:
                decryption.file_decryption(
                    encrypt_file_path=pathlib.Path(file),
                    output_folder_path=pathlib.Path(out_dir),
                    priv_key_file_path=pathlib.Path(privet_key_data[4]).joinpath(
                        "private.pem"
                    ),
                    pub_key_file_path=pathlib.Path(public_key_data[4]).joinpath(
                        "public.pem"
                    ),
                )
                total_files = len(all_files_path)
                self.update_progressber((count / total_files) * 100)
            except (
                decryption.EncryptionDataNotFoundError,
                decryption.InvalidTokenError,
                decryption.SignatureVerificationError,
                decryption.KeyNotDecryptedError,
            ) as e:
                error_file += 1
            count += 1
        self.view.loding_window.destroy()
        self.view.info_messagebox(
            "Decryption Successfully",
            f"Total encription file {len(all_files_path)} and decrypted {len(all_files_path) - error_file} file save to: {out_dir}",
        )

    # Lading GUI
    def loadGUI(self) -> None:
        self.view.mainWindow(self)
        self.view.mainloop()
        self.model.close_connection()

    # Validation Parts
    def validation_delete_my_keys(self) -> None:
        """Validation Delete Button Inputs."""
        selection = self.view.my_keys_table.selection()

        selection_keys_name = ""
        if len(selection) <= 10:
            for id in selection:
                selection_keys_name += f"[{self.view.my_keys_table.item(id)['values'][0]} - {self.view.my_keys_table.item(id)['values'][1]}]\n"
        else:
            for index in range(len(selection)):
                if index <= 10:
                    selection_keys_name += f"[{self.view.my_keys_table.item(selection[index])['values'][0]} - {self.view.my_keys_table.item(selection[index])['values'][1]}]\n"
                else:
                    selection_keys_name += (
                        f"...{len(selection)-index} additional keys not shown"
                    )
                    break

        if len(selection) != 0:
            yes_or_no = self.view.askyesno_messagebox(
                "Deleteing Keys",
                f"Are you sure you want delete the following {len(selection)} private key?\n"
                + selection_keys_name,
            )
            if yes_or_no:
                self.view.lodingWindow("Delete Keys....", self.del_my_keys)
        else:
            pass

    def validation_open_my_keys_folder(self) -> None:
        """Validation Public Keys Foulder Open Button Inputs."""
        if len(self.view.my_keys_table.focus()) != 0:
            self.open_my_keys_folder()
        else:
            pass

    def validation_delete_public_key(self) -> None:
        """Validation Delete Button Input"""
        selection = self.view.pub_keys_table.selection()

        selection_keys_name = ""
        if len(selection) <= 10:
            for id in selection:
                selection_keys_name += f"[{self.view.pub_keys_table.item(id)['values'][0]} - {self.view.pub_keys_table.item(id)['values'][3]}]\n"
        else:
            for index in range(len(selection)):
                if index <= 10:
                    selection_keys_name += f"[{self.view.pub_keys_table.item(selection[index])['values'][0]} - {self.view.pub_keys_table.item(selection[index])['values'][3]}]\n"
                else:
                    selection_keys_name += (
                        f"...{len(selection)-index} additional keys not shown"
                    )
                    break

        if len(selection) != 0:
            yes_or_no = self.view.askyesno_messagebox(
                "Deleteing Public Keys",
                f"Are you sure you want delete the following {len(selection)} public key?\n"
                + selection_keys_name,
            )
            if yes_or_no:
                self.view.lodingWindow("Delete Public Keys....", self.del_pub_keys)
        else:
            pass

    def validation_open_public_keys_folder(self) -> None:
        """validation open public keys folder inputs."""
        if len(self.view.pub_keys_table.focus()) != 0:
            self.open_pub_keys_folder()
        else:
            pass

    def validation_add_public_key(self) -> None:
        input_file_path = pathlib.Path(self.view.pub_key_file_path_textbox.get())
        key_owner_name = self.view.name_textbox.get()

        # Key Owner Name Validation
        if str(key_owner_name).strip() == "":
            self.view.error_messagebox("Input error", "Key owner name cannot be empty.")

        # Public Key file Validation
        elif input_file_path.as_posix() == ".":
            self.view.error_messagebox(
                "Input error", "Please select a public key file."
            )
        elif str(input_file_path.suffix) != ".pem":
            self.view.error_messagebox(
                "Input error", "This file is not a public key file."
            )
        elif pathlib.Path(input_file_path).exists() != True:
            self.view.error_messagebox("Input error", "This file is not exist.")

        else:
            self.view.lodingWindow(
                "Please wait few secents....", self.save_pub_key_file
            )

    def validation_edit_public_key(self) -> None:
        """Validation edit public keys."""
        if len(self.view.pub_keys_table.focus()) != 0:
            self.view.updatePublicKey(self)
        else:
            pass

    def validation_update_public_key(self) -> None:
        input_file_path = pathlib.Path(self.view.update_pub_key_file_path_textbox.get())
        key_owner_name = self.view.update_name_textbox.get()

        # Key Owner Name Validation
        if str(key_owner_name).strip() == "":
            self.view.error_messagebox("Input error", "Key owner name cannot be empty.")

        # Public Key file Validation
        elif input_file_path.as_posix() == ".":
            self.view.error_messagebox(
                "Input error", "Please select a public key file."
            )
        elif str(input_file_path.suffix) != ".pem":
            self.view.error_messagebox(
                "Input error", "This file is not a public key file."
            )
        elif pathlib.Path(input_file_path).exists() != True:
            self.view.error_messagebox("Input error", "This file is not exist.")

        else:
            self.view.lodingWindow(
                "Please wait few secents....", self.update_pub_key_file
            )

    def validation_encryption_text(self) -> None:
        privet_key = self.view.privet_key_drop_drown.get()
        public_key = self.view.public_key_drop_drown.get()
        output_dir_path = self.view.show_output_folder_path_textbox.get()
        privet_key_data = self.model.find_private_key_by_id(self.get_key_id(privet_key))
        public_key_data = self.model.find_public_key_by_id(self.get_key_id(public_key))

        # Private Key Validation
        if len(str(privet_key).strip()) == 0:
            self.view.error_messagebox("Input error", "Please select your private key.")
        elif len(privet_key_data) == 0:
            self.view.error_messagebox(
                "Input error", "Please select a valide private key."
            )
        elif (len(privet_key_data) != 0) and (
            self.get_key_name(privet_key) != privet_key_data[0][1]
        ):
            self.view.error_messagebox(
                "Input error", "Please select a valide private key."
            )

        # Public Key Validation
        elif len(str(public_key).strip()) == 0:
            self.view.error_messagebox("Input error", "Please select a public Key.")
        elif len(public_key_data) == 0:
            self.view.error_messagebox(
                "Input error", "Please select a valide public key."
            )
        elif (len(public_key_data) != 0) and (
            self.get_key_name(public_key) != public_key_data[0][3]
        ):
            self.view.error_messagebox(
                "Input error", "Please select a valide private key."
            )

        # Output folder path validation
        elif len(str(output_dir_path).strip()) == 0:
            self.view.error_messagebox("Input error", "Please select output folder.")
        elif not pathlib.Path(output_dir_path).exists():
            self.view.error_messagebox(
                "Input error", "Output folder path is not valide."
            )

        else:
            self.view.lodingWindow("Encripting Text....", self.encryption_text)

    def validation_encryption_file(self) -> None:
        input_file_path = self.view.show_input_file_path.get()
        privet_key = self.view.privet_key_drop_drown.get()
        public_key = self.view.public_key_drop_drown.get()
        output_dir_path = self.view.show_output_folder_path.get()
        privet_key_data = self.model.find_private_key_by_id(self.get_key_id(privet_key))
        public_key_data = self.model.find_public_key_by_id(self.get_key_id(public_key))

        # Input file path Validation
        if len(str(input_file_path).strip()) == 0:
            self.view.error_messagebox("Input error", "Please select a file.")
        elif not pathlib.Path(input_file_path).exists():
            self.view.error_messagebox("Input error", "Input file path is not valide.")

        # Private Key Validation
        elif len(str(privet_key).strip()) == 0:
            self.view.error_messagebox("Input error", "Please select your private key.")
        elif len(privet_key_data) == 0:
            self.view.error_messagebox(
                "Input error", "Please select a valide private key."
            )
        elif (len(privet_key_data) != 0) and (
            self.get_key_name(privet_key) != privet_key_data[0][1]
        ):
            self.view.error_messagebox(
                "Input error", "Please select a valide private key."
            )

        # Public Key Validation
        elif len(str(public_key).strip()) == 0:
            self.view.error_messagebox("Input error", "Please select a public Key.")
        elif len(public_key_data) == 0:
            self.view.error_messagebox(
                "Input error", "Please select a valide public key."
            )
        elif (len(public_key_data) != 0) and (
            self.get_key_name(public_key) != public_key_data[0][3]
        ):
            self.view.error_messagebox(
                "Input error", "Please select a valide private key."
            )

        # Output Path Validation
        elif len(str(output_dir_path).strip()) == 0:
            self.view.error_messagebox("Input error", "Please select output folder.")
        elif not pathlib.Path(output_dir_path).exists():
            self.view.error_messagebox(
                "Input error", "Output folder path is not valide."
            )

        else:
            self.view.lodingWindow("Please wait few secents....", self.encryption_file)

    def validation_encryption_folder(self) -> None:
        input_folder_path = self.view.show_input_folder_path.get()
        privet_key = self.view.privet_key_drop_drown.get()
        public_key = self.view.public_key_drop_drown.get()
        output_dir_path = self.view.show_output_folder_path.get()
        privet_key_data = self.model.find_private_key_by_id(self.get_key_id(privet_key))
        public_key_data = self.model.find_public_key_by_id(self.get_key_id(public_key))

        # Input file path Validation
        if len(str(input_folder_path).strip()) == 0:
            self.view.error_messagebox(
                "Input error", "Please select a Encription folder."
            )
        elif not pathlib.Path(input_folder_path).exists():
            self.view.error_messagebox("Input error", "Input file path is not valide.")

        # Private Key Validation
        elif len(str(privet_key).strip()) == 0:
            self.view.error_messagebox("Input error", "Please select your private key.")
        elif len(privet_key_data) == 0:
            self.view.error_messagebox(
                "Input error", "Please select a valide private key."
            )
        elif (len(privet_key_data) != 0) and (
            self.get_key_name(privet_key) != privet_key_data[0][1]
        ):
            self.view.error_messagebox(
                "Input error", "Please select a valide private key."
            )

        # Public Key Validation
        elif len(str(public_key).strip()) == 0:
            self.view.error_messagebox("Input error", "Please select a public Key.")
        elif len(public_key_data) == 0:
            self.view.error_messagebox(
                "Input error", "Please select a valide public key."
            )
        elif (len(public_key_data) != 0) and (
            self.get_key_name(public_key) != public_key_data[0][3]
        ):
            self.view.error_messagebox(
                "Input error", "Please select a valide private key."
            )

        # Output Path Validation
        elif len(str(output_dir_path).strip()) == 0:
            self.view.error_messagebox("Input error", "Please select output folder.")
        elif not pathlib.Path(output_dir_path).exists():
            self.view.error_messagebox(
                "Input error", "Output folder path is not valide."
            )

        else:
            self.view.lodingWindow(
                "Please wait few secents....", self.encryption_folder
            )

    def validation_decryption_file(self) -> None:
        input_file_path = self.view.show_input_file_path.get()
        privet_key = self.view.privet_key_drop_drown.get()
        public_key = self.view.public_key_drop_drown.get()
        output_dir_path = self.view.show_output_folder_path.get()
        privet_key_data = self.model.find_private_key_by_id(self.get_key_id(privet_key))
        public_key_data = self.model.find_public_key_by_id(self.get_key_id(public_key))

        # Input file path Validation
        if len(str(input_file_path).strip()) == 0:
            self.view.error_messagebox("Input error", "Please select a file.")
        elif not pathlib.Path(input_file_path).exists():
            self.view.error_messagebox("Input error", "Input file path is not valide.")

        # Private Key Validation
        elif len(str(privet_key).strip()) == 0:
            self.view.error_messagebox("Input error", "Please select your private key.")
        elif len(privet_key_data) == 0:
            self.view.error_messagebox(
                "Input error", "Please select a valide private key."
            )
        elif (len(privet_key_data) != 0) and (
            self.get_key_name(privet_key) != privet_key_data[0][1]
        ):
            self.view.error_messagebox(
                "Input error", "Please select a valide private key."
            )

        # Public Key Validation
        elif len(str(public_key).strip()) == 0:
            self.view.error_messagebox("Input error", "Please select a public Key.")
        elif len(public_key_data) == 0:
            self.view.error_messagebox(
                "Input error", "Please select a valide public key."
            )
        elif (len(public_key_data) != 0) and (
            self.get_key_name(public_key) != public_key_data[0][3]
        ):
            self.view.error_messagebox(
                "Input error", "Please select a valide private key."
            )

        # Output Path Validation
        elif len(str(output_dir_path).strip()) == 0:
            self.view.error_messagebox("Input error", "Please select output folder.")
        elif not pathlib.Path(output_dir_path).exists():
            self.view.error_messagebox(
                "Input error", "Output folder path is not valide."
            )

        else:
            ...
            self.view.lodingWindow("Please wait few secents....", self.decryption_file)

    def validation_decryption_folder(self) -> None:
        input_folder_path = self.view.show_input_folder_path.get()
        privet_key = self.view.privet_key_drop_drown.get()
        public_key = self.view.public_key_drop_drown.get()
        output_dir_path = self.view.show_output_folder_path.get()
        privet_key_data = self.model.find_private_key_by_id(self.get_key_id(privet_key))
        public_key_data = self.model.find_public_key_by_id(self.get_key_id(public_key))

        # Input file path Validation
        if len(str(input_folder_path).strip()) == 0:
            self.view.error_messagebox(
                "Input error", "Please select a decription folder."
            )
        elif not pathlib.Path(input_folder_path).exists():
            self.view.error_messagebox("Input error", "Input file path is not valide.")

        # Private Key Validation
        elif len(str(privet_key).strip()) == 0:
            self.view.error_messagebox("Input error", "Please select your private key.")
        elif len(privet_key_data) == 0:
            self.view.error_messagebox(
                "Input error", "Please select a valide private key."
            )
        elif (len(privet_key_data) != 0) and (
            self.get_key_name(privet_key) != privet_key_data[0][1]
        ):
            self.view.error_messagebox(
                "Input error", "Please select a valide private key."
            )

        # Public Key Validation
        elif len(str(public_key).strip()) == 0:
            self.view.error_messagebox("Input error", "Please select a public Key.")
        elif len(public_key_data) == 0:
            self.view.error_messagebox(
                "Input error", "Please select a valide public key."
            )
        elif (len(public_key_data) != 0) and (
            self.get_key_name(public_key) != public_key_data[0][3]
        ):
            self.view.error_messagebox(
                "Input error", "Please select a valide private key."
            )

        # Output Path Validation
        elif len(str(output_dir_path).strip()) == 0:
            self.view.error_messagebox("Input error", "Please select output folder.")
        elif not pathlib.Path(output_dir_path).exists():
            self.view.error_messagebox(
                "Input error", "Output folder path is not valide."
            )

        else:
            ...
            self.view.lodingWindow(
                "Please wait few secents....", self.decryption_folder
            )

    # helping function
    def update_progressber(self, value) -> None:
        """This function update progressbar"""
        self.view.loding_progressber["value"] += value
        self.view.loding_progressber.update()
        # print(self.view.loding_progressber["value"])

    def get_key_id(self, raw_data: str) -> int:
        if match := re.search(r"^(.+) -", raw_data):
            return int(match.group(1))
        else:
            return -1

    def get_key_name(self, raw_data: str) -> str:
        if match := re.search(r"\[(.*?)\]$", raw_data):
            return match.group(1)
        else:
            return ""
