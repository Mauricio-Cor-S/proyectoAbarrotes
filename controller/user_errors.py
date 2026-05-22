from abc import ABC, abstractmethod
#Importar con:
#import controller.user_errors as ue

class DumbUser(Exception,ABC):
    def __init__(self,msg=None):
        self._msg = msg
        super().__init__(msg or self.error_msg)

    def __str__(self):
        return self._msg or self.error_msg

    @property
    @abstractmethod
    def error_msg(self):
        pass

#Plantilla
'''
class errors(DumbUser):
    def error_msg(self):
        return ""

'''

class ProductDoesntExist(DumbUser):
    @property
    def error_msg(self):
        return "El producto no existe, intente de nuevo"

class ProductDoesExist(DumbUser):
    @property
    def error_msg(self):
        return "El producto ya existe. Intente de nuevo"

class InventoryRemaining(DumbUser):
    @property
    def error_msg(self):
        return "Aún quedan productos en el inventario, elimínelos para proceder."

class InvalidNumber(DumbUser):
    @property
    def error_msg(self):
        return "El número ingresado es inválido. Intente de nuevo."

class InvalidDate(DumbUser):
    @property
    def error_msg(self):
        return "La fecha ingresada es inválida. Intente de nuevo."

class ExpiryDoesntExist(DumbUser):
    @property
    def error_msg(self):
        return "La fecha insertada no existe. Intente de nuevo."

class ExpiryInsufficient(DumbUser):
    @property
    def error_msg(self):
        return "No existe suficiente producto en esa fecha para realizar la operacion. Intente de nuevo."

class StockInsufficient(DumbUser):
    @property
    def error_msg(self):
        return "No cuenta con mercancía suficiente. Intente de nuevo."

class MissingField(DumbUser):
    @property
    def error_msg(self):
        return "Falta un campo requerido. Intente de nuevo."
