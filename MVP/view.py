import tkinter as tk
import configuration as con
import pathlib
import threading
from tkinter import ttk, filedialog, messagebox
from PIL import ImageTk, Image
from typing import Protocol


class Presenter(Protocol):
    def gen_my_keys(self) -> None: ...
    def set_my_keys_table_data(self) -> None: ...
    def set_pub_keys_table_data(self) -> None: ...
    def get_private_key_id_and_folder_name(self) -> list[str]: ...
    def get_public_key_id_and_folder_name(self) -> list[str]: ...
    def validation_delete_my_keys(self) -> None: ...
    def validation_open_my_keys_folder(self) -> None: ...
    def validation_delete_public_key(self) -> None: ...
    def validation_open_public_keys_folder(self) -> None: ...
    def validation_import_keys(self) -> None: ...
    def validation_add_public_key(self) -> None: ...
    def validation_edit_public_key(self) -> None: ...
    def validation_update_public_key(self) -> None: ...
    def validation_encryption_text(self) -> None: ...
    def validation_encryption_file(self) -> None: ...
    def validation_encryption_folder(self) -> None: ...
    def validation_decryption_file(self) -> None: ...
    def validation_decryption_folder(self) -> None: ...


class Cripto50(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        style = ttk.Style()
        style.theme_use("alt")

    # Application Windows
    def mainWindow(self, presenter: Presenter) -> None:
        """Main Window of Cripto50 App"""
        #  home drow setup
        self.geometry("500x480")
        self.title("Crypto50")
        self.resizable(width=False, height=False)
        self.config(bg=con.WINDOWS_BACKGROUNG_COLOR)

        # Set Home Window Icon
        home_window_icon = ImageTk.PhotoImage(
            Image.open(con.ICON_PHOTO).resize((50, 50))
        )
        self.iconphoto(True, home_window_icon)

        # Menu Section
        self.MainMenu(presenter)

        # Headder Section
        header_section = tk.Frame(self, background=con.HEADER_FRAME_BACKGROUND_COLOR)
        header_section.place(x=0, y=0, width=500, height=58)

        header_title = tk.Label(
            header_section,
            text="CRYPTO50",
            font=("Arial", 30),
            background=con.HEADER_FRAME_BACKGROUND_COLOR,
            foreground=con.HEADER_FRAME_TEXT_COLOR,
        )
        header_title.place(x=140, y=4)

        # Main Content Section
        # My Key Manager Section
        self.my_key_manager_icon = ImageTk.PhotoImage(
            Image.open(con.MY_KEY_MANAGER_ICON).resize((50, 50))
        )

        my_key_manager_button = tk.Button(
            self,
            text="My Key Manager",
            image=self.my_key_manager_icon,
            width=195,
            padx=10,
            bg=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=lambda: self.MyKeyManager(presenter),
            compound="left",
        )
        my_key_manager_button.place(x=20, y=70)
        # my_key_manager_button.image = my_key_manager_icon

        # Public Key Manager Section
        self.public_key_manager_icon = ImageTk.PhotoImage(
            Image.open(con.PUBLIC_KEY_MANAGER_ICON).resize((50, 50))
        )
        pub_key_manager_button = tk.Button(
            self,
            text="Public Key Manager",
            image=self.public_key_manager_icon,
            width=195,
            padx=10,
            bg=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=lambda: self.PublicKeyManager(presenter),
            compound="left",
        )
        pub_key_manager_button.place(x=258, y=70)

        # Encryption Button
        self.encryption_text_icon = ImageTk.PhotoImage(
            Image.open(con.ENCRYPTION_TEXT_ICON).resize((50, 50))
        )
        encryption_text_button = tk.Button(
            self,
            text="Encryption Texts",
            image=self.encryption_text_icon,
            width=115,
            height=100,
            padx=10,
            pady=10,
            bg=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=lambda: self.EncryptText(presenter),
            compound="top",
        )
        encryption_text_button.place(x=20, y=140)

        # Encryption File Button
        self.encryption_file_icon = ImageTk.PhotoImage(
            Image.open(con.ENCRYPTION_FILE_ICON).resize((50, 50))
        )
        encryption_file_button = tk.Button(
            self,
            text="Encryption File",
            image=self.encryption_file_icon,
            width=115,
            height=100,
            padx=10,
            pady=10,
            bg=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=lambda: self.EncryptFile(presenter),
            compound="top",
        )
        encryption_file_button.place(x=180, y=140)

        # Encryption Folder Button
        self.encryption_folder_icon = ImageTk.PhotoImage(
            Image.open(con.ENCRYPTION_FOLDER_ICON).resize((50, 50))
        )
        encryption_folder_button = tk.Button(
            self,
            text="Encryption Files\nFrom Folder",
            image=self.encryption_folder_icon,
            width=115,
            height=100,
            padx=10,
            pady=10,
            bg=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=lambda: self.EncryptFoulder(presenter),
            compound="top",
        )
        encryption_folder_button.place(x=340, y=140)

        # Decryption File Button
        self.decryption_file_icon = ImageTk.PhotoImage(
            Image.open(con.DECRYPTION_FILE_ICON).resize((50, 50))
        )
        decryption_file_button = tk.Button(
            self,
            text="Decryption File",
            image=self.decryption_file_icon,
            width=435,
            height=60,
            padx=10,
            bg=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=lambda: self.DecryptFile(presenter),
            compound="left",
        )
        decryption_file_button.place(x=20, y=280)

        # Decryption Folder Button
        self.decryption_folder_icon = ImageTk.PhotoImage(
            Image.open(con.DECRYPTION_FOLDER_ICON).resize((50, 50))
        )
        decryption_folder_button = tk.Button(
            self,
            text="Decryption Files From Folder",
            image=self.decryption_folder_icon,
            width=435,
            height=60,
            padx=10,
            bg=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=lambda: self.DecryptFoulder(presenter),
            compound="left",
        )
        decryption_folder_button.place(x=20, y=360)

        # Footer Section
        footer_frame = tk.Frame(
            self,
            bg=con.FOOTER_BACKGROUND_COLOR,
        )
        footer_frame.place(x=0, y=440, width=500, height=40)

        footer_label = tk.Label(
            footer_frame,
            text="Cripto50 Encryption Softwer V 1.0.",
            background=con.FOOTER_BACKGROUND_COLOR,
            foreground=con.FOOTER_TEXT_COLOR,
        )
        footer_label.place(x=20, y=9)

    def MainMenu(self, presenter: Presenter) -> None:
        """Main menubar of Cripto50 App"""
        # Main Menubar
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        self.menu_exit_icon = ImageTk.PhotoImage(
            Image.open(con.EXIT_ICON).resize((12, 12))
        )

        file_menu = tk.Menu(
            menubar,
            tearoff=0,
            # background=con.WINDOWS_BACKGROUNG_COLOR,
            activebackground=con.SELECTION_ACTIVE_BACKGROUNG_COLOR,
        )
        menubar.add_cascade(label="Menu", menu=file_menu)
        file_menu.add_command(
            label="Encryption Texts", command=lambda: self.EncryptText(presenter)
        )
        file_menu.add_command(
            label="Encryption File", command=lambda: self.EncryptFile(presenter)
        )
        file_menu.add_command(
            label="Encription Files From Folder",
            command=lambda: self.EncryptFoulder(presenter),
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Decription File", command=lambda: self.DecryptFile(presenter)
        )
        file_menu.add_command(
            label="Encription Files From Folder",
            command=lambda: self.DecryptFoulder(presenter),
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Exit",
            image=self.menu_exit_icon,
            compound="left",
            command=lambda: self.destroy(),
        )

        tools_menu = tk.Menu(
            menubar,
            tearoff=0,
            # background=con.WINDOWS_BACKGROUNG_COLOR,
            activebackground=con.SELECTION_ACTIVE_BACKGROUNG_COLOR,
        )
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(
            label="My keys Manager", command=lambda: self.MyKeyManager(presenter)
        )
        tools_menu.add_separator()
        tools_menu.add_command(
            label="Public Key Manager", command=lambda: self.PublicKeyManager(presenter)
        )

    def MyKeyManager(self, presenter: Presenter) -> None:
        """My Key Manager Window"""
        self.my_key_manager_window = tk.Toplevel(self)
        self.my_key_manager_window.geometry("660x460")
        self.my_key_manager_window.resizable(width=False, height=False)
        self.my_key_manager_window.title("My Key Manager")
        self.my_key_manager_window.config(bg=con.WINDOWS_BACKGROUNG_COLOR)
        self.my_key_manager_window.grab_set()

        self.my_key_manager_window.iconphoto(False, self.my_key_manager_icon)

        # genarate new key button
        self.add_icon = ImageTk.PhotoImage(Image.open(con.PLUS_ICON).resize((10, 10)))

        genarate_new_key_button = tk.Button(
            self.my_key_manager_window,
            text=" Genrate New Keys",
            image=self.add_icon,
            width=290,
            pady=8,
            font=("Arial", 10, "bold"),
            background=con.PRIMARY_BUTTON_BACKGROUND_COLOR,
            foreground=con.PRIMARY_BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=lambda: self.lodingWindow(
                "Please wait few secents....", presenter.gen_my_keys
            ),
            compound="left",
        )
        genarate_new_key_button.place(x=20, y=5)
        genarate_new_key_button.image = self.add_icon

        # import keys button
        import_keys_button = tk.Button(
            self.my_key_manager_window,
            text=" Import Keys",
            image=self.add_icon,
            width=290,
            pady=8,
            font=("Arial", 10, "bold"),
            background=con.PRIMARY_BUTTON_BACKGROUND_COLOR,
            foreground=con.PRIMARY_BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=lambda: self.importKeys(presenter),
            compound="left",
        )
        import_keys_button.place(x=335, y=5)
        import_keys_button.image = self.add_icon

        # Tabile data
        self.my_keys_table = ttk.Treeview(
            self.my_key_manager_window,
            columns=("id", "folder_name", "date", "total_no_of_en"),
            show="headings",
        )

        self.my_keys_table.heading("id", text="ID")
        self.my_keys_table.column("id", anchor="center", stretch="no", width=100)

        self.my_keys_table.heading("folder_name", text="NAME")
        self.my_keys_table.column(
            "folder_name", anchor="center", stretch="no", width=190
        )

        self.my_keys_table.heading("date", text="DATE")
        self.my_keys_table.column("date", anchor="center", stretch="no", width=150)

        self.my_keys_table.heading("total_no_of_en", text="TOLAL NO. OF ENCRYPTION")
        self.my_keys_table.column(
            "total_no_of_en", anchor="center", stretch="no", width=160
        )
        self.my_keys_table.place(x=20, y=51, width=602, height=350)

        scrollbar = ttk.Scrollbar(
            self.my_key_manager_window,
            orient="vertical",
            command=self.my_keys_table.yview,
        )
        scrollbar.place(x=624, y=52, height=348)
        self.my_keys_table.configure(yscrollcommand=scrollbar.set)

        # Set tabile data helping presenter
        presenter.set_my_keys_table_data()

        # Delets keys button
        delete_key_button = tk.Button(
            self.my_key_manager_window,
            text="Delete",
            padx=10,
            pady=5,
            background=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=presenter.validation_delete_my_keys,
        )
        delete_key_button.place(x=444, y=412)

        # Open keys button
        open_key_button = tk.Button(
            self.my_key_manager_window,
            text="Open",
            padx=10,
            pady=5,
            background=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=presenter.validation_open_my_keys_folder,
        )
        open_key_button.place(x=515, y=412)

        # Close my key window button
        close_key_button = tk.Button(
            self.my_key_manager_window,
            text="Close",
            padx=10,
            pady=5,
            background=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=lambda: self.my_key_manager_window.destroy(),
        )
        close_key_button.place(x=582, y=412)

    def PublicKeyManager(self, presenter: Presenter) -> None:
        """Public Key Manager Window"""
        self.public_key_manager_window = tk.Toplevel(self)
        self.public_key_manager_window.geometry("660x460")
        self.public_key_manager_window.resizable(width=False, height=False)
        self.public_key_manager_window.title("Public Key Manager")
        self.public_key_manager_window.config(background="#d0d0d8")
        self.public_key_manager_window.grab_set()

        self.public_key_manager_window.iconphoto(False, self.public_key_manager_icon)

        # Add New Public Key Button
        self.add_icon = ImageTk.PhotoImage(
            Image.open(pathlib.Path(con.PLUS_ICON)).resize((15, 15))
        )
        add_new_public_key_button = tk.Button(
            self.public_key_manager_window,
            text=" Add New Public Keys",
            image=self.add_icon,
            width=612,
            pady=8,
            font=("Arial", 10, "bold"),
            background=con.PRIMARY_BUTTON_BACKGROUND_COLOR,
            foreground=con.PRIMARY_BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=lambda: self.addPublicKey(presenter),
            compound="left",
            # background="gray"
        )
        add_new_public_key_button.place(x=20, y=5)
        add_new_public_key_button.image = self.add_icon

        # Public key Treeview
        self.pub_keys_table = ttk.Treeview(
            self.public_key_manager_window,
            columns=("id", "key_owner_name", "date", "file_name"),
            show="headings",
        )

        self.pub_keys_table.heading("id", text="ID")
        self.pub_keys_table.column("id", anchor="center", stretch="no", width=100)

        self.pub_keys_table.heading("key_owner_name", text="KEY OWNER NAME")
        self.pub_keys_table.column(
            "key_owner_name", anchor="center", stretch="no", width=190
        )

        self.pub_keys_table.heading("date", text="DATE")
        self.pub_keys_table.column("date", anchor="center", stretch="no", width=150)

        self.pub_keys_table.heading("file_name", text="FILE NAME")
        self.pub_keys_table.column(
            "file_name", anchor="center", stretch="no", width=160
        )
        self.pub_keys_table.place(x=20, y=51, width=602, height=350)

        # self.pub_keys_table.insert()

        scrollbar = ttk.Scrollbar(
            self.public_key_manager_window,
            orient="vertical",
            command=self.pub_keys_table.yview,
        )
        scrollbar.place(x=622, y=52, height=348)
        self.pub_keys_table.configure(yscrollcommand=scrollbar.set)

        # Set tabile data helping presenter
        presenter.set_pub_keys_table_data()

        # Public kew edit button
        edit_key_button = tk.Button(
            self.public_key_manager_window,
            text="Edit Key",
            padx=10,
            pady=5,
            background=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=presenter.validation_edit_public_key,
        )
        edit_key_button.place(x=364, y=412)

        # Public Key delets button
        delete_key_button = tk.Button(
            self.public_key_manager_window,
            text="Delete",
            padx=10,
            pady=5,
            background=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=presenter.validation_delete_public_key,
        )
        delete_key_button.place(x=444, y=412)

        # Public Keys Folder Open Button
        open_key_button = tk.Button(
            self.public_key_manager_window,
            text="Open",
            padx=10,
            pady=5,
            background=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=presenter.validation_open_public_keys_folder,
        )
        open_key_button.place(x=515, y=412)

        # Public Key Windrow Close Button
        close_key_button = tk.Button(
            self.public_key_manager_window,
            text="Close",
            padx=10,
            pady=5,
            background=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=lambda: self.public_key_manager_window.destroy(),
        )
        close_key_button.place(x=582, y=412)

    def importKeys(self, presenter: Presenter) -> None:
        """Public Keys Adding Window"""
        import_keys_window = tk.Toplevel(self)
        import_keys_window.geometry("500x250")
        import_keys_window.resizable(width=False, height=False)
        import_keys_window.title("Import Keys")
        import_keys_window.config(bg=con.WINDOWS_BACKGROUNG_COLOR)
        import_keys_window.grab_set()

        # Browes Private Key From section
        file_open_text_label = tk.Label(
            import_keys_window,
            font=("Arial", 9),
            text="Open Private Key From File:",
            foreground=con.INPUT_LABEL_TEXT_COLOR,
            background=con.WINDOWS_BACKGROUNG_COLOR,
        )
        file_open_text_label.place(x=20, y=20)

        self.private_key_file_path_textbox = tk.Entry(
            import_keys_window, font=("Arial", 10)
        )
        self.private_key_file_path_textbox.place(x=20, y=40, width=390, height=25)

        browse_key_file = tk.Button(
            import_keys_window,
            text="Browse",
            background=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=lambda: self.open_specific_file(
                self.private_key_file_path_textbox, filetypes=[("Peivate Keys", ".pem")]
            ),
        )
        browse_key_file.place(x=415, y=40, width=60)

        # Browes Public Key From section
        file_open_text_label = tk.Label(
            import_keys_window,
            font=("Arial", 9),
            text="Open Publuc Key From File:",
            foreground=con.INPUT_LABEL_TEXT_COLOR,
            background=con.WINDOWS_BACKGROUNG_COLOR,
        )
        file_open_text_label.place(x=20, y=100)

        self.public_key_file_path_textbox = tk.Entry(
            import_keys_window, font=("Arial", 10)
        )
        self.public_key_file_path_textbox.place(x=20, y=120, width=390, height=25)

        browse_key_file = tk.Button(
            import_keys_window,
            text="Browse",
            background=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=lambda: self.open_specific_file(
                self.public_key_file_path_textbox, filetypes=[("Public Keys", ".pem")]
            ),
        )
        browse_key_file.place(x=415, y=120, width=60)

        # Save Keys From File Button
        import_keys_window_from_file_button = tk.Button(
            import_keys_window,
            text="Add Keys From File",
            pady=5,
            padx=10,
            background=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=presenter.validation_import_keys,
        )
        import_keys_window_from_file_button.place(x=275, y=200)

        # Public Key Add Windrow Close Button
        close_window_butt = tk.Button(
            import_keys_window,
            text="Close",
            padx=10,
            pady=5,
            background=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=lambda: import_keys_window.destroy(),
        )
        close_window_butt.place(x=418, y=200)

    def addPublicKey(self, presenter: Presenter) -> None:
        """Public Keys Adding Window"""
        add_pub_key_window = tk.Toplevel(self)
        add_pub_key_window.geometry("500x250")
        add_pub_key_window.resizable(width=False, height=False)
        add_pub_key_window.title("Add New Public Key")
        add_pub_key_window.config(bg=con.WINDOWS_BACKGROUNG_COLOR)
        add_pub_key_window.grab_set()
        # add_pub_key_window.focus()

        add_pub_key_window.iconphoto(False, self.public_key_manager_icon)

        # User Input From
        # Public Key Owner Name Entry Section
        name_label = tk.Label(
            add_pub_key_window,
            font=("Arial", 9),
            text="Publuc Key Owner Name:",
            foreground=con.INPUT_LABEL_TEXT_COLOR,
            background=con.WINDOWS_BACKGROUNG_COLOR,
        )
        name_label.place(x=20, y=20)

        self.name_textbox = tk.Entry(add_pub_key_window, font=("Arial", 10))
        self.name_textbox.place(x=20, y=40, width=460, height=25)

        # Browes Public Key From section
        file_open_text_label = tk.Label(
            add_pub_key_window,
            font=("Arial", 9),
            text="Open Publuc Key From File:",
            foreground=con.INPUT_LABEL_TEXT_COLOR,
            background=con.WINDOWS_BACKGROUNG_COLOR,
        )
        file_open_text_label.place(x=20, y=100)

        self.pub_key_file_path_textbox = tk.Entry(
            add_pub_key_window, font=("Arial", 10)
        )
        self.pub_key_file_path_textbox.place(x=20, y=120, width=390, height=25)

        browse_key_file = tk.Button(
            add_pub_key_window,
            text="Browse",
            background=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=lambda: self.open_specific_file(
                self.pub_key_file_path_textbox, filetypes=[("Public Keys", ".pem")]
            ),
        )
        browse_key_file.place(x=415, y=120, width=60)

        # Save Public Keys From File Button
        add_pub_key_window_from_file_button = tk.Button(
            add_pub_key_window,
            text="Add Public Key From File",
            pady=5,
            padx=10,
            background=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=presenter.validation_add_public_key,
        )
        add_pub_key_window_from_file_button.place(x=240, y=200)

        # Public Key Add Windrow Close Button
        close_window_butt = tk.Button(
            add_pub_key_window,
            text="Close",
            padx=10,
            pady=5,
            background=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=lambda: add_pub_key_window.destroy(),
        )
        close_window_butt.place(x=418, y=200)

    def updatePublicKey(self, presenter: Presenter) -> None:
        """Public Keys Update Window"""
        update_pub_key_window = tk.Toplevel(self)
        update_pub_key_window.geometry("500x250")
        update_pub_key_window.resizable(width=False, height=False)
        update_pub_key_window.title("Edit Public Key")
        update_pub_key_window.config(bg=con.WINDOWS_BACKGROUNG_COLOR)
        update_pub_key_window.grab_set()
        # update_pub_key_window.focus()

        update_pub_key_window.iconphoto(False, self.public_key_manager_icon)

        treeview_id = self.pub_keys_table.focus()
        treeview_item = self.pub_keys_table.item(treeview_id)

        # User Input From
        # Public Key Owner Name Entry Section
        name_label = tk.Label(
            update_pub_key_window,
            font=("Arial", 9),
            text="Update Publuc Key Owner Name:",
            foreground=con.INPUT_LABEL_TEXT_COLOR,
            background=con.WINDOWS_BACKGROUNG_COLOR,
        )
        name_label.place(x=20, y=20)

        self.update_name_textbox = tk.Entry(update_pub_key_window, font=("Arial", 10))
        self.update_name_textbox.place(x=20, y=40, width=460, height=25)
        self.update_name_textbox.delete(0, "end")
        self.update_name_textbox.insert(0, treeview_item["values"][1])

        # Browes Public Key From section
        file_open_text_label = tk.Label(
            update_pub_key_window,
            font=("Arial", 9),
            text="Open Publuc Key From File:",
            foreground=con.INPUT_LABEL_TEXT_COLOR,
            background=con.WINDOWS_BACKGROUNG_COLOR,
        )
        file_open_text_label.place(x=20, y=100)

        self.update_pub_key_file_path_textbox = tk.Entry(
            update_pub_key_window, font=("Arial", 10)
        )
        self.update_pub_key_file_path_textbox.place(x=20, y=120, width=390, height=25)
        self.update_pub_key_file_path_textbox.delete(0, "end")
        self.update_pub_key_file_path_textbox.insert(
            0, pathlib.Path(treeview_item["values"][4]).joinpath("public.pem")
        )

        browse_key_file = tk.Button(
            update_pub_key_window,
            text="Browse",
            background=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=lambda: self.open_specific_file(
                self.update_pub_key_file_path_textbox,
                filetypes=[("Public Keys", ".pem")],
            ),
        )
        browse_key_file.place(x=415, y=120, width=60)

        # Save Public Keys From File Button
        add_pub_key_window_from_file_button = tk.Button(
            update_pub_key_window,
            text="Update Public Key",
            pady=5,
            padx=10,
            background=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=presenter.validation_update_public_key,
        )
        add_pub_key_window_from_file_button.place(x=285, y=200)

        # Public Key Add Windrow Close Button
        close_window_butt = tk.Button(
            update_pub_key_window,
            text="Close",
            padx=10,
            pady=5,
            background=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=lambda: update_pub_key_window.destroy(),
        )
        close_window_butt.place(x=418, y=200)

    def EncryptText(self, presenter: Presenter) -> None:
        encript_text_window = tk.Toplevel(self)
        encript_text_window.geometry("500x450")
        encript_text_window.resizable(width=False, height=False)
        encript_text_window.title("Encription Texts")
        encript_text_window.config(bg=con.WINDOWS_BACKGROUNG_COLOR)
        encript_text_window.grab_set()

        # BEGINING TEXTS BOX
        text_label = tk.Label(
            encript_text_window,
            font=("Arial", 9),
            text="Enter Your Secrets Text:",
            foreground=con.INPUT_LABEL_TEXT_COLOR,
            background=con.WINDOWS_BACKGROUNG_COLOR,
        )
        text_label.place(x=20, y=15)

        self.plain_textbox = tk.Text(encript_text_window)
        self.plain_textbox.place(x=20, y=40, width=428, height=200)

        text_box_scrollbar = ttk.Scrollbar(
            encript_text_window, orient="vertical", command=self.plain_textbox.yview
        )
        text_box_scrollbar.place(x=450, y=40, height=200)
        self.plain_textbox.configure(yscrollcommand=text_box_scrollbar.set)
        # END TEXTS BOX

        # BEGINING DROPDOWN LIST
        priv_key_drop_drown_values = presenter.get_private_key_id_and_folder_name()
        pub_key_drop_drown_values = presenter.get_public_key_id_and_folder_name()

        private_key_lebel = tk.Label(
            encript_text_window,
            text="Select Your Private Key:",
            foreground=con.INPUT_LABEL_TEXT_COLOR,
            background=con.WINDOWS_BACKGROUNG_COLOR,
        )
        private_key_lebel.place(x=20, y=250)

        self.privet_key_drop_drown = ttk.Combobox(
            encript_text_window, values=priv_key_drop_drown_values
        )
        self.privet_key_drop_drown.place(x=170, y=250, width=296)

        receiver_public_key_lebel = tk.Label(
            encript_text_window,
            text="Select Receiver Public Key:",
            foreground=con.INPUT_LABEL_TEXT_COLOR,
            background=con.WINDOWS_BACKGROUNG_COLOR,
        )
        receiver_public_key_lebel.place(x=20, y=286)

        self.public_key_drop_drown = ttk.Combobox(
            encript_text_window, values=pub_key_drop_drown_values
        )
        self.public_key_drop_drown.place(x=170, y=286, width=296)
        # END DROPDOWN LIST

        output_text_label = tk.Label(
            encript_text_window,
            font=("Arial", 9),
            text="Open Output File Directory:",
            foreground=con.INPUT_LABEL_TEXT_COLOR,
            background=con.WINDOWS_BACKGROUNG_COLOR,
        )
        output_text_label.place(x=20, y=322)

        self.show_output_folder_path_textbox = tk.Entry(
            encript_text_window, font=("Arial", 10)
        )
        self.show_output_folder_path_textbox.place(x=20, y=344, width=385, height=25)

        browse_output_directory = tk.Button(
            encript_text_window,
            text="Browse",
            background=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=lambda: self.open_directory(self.show_output_folder_path_textbox),
        )
        browse_output_directory.place(x=415, y=344, width=58)

        encrtption_text_button = tk.Button(
            encript_text_window,
            text="Encryption Text",
            pady=5,
            background=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=presenter.validation_encryption_text,
        )
        encrtption_text_button.place(x=95, y=400, width=300)

        close_window_button = tk.Button(
            encript_text_window,
            text="Close",
            padx=10,
            pady=5,
            background=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=lambda: encript_text_window.destroy(),
        )
        close_window_button.place(x=410, y=400)

    def EncryptFile(self, presenter: Presenter) -> None:
        encript_file_window = tk.Toplevel(self)
        encript_file_window.geometry("500x340")
        encript_file_window.resizable(width=False, height=False)
        encript_file_window.title("Encript File")
        encript_file_window.config(bg=con.WINDOWS_BACKGROUNG_COLOR)
        encript_file_window.grab_set()

        # BEGINING FILE INPUT DILOGBOX
        text_label = tk.Label(
            encript_file_window,
            font=("Arial", 9),
            text="Open Input File:",
            foreground=con.INPUT_LABEL_TEXT_COLOR,
            background=con.WINDOWS_BACKGROUNG_COLOR,
        )
        text_label.place(x=20, y=29)

        self.show_input_file_path = tk.Entry(encript_file_window, font=("Arial", 10))
        self.show_input_file_path.place(x=20, y=50, width=390, height=25)

        browse_file_button = tk.Button(
            encript_file_window,
            text="Browse",
            background=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=lambda: self.open_all_file(self.show_input_file_path),
        )
        browse_file_button.place(x=415, y=50, width=60)
        # END FILE INPUT DILOGBOX

        # BEGINING DROPDOWN LIST
        priv_keys_drop_drown_values = presenter.get_private_key_id_and_folder_name()
        pub_keys_drop_drown_values = presenter.get_public_key_id_and_folder_name()

        private_key_lebel = tk.Label(
            encript_file_window,
            text="Select Your Private Key:",
            foreground=con.INPUT_LABEL_TEXT_COLOR,
            background=con.WINDOWS_BACKGROUNG_COLOR,
        )
        private_key_lebel.place(x=20, y=100)

        self.privet_key_drop_drown = ttk.Combobox(
            encript_file_window, values=priv_keys_drop_drown_values
        )
        self.privet_key_drop_drown.place(x=170, y=100, width=304)

        receiver_public_key_lebel = tk.Label(
            encript_file_window,
            text="Select Receiver Public Key:",
            foreground=con.INPUT_LABEL_TEXT_COLOR,
            background=con.WINDOWS_BACKGROUNG_COLOR,
        )
        receiver_public_key_lebel.place(x=20, y=150)

        self.public_key_drop_drown = ttk.Combobox(
            encript_file_window, values=pub_keys_drop_drown_values
        )
        self.public_key_drop_drown.place(x=170, y=150, width=304)
        # END DROPDOWN LIST

        output_folder_label = tk.Label(
            encript_file_window,
            font=("Arial", 9),
            text="Open Output Directory:",
            foreground=con.INPUT_LABEL_TEXT_COLOR,
            background=con.WINDOWS_BACKGROUNG_COLOR,
        )
        output_folder_label.place(x=20, y=200)

        self.show_output_folder_path = tk.Entry(encript_file_window, font=("Arial", 10))
        self.show_output_folder_path.place(x=20, y=220, width=385, height=25)

        browse_output_directory = tk.Button(
            encript_file_window,
            text="Browse",
            background=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=lambda: self.open_directory(self.show_output_folder_path),
        )
        browse_output_directory.place(x=415, y=220, width=58)

        encrtption_text_button = tk.Button(
            encript_file_window,
            text="Encryption File",
            pady=5,
            background=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=presenter.validation_encryption_file,
        )
        encrtption_text_button.place(x=95, y=280, width=300)

        close_window_button = tk.Button(
            encript_file_window,
            text="Close",
            padx=10,
            pady=5,
            background=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=lambda: encript_file_window.destroy(),
        )
        close_window_button.place(x=410, y=280)

    def EncryptFoulder(self, presenter: Presenter) -> None:
        encrypt_folder_window = tk.Toplevel(self)
        encrypt_folder_window.geometry("500x340")
        encrypt_folder_window.resizable(width=False, height=False)
        encrypt_folder_window.title("Encript Files From Folder")
        encrypt_folder_window.config(bg=con.WINDOWS_BACKGROUNG_COLOR)
        encrypt_folder_window.grab_set()

        # BEGINING FILE INPUT DILOGBOX
        text_label = tk.Label(
            encrypt_folder_window,
            font=("Arial", 9),
            text="Open Input Folder:",
            foreground=con.INPUT_LABEL_TEXT_COLOR,
            background=con.WINDOWS_BACKGROUNG_COLOR,
        )
        text_label.place(x=20, y=29)

        self.show_input_folder_path = tk.Entry(
            encrypt_folder_window, font=("Arial", 10)
        )
        self.show_input_folder_path.place(x=20, y=50, width=390, height=25)

        browse_file_button = tk.Button(
            encrypt_folder_window,
            text="Browse",
            background=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=lambda: self.open_directory(self.show_input_folder_path),
        )
        browse_file_button.place(x=415, y=50, width=60)
        # END FILE INPUT DILOGBOX

        # BEGINING DROPDOWN LIST
        priv_keys_drop_drown_values = presenter.get_private_key_id_and_folder_name()
        pub_keys_drop_drown_values = presenter.get_public_key_id_and_folder_name()

        private_key_lebel = tk.Label(
            encrypt_folder_window,
            text="Select Your Private Key:",
            foreground=con.INPUT_LABEL_TEXT_COLOR,
            background=con.WINDOWS_BACKGROUNG_COLOR,
        )
        private_key_lebel.place(x=20, y=100)

        self.privet_key_drop_drown = ttk.Combobox(
            encrypt_folder_window, values=priv_keys_drop_drown_values
        )
        self.privet_key_drop_drown.place(x=170, y=100, width=304)

        receiver_public_key_lebel = tk.Label(
            encrypt_folder_window,
            text="Select Receiver Public Key:",
            foreground=con.INPUT_LABEL_TEXT_COLOR,
            background=con.WINDOWS_BACKGROUNG_COLOR,
        )
        receiver_public_key_lebel.place(x=20, y=150)

        self.public_key_drop_drown = ttk.Combobox(
            encrypt_folder_window, values=pub_keys_drop_drown_values
        )
        self.public_key_drop_drown.place(x=170, y=150, width=304)
        # END DROPDOWN LIST

        output_text_label = tk.Label(
            encrypt_folder_window,
            font=("Arial", 9),
            text="Open Output File Directory:",
            foreground=con.INPUT_LABEL_TEXT_COLOR,
            background=con.WINDOWS_BACKGROUNG_COLOR,
        )
        output_text_label.place(x=20, y=200)

        self.show_output_folder_path = tk.Entry(
            encrypt_folder_window, font=("Arial", 10)
        )
        self.show_output_folder_path.place(x=20, y=220, width=385, height=25)

        browse_output_directory = tk.Button(
            encrypt_folder_window,
            text="Browse",
            background=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=lambda: self.open_directory(self.show_output_folder_path),
        )
        browse_output_directory.place(x=415, y=220, width=58)

        encrypt_folder_button = tk.Button(
            encrypt_folder_window,
            text="Encryption Folder",
            pady=5,
            background=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=presenter.validation_encryption_folder,
        )
        encrypt_folder_button.place(x=95, y=280, width=300)

        close_window_button = tk.Button(
            encrypt_folder_window,
            text="Close",
            padx=10,
            pady=5,
            background=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=lambda: encrypt_folder_window.destroy(),
        )
        close_window_button.place(x=410, y=280)

    def DecryptFile(self, presenter: Presenter) -> None:
        decrypt_file_window = tk.Toplevel(self)
        decrypt_file_window.geometry("500x340")
        decrypt_file_window.resizable(width=False, height=False)
        decrypt_file_window.title("Decript File")
        decrypt_file_window.config(bg=con.WINDOWS_BACKGROUNG_COLOR)
        decrypt_file_window.grab_set()

        # BEGINING FILE INPUT DILOGBOX
        text_label = tk.Label(
            decrypt_file_window,
            font=("Arial", 9),
            text="Open Encryption File:",
            foreground=con.INPUT_LABEL_TEXT_COLOR,
            background=con.WINDOWS_BACKGROUNG_COLOR,
        )
        text_label.place(x=20, y=29)

        self.show_input_file_path = tk.Entry(decrypt_file_window, font=("Arial", 10))
        self.show_input_file_path.place(x=20, y=50, width=390, height=25)

        browse_file_butt = tk.Button(
            decrypt_file_window,
            text="Browse",
            background=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=lambda: self.open_specific_file(
                self.show_input_file_path, [("Encryption file", "*.enc")]
            ),
        )
        browse_file_butt.place(x=415, y=50, width=60)
        # END FILE INPUT DILOGBOX

        # BEGINING DROPDOWN LIST
        pub_keys_drop_drown_values = presenter.get_public_key_id_and_folder_name()
        priv_keys_drop_drown_values = presenter.get_private_key_id_and_folder_name()

        private_key_lebel = tk.Label(
            decrypt_file_window,
            text="Select Your Private Key:",
            foreground=con.INPUT_LABEL_TEXT_COLOR,
            background=con.WINDOWS_BACKGROUNG_COLOR,
        )
        private_key_lebel.place(x=20, y=100)

        self.privet_key_drop_drown = ttk.Combobox(
            decrypt_file_window, values=priv_keys_drop_drown_values
        )
        self.privet_key_drop_drown.place(x=170, y=100, width=304)

        self.receiver_public_key_lebel = tk.Label(
            decrypt_file_window,
            text="Select Receiver Public Key:",
            foreground=con.INPUT_LABEL_TEXT_COLOR,
            background=con.WINDOWS_BACKGROUNG_COLOR,
        )
        self.receiver_public_key_lebel.place(x=20, y=150)

        self.public_key_drop_drown = ttk.Combobox(
            decrypt_file_window, values=pub_keys_drop_drown_values
        )
        self.public_key_drop_drown.place(x=170, y=150, width=304)
        # END DROPDOWN LIST

        output_file_text_label = tk.Label(
            decrypt_file_window,
            font=("Arial", 9),
            text="Open Output File Directory:",
            foreground=con.INPUT_LABEL_TEXT_COLOR,
            background=con.WINDOWS_BACKGROUNG_COLOR,
        )
        output_file_text_label.place(x=20, y=200)

        self.show_output_folder_path = tk.Entry(decrypt_file_window, font=("Arial", 10))
        self.show_output_folder_path.place(x=20, y=220, width=385, height=25)

        browse_output_directory = tk.Button(
            decrypt_file_window,
            text="Browse",
            background=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=lambda: self.open_directory(self.show_output_folder_path),
        )
        browse_output_directory.place(x=415, y=220, width=58)

        decrypt_file_button = tk.Button(
            decrypt_file_window,
            text="Decryption File",
            background=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            pady=5,
            # command=presenter.validation_encryption_folder
            command=presenter.validation_decryption_file,
        )
        decrypt_file_button.place(x=95, y=280, width=300)

        close_window_button = tk.Button(
            decrypt_file_window,
            text="Close",
            padx=10,
            pady=5,
            background=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=lambda: decrypt_file_window.destroy(),
        )
        close_window_button.place(x=410, y=280)

    def DecryptFoulder(self, presenter: Presenter) -> None:
        decrypt_folder_window = tk.Toplevel(self)
        decrypt_folder_window.geometry("500x340")
        decrypt_folder_window.resizable(width=False, height=False)
        decrypt_folder_window.title("Decript File From Folder")
        decrypt_folder_window.config(bg=con.WINDOWS_BACKGROUNG_COLOR)
        decrypt_folder_window.grab_set()

        # BEGINING FILE INPUT DILOGBOX
        text_label = tk.Label(
            decrypt_folder_window,
            font=("Arial", 9),
            text="Open Encript Files Folder:",
            foreground=con.INPUT_LABEL_TEXT_COLOR,
            background=con.WINDOWS_BACKGROUNG_COLOR,
        )
        text_label.place(x=20, y=29)

        self.show_input_folder_path = tk.Entry(
            decrypt_folder_window, font=("Arial", 10)
        )
        self.show_input_folder_path.place(x=20, y=50, width=390, height=25)

        browse_file_butt = tk.Button(
            decrypt_folder_window,
            text="Browse",
            background=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=lambda: self.open_directory(self.show_input_folder_path),
        )
        browse_file_butt.place(x=415, y=50, width=60)
        # END FILE INPUT DILOGBOX

        # BEGINING DROPDOWN LIST
        priv_keys_drop_drown_values = presenter.get_private_key_id_and_folder_name()
        pub_keys_drop_drown_values = presenter.get_public_key_id_and_folder_name()

        private_key_lebel = tk.Label(
            decrypt_folder_window,
            text="Select your private key:",
            foreground=con.INPUT_LABEL_TEXT_COLOR,
            background=con.WINDOWS_BACKGROUNG_COLOR,
        )
        private_key_lebel.place(x=20, y=100)

        self.privet_key_drop_drown = ttk.Combobox(
            decrypt_folder_window, values=priv_keys_drop_drown_values
        )
        self.privet_key_drop_drown.place(x=170, y=100, width=304)

        receiver_public_key_lebel = tk.Label(
            decrypt_folder_window,
            text="Select Receiver Public Key:",
            foreground=con.INPUT_LABEL_TEXT_COLOR,
            background=con.WINDOWS_BACKGROUNG_COLOR,
        )
        receiver_public_key_lebel.place(x=20, y=150)

        self.public_key_drop_drown = ttk.Combobox(
            decrypt_folder_window, values=pub_keys_drop_drown_values
        )
        self.public_key_drop_drown.place(x=170, y=150, width=304)
        # END DROPDOWN LIST

        output_text_label = tk.Label(
            decrypt_folder_window,
            font=("Arial", 9),
            text="Open Output File Directory:",
            foreground=con.INPUT_LABEL_TEXT_COLOR,
            background=con.WINDOWS_BACKGROUNG_COLOR,
        )
        output_text_label.place(x=20, y=200)

        self.show_output_folder_path = tk.Entry(
            decrypt_folder_window, font=("Arial", 10)
        )
        self.show_output_folder_path.place(x=20, y=220, width=385, height=25)

        browse_output_directory = tk.Button(
            decrypt_folder_window,
            text="Browse",
            background=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=lambda: self.open_directory(self.show_output_folder_path),
        )
        browse_output_directory.place(x=415, y=220, width=58)

        decrypt_folder_button = tk.Button(
            decrypt_folder_window,
            text="Decryption Files From Folder",
            pady=5,
            background=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=presenter.validation_decryption_folder,
        )
        decrypt_folder_button.place(x=95, y=280, width=300)

        close_window_button = tk.Button(
            decrypt_folder_window,
            text="Close",
            padx=10,
            pady=5,
            background=con.BUTTON_BACKGROUND_COLOR,
            foreground=con.BUTTON_TEXT_COLOR,
            relief="groove",
            borderwidth=4,
            command=lambda: decrypt_folder_window.destroy(),
        )
        close_window_button.place(x=410, y=280)

    def lodingWindow(self, massage: str, target: object) -> None:
        """Loding Window"""
        self.loding_window = tk.Toplevel(self)
        self.loding_window.geometry("400x200")
        self.loding_window.resizable(width=False, height=False)
        self.loding_window.title("Genrateing Keys....")
        self.loding_window.config(bg=con.WINDOWS_BACKGROUNG_COLOR)
        self.loding_window.grab_set()

        massage_text = tk.Label(
            self.loding_window,
            text=massage,
            font=("Arial", 15, "bold"),
            foreground=con.INPUT_LABEL_TEXT_COLOR,
            background=con.WINDOWS_BACKGROUNG_COLOR,
        )
        massage_text.pack(pady=40)

        self.loding_progressber = ttk.Progressbar(
            self.loding_window, orient="horizontal", length=100, mode="determinate"
        )
        self.loding_progressber.place(x=20, y=100, width=360)

        threading.Thread(target=target).start()

    # Addon Function
    def set_pub_keys_table_data(self, data: list[tuple]) -> None:
        for row in data:
            self.pub_keys_table.insert(parent="", index="end", values=row)

    def set_my_keys_table_data(self, data: list[tuple]) -> None:
        for row in data:
            self.my_keys_table.insert(parent="", index="end", values=row)

    def open_specific_file(
        self,
        textbox: tk.Entry,
        filetypes: list[tuple[str, str | list[str] | tuple[str, ...]]],
        initialdir: str = None,
    ) -> None:
        """Set open specific file path to entry box."""
        open_file = filedialog.askopenfile(
            initialdir=initialdir, mode="r", filetypes=filetypes
        )
        if open_file:
            textbox.delete(0, "end")
            textbox.insert(0, open_file.name)

    def open_all_file(self, textbox: tk.Entry) -> None:
        """Set open specific file path to entry box."""
        open_file = filedialog.askopenfile(
            mode="r",
        )
        if open_file:
            textbox.delete(0, "end")
            textbox.insert(0, open_file.name)

    def open_directory(self, textbox: tk.Entry) -> None:
        """Open foulder"""
        folder = filedialog.askdirectory(title="Open output folder")
        if len(str(folder).strip()) != 0:
            textbox.delete(0, "end")
            textbox.insert(0, folder)

    # Messagebox
    def error_messagebox(self, title: str, massage: str) -> None:
        messagebox.showerror(title, massage)

    def info_messagebox(self, title: str, massage: str) -> None:
        messagebox.showinfo(title, massage)

    def askyesno_messagebox(self, title: str, massage: str) -> None:
        return messagebox.askyesno(title, massage)
