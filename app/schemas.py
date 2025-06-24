from pydantic import BaseModel
from typing import List, Any, Dict
from datetime import datetime


class Party(BaseModel):
    role: str
    name: str


class ContractBase(BaseModel):
    filename: str
    subject: str
    conditions: Dict[str, Any]
    parties: List[Party]


class ContractCreate(ContractBase):
    pass


class ContractRead(ContractBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
