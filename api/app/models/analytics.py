from pydantic import BaseModel, Field
from typing import List, Optional, Annotated, Union, Dict
from enum import Enum
from datetime import datetime
from fastapi import FastAPI, Query

class Granularity(Enum):
  hourly = 'hourly'
  daily = 'daily'

class OrderedMap(BaseModel):
  attribute: str
  value: str

class AnalyticsQueryParams(BaseModel):
  groupBy: str
  filters: Annotated[Union[List[OrderedMap], None], Query()] = None
  metrics: str
  granularity: Granularity
  startDate: Optional[str] = None
  endDate: Optional[str] = None