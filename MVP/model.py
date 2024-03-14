import sqlite3
import pathlib
from configuration import DATABASE_DIRECTORY


class Model:
    def __init__(self) -> None:
        self._db_file_path = pathlib.Path(DATABASE_DIRECTORY).joinpath("CRIPTO50.db")

        self._con = sqlite3.connect(self._db_file_path, check_same_thread=False)
        self._cur = self._con.cursor()
        self._cur.execute(
            """
                CREATE TABLE IF NOT EXISTS my_keys 
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    folder_name TEXT,
                    date_string TEXT,
                    total_encryption_file_no INT,
                    key_folder_path TEXT
                )
            """
        )

        self._con.commit()

        self._cur.execute(
            """
                CREATE TABLE IF NOT EXISTS public_keys 
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key_owner_name TEXT,
                    date_string TEXT,
                    key_folder_name TEXT,
                    key_folder_path TEXT
                )
            """
        )
        self._con.commit()

    def insert_my_key_data(self, data: dict) -> None:
        with self._con:
            self._cur.execute(
                "INSERT INTO my_keys VALUES (:id, :folder_name, :date_string, :total_encryption_file_no, :key_folder_path)",
                data,
            )

        self._con.commit()

    def get_my_keys_data(self) -> list[tuple]:
        with self._con:
            self._cur.execute("""SELECT * FROM my_keys""")
            data = self._cur.fetchall()

        return data

    def get_last_row_from_my_key(self) -> tuple:
        with self._con:
            self._cur.execute("""SELECT * FROM my_keys""")
            data = self._cur.fetchall()

        if len(data) == 0:
            return tuple()
        return data[len(data) - 1]

    def del_my_keys_table_data(self, id: int) -> None:
        with self._con:
            self._cur.execute("DELETE from my_keys WHERE id = :id", {"id": id})
        self._con.commit()

    def update_total_encryption_file_no_from_my_key(self, id: int, value: str) -> None:
        with self._con:
            self._cur.execute(
                "UPDATE my_keys SET total_encryption_file_no = :total_encryption_file_no WHERE id = :id",
                {"id": id, "total_encryption_file_no": value},
            )
        self._con.commit()

    def get_pub_keys_data(self) -> list[tuple]:
        with self._con:
            self._cur.execute("""SELECT * FROM public_keys""")
            data = self._cur.fetchall()

        return data

    def insert_pub_key_data(self, data: dict) -> None:
        with self._con:
            self._cur.execute(
                "INSERT INTO public_keys VALUES (:id, :key_owner_name, :date_string, :key_folder_name, :key_folder_path)",
                data,
            )

        self._con.commit()

    def del_pub_keys_table_data(self, id: int) -> None:
        with self._con:
            self._cur.execute("DELETE from public_keys WHERE id = :id", {"id": id})
        self._con.commit()

    def get_last_row_from_pub(self) -> tuple:
        with self._con:
            self._cur.execute("""SELECT * FROM public_keys""")
            data = self._cur.fetchall()
        if len(data) == 0:
            return tuple()
        return data[len(data) - 1]

    def update_pub_keys_data(self, data: dict) -> None:
        with self._con:
            self._cur.execute(
                "UPDATE public_keys SET key_owner_name = :key_owner_name, date_string = :date_string, key_folder_name = :key_folder_name, key_folder_path = :key_folder_path WHERE id = :id",
                data,
            )
        self._con.commit()

    def get_id_and_folder_name_from_private_keys(self) -> list[tuple]:
        with self._con:
            self._cur.execute("""SELECT id, folder_name FROM my_keys""")
            data = self._cur.fetchall()
        return data

    def get_id_and_folder_name_from_public_keys(self) -> list[tuple]:
        with self._con:
            self._cur.execute("""SELECT id, key_folder_name FROM public_keys""")
            data = self._cur.fetchall()
        return data

    def find_private_key_by_id(self, id: int) -> list[tuple]:
        with self._con:
            self._cur.execute("SELECT * FROM my_keys WHERE id = :id", {"id": id})
            data = self._cur.fetchall()
        return data

    def find_public_key_by_id(self, id: int) -> list[tuple]:
        with self._con:
            self._cur.execute("SELECT * FROM public_keys WHERE id = :id", {"id": id})
            data = self._cur.fetchall()
        return data

    def close_connection(self) -> None:
        self._con.close()
