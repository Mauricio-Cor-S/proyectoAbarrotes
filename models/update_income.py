from pathlib import Path
from decimal import Decimal, InvalidOperation
import sys

if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

INCOME_FILE = BASE_DIR / "data" / "income"

def upd_income(income):
    INCOME_FILE.parent.mkdir(parents=True, exist_ok=True)
    INCOME_FILE.write_text(str(income), encoding="utf-8")

def retrieve_income():
    if not INCOME_FILE.exists():
        upd_income("0")
        return Decimal("0")
    
    contenido = INCOME_FILE.read_text(encoding="utf-8")
    try:
        return Decimal(contenido)
    except InvalidOperation:
        raise ValueError(f"Error: El contenido '{contenido}' no es un decimal valido.")
