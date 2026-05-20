import sqlite3
from pathlib import Path
from datetime import datetime
import sys
import models.parse_validation as pv

if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

DB_INVENTORY = BASE_DIR / "data" / "sqlite" / "inventory.db"
DB_TRANSACTION = BASE_DIR / "data" / "sqlite" / "transactions.db"

DB_INVENTORY.parent.mkdir(parents=True, exist_ok=True)
DB_TRANSACTION.parent.mkdir(parents=True, exist_ok=True)

class Database():
    def __init__(self, db_path):
        self.__connection = sqlite3.connect(str(db_path))
        self.__cursor = self.__connection.cursor()
    def execute(self, query, parameters=()):
        self.__cursor.execute(query, parameters)
    def fetch_all(self):
        return self.__cursor.fetchall()
    def commit(self):
        self.__connection.commit()
    def close(self):
        self.__connection.close()

class SaveInventory():
    def __init__(self):
        self.db = Database(DB_INVENTORY)
        self.__create_table()

    def __create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS inventory (
        product_id TEXT PRIMARY KEY,
        barcode TEXT,
        product_name TEXT,
        description TEXT,
        price TEXT,
        selling_price TEXT,
        expiry_json TEXT,
        category TEXT
        )
        """
        #self.db.execute(query)
        #self.db.commit()
        self.db.execute(query)
        self.db.commit()

    def log(self, product_id, barcode, product_name, description, price_dec, selling_price_dec, expiry, category):
        price = str(price_dec)
        selling_price = str(selling_price_dec)
        expiry_json = pv.expiry_to_json(expiry)
        query = """
        INSERT INTO inventory (
        product_id, barcode, product_name, description, price, selling_price, expiry_json, category
        ) VALUES (?,?,?,?,?,?,?,?)
        """
        parameters = (
            product_id, barcode, product_name, description, price, selling_price, expiry_json, category
        )
        self.db.execute(query, parameters)
        self.db.commit()
        self.db.close()

    def replace(self, product_id, barcode, product_name, description, price_dec, selling_price_dec, expiry, category):
        query = """
        UPDATE inventory SET
        barcode=?,
        product_name=?,
        description=?,
        price=?,
        selling_price=?,
        expiry_json=?,
        category=?
        WHERE product_id = ?
        """
        parameters = (
            barcode,
            product_name,
            description,
            str(price_dec),
            str(selling_price_dec),
            pv.expiry_to_json(expiry),
            category,
            product_id
        )
        self.db.execute(query, parameters)
        self.db.commit()
        self.db.close()

    def delete_product(self, product_id):
        query = """
        DELETE FROM inventory WHERE product_id = ?
        """
        parameters = (product_id,)
        self.db.execute(query, parameters)
        self.db.commit()
        self.db.close()

    def load_all(self):
        query = """
        SELECT
        product_id,
        barcode,
        product_name,
        description,
        price,
        selling_price,
        expiry_json,
        category
        FROM inventory
        """
        self.db.execute(query)
        result = self.db.fetch_all()
        self.db.close()
        return result

class SaveTransaction():
    def __init__(self):
        self.db = Database(DB_TRANSACTION)
        self.__create_table()

    def __create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        type_transaction TEXT,
        product_id TEXT,
        product_name TEXT,
        expiry_date TEXT,
        product_change_amount INTEGER,
        new_stock INTEGER,
        new_income TEXT
        )
        """
        self.db.execute(query)
        self.db.commit()


    def log(self, type_transaction, product_id, product_name, expiry_date, product_change_amount, new_stock, new_income):
        query = """
        INSERT INTO transactions (
        timestamp, type_transaction, product_id, product_name, expiry_date, product_change_amount, new_stock, new_income
        ) VALUES (?,?,?,?,?,?,?,?)
        """
        parameters = (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            type_transaction,
            product_id,
            product_name,
            expiry_date,
            product_change_amount,
            new_stock,
            new_income
        )
        self.db.execute(query, parameters)
        self.db.commit()
        self.db.close()