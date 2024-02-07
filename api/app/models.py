from pydantic import BaseModel, validator
from datetime import datetime

class Event(BaseModel):
  id: int
  event_date: datetime
  attribute1: int = None
  attribute2: int = None
  attribute3: int = None
  attribute4: str = None
  attribute5: str = None
  attribute6: bool = None
  metric1: int
  metric2: float
  
  @validator("event_date", pre=True)
  def validate_date(cls, value):
    return value
  
  @validator('id', 'attribute1', 'attribute2', 'attribute3', 'metric1')
  def validate_int64(cls, value):
    min_int64 = -(2**63)
    max_int64 = (2**63) - 1
    if not (min_int64 <= value <= max_int64):
      raise ValueError(f"{value} is not within the int64 range")
    return value

  @validator("attribute6")
  def validate_bool(cls, value):
    if not isinstance(value, bool):
      raise ValueError(f"{value} is not a bool")
    return value
