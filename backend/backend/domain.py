from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class Investor:
    id: int
    name: str
    type: str
    date_added: date
    address: str
    total_commitment: int
