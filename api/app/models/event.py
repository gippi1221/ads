from pydantic import BaseModel, validator
from datetime import datetime
from decimal import Decimal

class Event(BaseModel):
  """
  Represents an event with various attributes and metrics.
  """
  id: int
  event_date: datetime
  attribute1: int = None
  attribute2: int = None
  attribute3: int = None
  attribute4: str = None
  attribute5: str = None
  attribute6: bool = None
  metric1: int
  metric2: Decimal
  
  #custom validators. there is a room for improvement
  @validator('id', 'attribute1', 'attribute2', 'attribute3', 'metric1')
  def validate_int64(cls, value):
    min_int64 = -(2**63)
    max_int64 = (2**63) - 1
    if not (min_int64 <= value <= max_int64):
      raise ValueError(f"{value} is not within the int64 range")
    return value
