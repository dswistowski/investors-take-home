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


@dataclass(frozen=True, slots=True)
class Commitment:
    id: int
    asset_class: str
    currency: str
    amount: int

@dataclass(frozen=True, slots=True)
class AssetClass:
    id: int
    name: str
    value: int