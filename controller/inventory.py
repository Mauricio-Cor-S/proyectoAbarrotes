from datetime import date
from models.product import product
import models.sqlite3_save as ss
import controller.user_errors as ue
from decimal import Decimal
import json
from models.update_income import upd_income, retrieve_income
import models.parse_validation as pv


class Inventory():
    def __init__(self):
        self.__inventory = {}
        self.__income = retrieve_income()
        self.load_inventory()
    @property
    def income(self):
        return self.__income

    def by_id(self, id_num):
        return self.__inventory.get(id_num)
        #None = no existe

    def list_product(self,id_num):
        i= self.by_id(id_num)
        if i == None:
            raise ue.ProductDoesntExist()
        return  (
                    id_num,
                    i.barcode,
                    i.name,
                    i.description,
                    i.price,
                    i.selling_price,
                    i.category
                )

    def list_products(self):
        products = []
        for id_num, i in self.__inventory.items():
            products.append({
                            "id_num": id_num, ###CORREGIR :( Ya quedó
                            "barcode":i.barcode,
                            "name":i.name,
                            "description":i.description,
                            "price":i.price,
                            "selling_price":i.selling_price,
                            "category":i.category})
        return products


    def add_product(self, id_num, barcode, name, description, price, selling_price, category):
        if id_num in self.__inventory:
            raise ue.ProductDoesExist()
        current = product(barcode, name, description, price, selling_price, category)
        #add
        self.__inventory[id_num] = current
        ss.SaveInventory().log(id_num,current.barcode,current.name,current.description,
        current.price,current.selling_price,current.expiry,current.category)

    
    
    def delete_product(self, id_num):
        i = self.by_id(id_num)
        if i == None:
            raise ue.ProductDoesntExist()
        elif i.amount() != 0:
            raise ue.InventoryRemaining()
        #delete
        ss.SaveTransaction().log("DELETE",id_num,i.name,"",0,0,str(self.__income))
        del self.__inventory[id_num]
        ss.SaveInventory().delete_product(id_num)

    def sell(self, amount, id_num):

        current = self.by_id(id_num)

        if current is None:
            raise ue.ProductDoesntExist()

        current.subtract(amount)

        self.__income += (
            current.selling_price * Decimal(amount)
        )

        upd_income(str(self.__income))

        self.save_product(id_num)

        ss.SaveTransaction().log("SELL",id_num,current.name,"",amount,current.amount(),str(self.__income))

    def trash(self, amount, id_num, expiry=None):
        current = self.by_id(id_num)

        if current is None:
            raise ue.ProductDoesntExist()

        current.subtract(amount, expiry)
        self.save_product(id_num)

        ss.SaveTransaction().log("TRASH",id_num,current.name,expiry.isoformat() if expiry else "",amount,
            current.amount(),str(self.__income))
        return

    def change_income(self,income_change):
        self.__income += income_change
        upd_income(str(self.__income))

    def load_inventory(self):

        rows = ss.SaveInventory().load_all()

        for row in rows:

            (
                product_id,
                barcode,
                product_name,
                description,
                price,
                selling_price,
                expiry_json,
                category
            ) = row

            current_product = product(
                barcode,
                product_name,
                description,
                Decimal(price),
                Decimal(selling_price),
                category
            )

            current_product.expiry = pv.json_to_expiry(expiry_json)

            self.__inventory[product_id] = current_product

    def add_stock(self, id_num, amount, expiry):

        current = self.by_id(id_num)

        if current is None:
            raise ue.ProductDoesntExist()

        current.add(amount, expiry)

        self.save_product(id_num)

        ss.SaveTransaction().log(
            "RESTOCK",
            id_num,
            current.name,
            expiry.isoformat(),
            amount,
            current.amount(),
            str(self.__income)
        )

    def save_product(self, id_num):

        current = self.by_id(id_num)

        if current is None:
            raise ue.ProductDoesntExist()

        ss.SaveInventory().replace(id_num,current.barcode,current.name,current.description,current.price,
            current.selling_price,current.expiry,current.category
        )

    def trash_expired(self, id_num):
        current = self.by_id(id_num)

        if current is None:
            raise ue.ProductDoesntExist()

        expired_amount = current.delete_expired()

        if expired_amount > 0:
            ss.SaveTransaction().log("TRASH", id_num, current.name, "expired", expired_amount, current.amount(), str(self.__income))

        self.save_product(id_num)