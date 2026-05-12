from datetime import date, datetime
import controller.user_errors as ue
import models.parse_validation as pv 
from decimal import Decimal

class product():
    def __init__(self, barcode, name, description, price, selling_price, category):
        self.__barcode = barcode
        self.__name = name
        self.__description = description
        self.__price = Decimal(price)
        self.__selling_price = Decimal(selling_price)
        self.expiry = {}
        self.category = category
    #setters

    @property
    def barcode(self):
        return self.__barcode

    @barcode.setter
    def barcode(self,barcode):
        self.__barcode = barcode

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self,name):
        self.__name = name

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self,description):
        self.__description = description

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self,price):
        self.__price = price

    @property
    def selling_price(self):
        return self.__selling_price

    @selling_price.setter
    def selling_price(self,selling_price):
        self.__selling_price = selling_price

    #methods
    def delete_expired(self):
        total = 0
        for i in list(self.expiry):
            if i < date.today():
                total += self.expiry[i]
                del self.expiry[i]
        return total

    def amount(self):
        amount = 0
        for quantity in self.expiry.values():
            amount += quantity
        return amount

    def add(self,amount,add_expiry):
        if add_expiry in self.expiry:
            self.expiry[add_expiry] = self.expiry[add_expiry] + amount
        else:
            self.expiry[add_expiry] = amount

    def total_price(self, amount):
        return self.__selling_price * amount


    
    def expiry_amount(self):
        amount = 0
        for i in list(self.expiry):
            if i < date.today():
                amount +=1
        return amount
    
    def subtract(self, amount, expiry=None):

        if amount <= 0:
            # ERROR: cantidad inválida
            raise ue.InvalidNumber("Su número no puede ser igual a cero o menor. Intente de nuevo.")

        if expiry is None:

            if amount > self.amount():
                # ERROR: stock insuficiente
                raise ue.StockInsufficient()

            left = amount

            for d in sorted(list(self.expiry)):
                qty = self.expiry[d]

                if left <= qty:
                    self.expiry[d] -= left
                    if self.expiry[d] == 0:
                        del self.expiry[d]
                    break
                else:
                    left -= qty
                    del self.expiry[d]

        else:
            qty = self.expiry.get(expiry)

            if qty is None:
                raise ue.ExpiryDoesntExist()
                return

            if amount > qty:
                raise ue.ExpiryInsufficient()
                return

            self.expiry[expiry] -= amount

            if self.expiry[expiry] == 0:
                del self.expiry[expiry]

