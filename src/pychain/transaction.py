import hashlib
import json
import time
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Transaction:
    sender: str
    recipient: str
    amount: float
    fee: float = 0.0
    timestamp: float = 0.0
    signature: Optional[str] = None
    tx_id: Optional[str] = None

    def __post_init__(self):
        if self.timestamp == 0.0:
            self.timestamp = time.time()
        if self.tx_id is None:
            self.tx_id = self.calculate_tx_id()

    def calculate_tx_id(self) -> str:
        payload = f"{self.sender}:{self.recipient}:{self.amount}:{self.fee}:{self.timestamp}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def is_coinbase(self) -> bool:
        return self.sender == "COINBASE"

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        return cls(**data)
