from dataclasses import dataclass, field
from typing import List

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(kw_only=True)
class PersonTicket:
    personid = None
    ticketid = None
