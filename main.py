from controller.inventory import Inventory
from view.app import App

Inventory_main = Inventory
App_main = App(Inventory_main)
App_main.mainloop()