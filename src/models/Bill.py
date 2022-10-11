from dataclasses import dataclass, field
from typing import List

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(kw_only=True)
class BillTicket:
    billticketid = None
    tickets: List[str] = field(default_factory=lambda: [])
    write_at: str
    create_at: str
    write_udi: str
    create_uid: str
    type: List[str] = field(default_factory=lambda: ["PENDING", "CANCELED"])
