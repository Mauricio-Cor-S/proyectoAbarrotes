import customtkinter as ctk
from tkinter import messagebox as mb
import controller.user_errors as ue
from decimal import Decimal
from models.parse_validation import validate_cur, parse_date


class App(ctk.CTk):

    def __init__(self, inventory_class):
        super().__init__()

        self.title("Sistema de Inventario - Abarrotes el güero moreno")
        self.geometry("900x1000") 
        self.resizable(False, False)

        self.inventory = inventory_class()

        self.create_widgets()
        self.refresh_inventory()

    def create_widgets(self):

        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.pack(fill="x", padx=10, pady=10)
        self.title_label = ctk.CTkLabel(self.top_frame, text="Inventario")
        self.title_label.pack(side="left")
        self.income_label = ctk.CTkLabel(self.top_frame, text="Ingresos: 0")
        self.income_label.pack(side="right")
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.left_frame = ctk.CTkFrame(self.main_frame)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=5) ########
        self.right_frame = ctk.CTkFrame(self.main_frame)
        self.right_frame.pack(side="right", fill="y", padx=(10, 0), pady=5)
        self.inventory_text = ctk.CTkTextbox(self.left_frame,width=560,height=420, state="disabled")
        self.inventory_text.pack(fill="both", expand=True)
        self.button_frame = ctk.CTkFrame(self.left_frame)
        self.button_frame.pack(fill="x", pady=(10, 0))
        self.refresh_button = ctk.CTkButton(self.button_frame,text="Actualizar lista",command=self.refresh_inventory)
        self.refresh_button.pack(side="left", padx=5, pady=5)
        self.clear_button = ctk.CTkButton(self.button_frame,text="Limpiar campos",command=self.clear_form)
        self.clear_button.pack(side="left", padx=5, pady=5)
        self.message_label = ctk.CTkLabel(self.right_frame,text="",wraplength=280,justify="left")
        self.message_label.pack(fill="x", pady=(0, 10))
        self.id_label = ctk.CTkLabel(self.right_frame, text="ID")
        self.id_label.pack(anchor="w", pady=(5, 0))
        self.id_entry = ctk.CTkEntry(self.right_frame, width=280)
        self.id_entry.pack(fill="x", pady=(2, 5))
        self.barcode_label = ctk.CTkLabel(self.right_frame, text="Código de barras")
        self.barcode_label.pack(anchor="w", pady=(5, 0))
        self.barcode_entry = ctk.CTkEntry(self.right_frame, width=280)
        self.barcode_entry.pack(fill="x", pady=(2, 5))
        self.name_label = ctk.CTkLabel(self.right_frame, text="Nombre")
        self.name_label.pack(anchor="w", pady=(5, 0))
        self.name_entry = ctk.CTkEntry(self.right_frame, width=280)
        self.name_entry.pack(fill="x", pady=(2, 5))
        self.description_label = ctk.CTkLabel(self.right_frame, text="Descripción")
        self.description_label.pack(anchor="w", pady=(5, 0))
        self.description_entry = ctk.CTkEntry(self.right_frame, width=280)
        self.description_entry.pack(fill="x", pady=(2, 5))
        self.price_label = ctk.CTkLabel(self.right_frame, text="Precio")
        self.price_label.pack(anchor="w", pady=(5, 0))
        self.price_entry = ctk.CTkEntry(self.right_frame, width=280)
        self.price_entry.pack(fill="x", pady=(2, 5))
        self.selling_price_label = ctk.CTkLabel(self.right_frame, text="Precio de venta")
        self.selling_price_label.pack(anchor="w", pady=(5, 0))
        self.selling_price_entry = ctk.CTkEntry(self.right_frame, width=280)
        self.selling_price_entry.pack(fill="x", pady=(2, 5))
        self.category_label = ctk.CTkLabel(self.right_frame, text="Categoría")
        self.category_label.pack(anchor="w", pady=(5, 0))
        self.category_entry = ctk.CTkEntry(self.right_frame, width=280)
        self.category_entry.pack(fill="x", pady=(2, 5))
        self.amount_label = ctk.CTkLabel(self.right_frame, text="Cantidad")
        self.amount_label.pack(anchor="w", pady=(5, 0))
        self.amount_entry = ctk.CTkEntry(self.right_frame, width=280)
        self.amount_entry.pack(fill="x", pady=(2, 5))
        self.expiry_label = ctk.CTkLabel(self.right_frame, text="Fecha caducidad")
        self.expiry_label.pack(anchor="w", pady=(5, 0))
        self.expiry_entry = ctk.CTkEntry(self.right_frame, width=280)
        self.expiry_entry.pack(fill="x", pady=(2, 5))
        self.action_frame = ctk.CTkFrame(self.right_frame)
        self.action_frame.pack(fill="x", pady=10)
        self.add_button = ctk.CTkButton(self.action_frame,text="Agregar producto",command=self.add_product)
        self.add_button.pack(fill="x", pady=2)
        self.delete_button = ctk.CTkButton(self.action_frame,text="Eliminar producto",command=self.delete_product)
        self.delete_button.pack(fill="x", pady=2)
        self.restock_button = ctk.CTkButton(self.action_frame,text="Agregar stock",command=self.add_stock)
        self.restock_button.pack(fill="x", pady=2)
        self.sell_button = ctk.CTkButton(self.action_frame,text="Vender",command=self.sell_product)
        self.sell_button.pack(fill="x", pady=2)
        self.trash_button = ctk.CTkButton(self.action_frame,text="Desechar",command=self.trash_product)
        self.trash_button.pack(fill="x", pady=2)
        self.trash_expired_button = ctk.CTkButton(self.action_frame,text="Desechar caducados",command=self.trash_expired)
        self.trash_expired_button.pack(fill="x", pady=2)

    def show_message(self, text, error=False):
        message = str(text)

        if error:
            mb.showerror("Error", message, parent=self)
            self.message_label.configure(text=message, text_color="#ff0000")
        else:
            self.message_label.configure(text=message, text_color="#00ffff")

    def clear_form(self):

        self.id_entry.delete(0, "end")
        self.barcode_entry.delete(0, "end")
        self.name_entry.delete(0, "end")
        self.description_entry.delete(0, "end")
        self.price_entry.delete(0, "end")
        self.selling_price_entry.delete(0, "end")
        self.category_entry.delete(0, "end")
        self.amount_entry.delete(0, "end")
        self.expiry_entry.delete(0, "end")
        self.show_message("Campos vaciados.")

    def refresh_inventory(self):

        self.inventory_text.configure(state="normal")
        self.inventory_text.delete("1.0", "end")
        products = self.inventory.list_products()
        self.income_label.configure(text=f"Ingreso: {self.inventory.income}")

        if  products == []:
            self.inventory_text.insert("end","No hay productos registrados.\n")
            self.inventory_text.configure(state="disabled")
            return

        header = "ID | Nombre | Precio venta | Stock | Categoría"

        self.inventory_text.insert("end", header + "\n")
        self.inventory_text.insert("end", "-" * len(header) + "\n")

        for product in products:
            product_obj = self.inventory.by_id(product["id_num"])
            stock = product_obj.amount()
            line = (
                f"{product['id_num']} | "
                f"{product['name']} | "
                f"{product['selling_price']} | "
                f"{stock} | "
                f"{product['category']}\n"
            )

            self.inventory_text.insert("end", line)
            if product_obj.expiry:
                sorted_expiries = sorted(product_obj.expiry.items())
                for expiry_date, amount in sorted_expiries:
                    expiry_line = (f"    {expiry_date.isoformat()} → {amount}\n")

                    self.inventory_text.insert("end", expiry_line)

            else:
                self.inventory_text.insert("end","    Sin fechas de caducidad\n")
        self.inventory_text.configure(state="disabled")

    def parse_price(self, text):
        if text == "":
            raise ue.InvalidNumber()
        return validate_cur(text)
    def parse_amount(self, text):
        if text == "":
            raise ue.InvalidNumber()
        amount = validate_cur(text)
        if amount != amount.quantize(Decimal("1")): #para ver que no tenga decimales
            raise ue.InvalidNumber()
        return int(amount)
    def parse_expiry(self, text):
        text = text.strip()
        if text == "":
            return None
        return parse_date(text)
    def add_product(self):
        try:
            product_id = self.id_entry.get().strip()
            if product_id == "":
                raise ue.InvalidNumber("Falta el ID del producto cabezón.")
            barcode = self.barcode_entry.get().strip()
            name = self.name_entry.get().strip()
            description = self.description_entry.get().strip()
            price = self.parse_price(self.price_entry.get().strip())
            selling_price = self.parse_price(self.selling_price_entry.get().strip())
            category = self.category_entry.get().strip()
            self.inventory.add_product(
                product_id,
                barcode,
                name,
                description,
                price,
                selling_price,
                category
            )

            self.refresh_inventory()

            self.show_message("Producto agregado correctamente.")

        except ue.DumbUser as error:
            self.show_message(error, error=True)

        except Exception as error:
            self.show_message(f"Error: {error}",error=True)

    def delete_product(self):
        try:
            product_id = self.id_entry.get().strip()
            if product_id == "":
                raise ue.InvalidNumber("Falta el ID del producto.")
            self.inventory.delete_product(product_id)
            self.refresh_inventory()
            self.show_message("Producto eliminado.")

        except ue.DumbUser as error:
            self.show_message(error, error=True)

        except Exception as error:
            self.show_message(
                f"Error: {error}",
                error=True
            )

    def add_stock(self):

        try:
            product_id = self.id_entry.get().strip()
            amount = self.parse_amount(self.amount_entry.get().strip())

            expiry = self.parse_expiry(self.expiry_entry.get().strip())

            if expiry is None:
                raise ue.InvalidDate()

            self.inventory.add_stock(product_id,amount,expiry)
            self.refresh_inventory()
            self.show_message("Stock agregado.")
        except ue.DumbUser as error:
            self.show_message(error, error=True)

        except Exception as error:
            self.show_message(f"Error: {error}",error=True )

    def sell_product(self):
        try:
            product_id = self.id_entry.get().strip()
            amount = self.parse_amount(self.amount_entry.get().strip())
            self.inventory.sell(amount,product_id)
            self.refresh_inventory()
            self.show_message("Venta registrada.")
        except ue.DumbUser as error:
            self.show_message(error, error=True)

        except Exception as error:
            self.show_message(f"Error: {error}",error=True)

    def trash_product(self):
        try:
            product_id = self.id_entry.get().strip()
            amount = self.parse_amount(self.amount_entry.get().strip())
            expiry = self.parse_expiry(self.expiry_entry.get().strip())
            self.inventory.trash(amount,product_id,expiry)
            self.refresh_inventory()
            self.show_message("Producto desechado.")

        except ue.DumbUser as error:
            self.show_message(error, error=True)

        except Exception as error:
            self.show_message(f"Error python: {error}",error=True)

    def trash_expired(self):
        try:
            product_id = self.id_entry.get().strip()
            if product_id == "":
                raise ue.InvalidNumber("Falta el ID del producto cabezón.")
            self.inventory.trash_expired(product_id)
            self.refresh_inventory()
            self.show_message("Caducados desechados.")
        except ue.DumbUser as error:
            self.show_message(error, error=True)
        except Exception as error:
            self.show_message(f"Error: {error}",error=True)