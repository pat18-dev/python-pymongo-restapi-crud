from dataclasses import dataclass, field
from typing import List

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(kw_only=True)
class Person:
    document_number: str = None
    name: str = None
    level: List[str] = field(
        default_factory=lambda: ["PLANNING", "DESIGN", "TODO", "TEST", "END"]
    )
    grade: List[str] = field(
        default_factory=lambda: ["PLANNING", "DESIGN", "TODO", "TEST", "END"]
    )
