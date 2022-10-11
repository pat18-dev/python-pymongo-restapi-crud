from dataclasses import dataclass, field
from typing import List

from dataclasses_json import dataclass_json

PRICE = {"POLLADA": 20, "PARRILLADA": 20, "ROCOTO": 15, "LECHON": 25, "ARROZ": 15}


@dataclass_json
@dataclass(kw_only=True)
class TicketActivity:
    activityid = None
    description: str
    write_at: str
    create_at: str
    write_udi: str
    create_uid: str
    type: List[str] = field(
        default_factory=lambda: ["POLLADA", "PARRILLADA", "ROCOTO", "LECHON", "ARROZ"]
    )

    @property
    def price(self) -> float:
        return PRICE.get(self.type, 0.0)
