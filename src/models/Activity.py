from dataclasses import dataclass, field
from typing import List

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(kw_only=True)
class Activity:
    activityid = None
    description: str
    write_at: str
    create_at: str
    write_udi: str
    create_uid: str
    stages: List[str] = field(default_factory=lambda: ["START", "END"])
