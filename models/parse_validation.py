from datetime import date, datetime
import json
import re
import controller.user_errors as ue
from decimal import Decimal, ROUND_DOWN

def parse_date(date_text):
    formatos = ["%Y/%m/%d", "%d,%m,%y","%Y-%m-%d", "%d-%m-%y"]
    clean_date = re.sub(r"\s+","",date_text)
    for formato in formatos:
        try:
            return datetime.strptime(clean_date,formato).date()
        except Exception:
            continue
    raise ue.InvalidDate()

def validate_cur(cur,allows_negatives=False):
    clean_cur=re.sub(r"[\s,]","",cur)
    try:
        value = Decimal(clean_cur)
    except Exception:
        raise ue.InvalidNumber()
    real_cur = value.quantize(Decimal("0.00"),rounding=ROUND_DOWN)
    if allows_negatives:
        return real_cur
    elif 0 <= real_cur:
        return real_cur
    raise ue.InvalidNumber("El número no puede ser negativo. Intenta de nuevo")
    
def date_to_text(date_convert):
    return date_convert.strftime("%Y-%m-%d")

def text_date_to_text(text_date):
    return date_to_text(parse_date(text_date))

def json_to_expiry(expiry_json):
    data = json.loads(expiry_json)

    return {
        date.fromisoformat(d): quantity
        for d, quantity in data.items()
    }

def expiry_to_json(expiry_dict):
    return json.dumps({
        d.isoformat(): quantity
        for d, quantity in expiry_dict.items() #creo que esto funciona
    })