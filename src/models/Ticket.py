from dataclasses import dataclass, field
from typing import List
from datetime import datetime

from dataclasses_json import dataclass_json

STATE = {
    "P": "PENDIENTE",
    "E": "TERMINADO",
    "X": "ANULADO",
}

PRICES = {
    "O": 20.0, 
    "P": 20.0, 
    "R": 15.0, 
    "L": 25.0, 
    "A": 15.0, 
    "B": 5.0
}

CATEGORIES = {
    "O": "POLLADA",
    "P": "PARRILLADA",
    "R": "ROCOTO",
    "L": "LECHON",
    "A": "ARROZ",
    "B": "BINGO",
}
LEVELS = {
    "0": "3 AÑOS",
    "1": "4 AÑOS",
    "2": "5 AÑOS",
    "3": "1RO",
    "4": "2DO",
    "5": "2DOA",
    "6": "3RO",
    "7": "4TO",
    "8": "5TO",
    "9": "6TO",
    "10": "N/A"
}
GRADES = {
    "1": "INICIAL",
    "2": "PRIMARIA",
    "3": "SECUNDARIA",
    "4": "DEUDORES",
    "5": "N/A"
}
DATE_FORMAT = "%d/%m/%Y, %H:%M:%S"

@dataclass_json
@dataclass(kw_only=True)
class Ticket:
    ticketid = None
    name: str
    level: str
    grade: str
    state: str
    write_udi: str
    price: float
    write_at: field(default_factory=datetime.now().strftime(DATE_FORMAT))
    category: List[str] = field(
        default_factory=lambda: [k for k, _ in CATEGORIES.items()]
    )
