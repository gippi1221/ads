import logging
import re
import clickhouse_connect
from clickhouse_connect import common
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Query, Request
from fastapi.exceptions import RequestValidationError
from datetime import datetime
from typing import Optional
from models import Event
from helpers import parse_filters, validate_iso_date

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

common.set_setting('autogenerate_session_id', False)
client = clickhouse_connect.get_client(host='clickhouse', port=8123, database='sample')

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def value_error_exception_handler(request: Request, exc: RequestValidationError):
  logger.error(exc)
  return JSONResponse(status_code=405, content={"description": "Invalid input"})

@app.post('/event')
async def add_event(event: Event):
  try:

    row = [event.model_dump()[field] for field in event.model_fields.keys()]
    client.insert('events', [row], column_names=list(event.model_fields.keys()))
    return JSONResponse(status_code=200, content={"description": "Successful operation"})

  except Exception as e:
    logger.exception("An error occurred while processing the request.")
    return JSONResponse(status_code=400, content={"description": "Internal error"})

@app.get('/analytics/query')
async def get_data(
    groupBy: str = Query(..., min_length=1, description="Attributes for grouping (comma-separated)", example="attribute1,attribute4"),
    filters: Optional[str] = Query(None, description="Array of filters (attribute-value pairs)", example=[{"attribute": "attribute1", "value": "198772"}, {"attribute": "attribute4", "value": "some string"}]),
    metrics: str = Query(..., min_length=1, description="Metrics to retrieve (comma-separated, always sums)", example="metric1,metric2"),
    granularity: str = Query(..., min_length=1, description="Granularity (hourly or daily)", example="hourly"),
    startDate: Optional[str] = Query(None, description="Start date and time for filtering (format: YYYY-MM-DDTHH:mm:ss)", example="2023-02-02T01:00:00"),
    endDate: Optional[str] = Query(None, description="End date and time for filtering (format: YYYY-MM-DDTHH:mm:ss)", example="2023-02-02T01:00:00")
  ):
  try:
    
    where_list = []
    params = {}

    #input params validation
    if granularity not in ['hourly', 'daily']:
      raise ValueError("Invalid granularity value, must be hourly or daily")
    
    if not re.match(r'^\w+(,\w+)+$', metrics):
      raise ValueError("Invalid metrics value, must comma separated names")
    
    if not re.match(r'^\w+(,\w+)+$', groupBy):
      raise ValueError("Invalid metrics value, must comma separated names")

    if startDate:
      validate_iso_date(startDate)
      where_list.append("event_date >= {start_date:DateTime}")
      params['start_date'] = startDate

    if endDate:
      validate_iso_date(endDate)
      where_list.append("event_date < {end_date:DateTime}")
      params['end_date'] = endDate
    
    #parse filters array and validate input values
    #populate where array and parameters dictionary
    if filters:
      parsed_filters = parse_filters(filters)
      for f in parsed_filters:
        attribute = f['attribute']
        value = f['value']

        if attribute == 'attribute1':
          try:
            int_value = int(value)
          except ValueError:
            raise ValueError("Invalid value for attribute1. Expected an int.")
          where_list.append("attribute1 = {attribute1:Int64}")
          params['attribute1'] = int_value
        elif attribute == 'attribute2':
          try:
            int_value = int(value)
          except ValueError:
            raise ValueError("Invalid value for attribute2. Expected an int.")
          where_list.append("attribute2 = {attribute2:Int64}")
          params['attribute2'] = int_value
        elif attribute == 'attribute3':
          try:
            int_value = int(value)
          except ValueError:
            raise ValueError("Invalid value for attribute3. Expected an int.")
          where_list.append("attribute3 = {attribute3:Int64}")
          params['attribute3'] = int_value
        elif attribute == 'attribute4':
          if not isinstance(value, str):
            raise ValueError("Invalid type for attribute4. Expected str.")
          where_list.append("attribute4 = {attribute4:String}")
          params['attribute4'] = value
        elif attribute == 'attribute5':
          if not isinstance(value, str):
            raise ValueError("Invalid type for attribute5. Expected str.")
          where_list.append("attribute5 = {attribute5:String}")
          params['attribute5'] = value
        elif attribute == 'attribute6':
          if value not in ['true', 'false']:
            raise ValueError("Invalid type for attribute6. Expected bool.")
          where_list.append("attribute6 = {attribute6:Bool}")
          params['attribute6'] = value == 'true'
        else:
          raise ValueError("Unknown filter parameter")

    #build db query
    query = f"select {groupBy},date_trunc('{'hour' if granularity == 'hourly' else 'day'}', event_date) as date"

    for m in metrics.split(','):
      query += f",sum({m}) as {m}"

    query += f"\nfrom events"

    if where_list:
      where_clause = " and ".join(where_list)
      query += f"\nwhere {where_clause}"

    query += f"\ngroup by date_trunc('{'hour' if granularity == 'hourly' else 'day'}', event_date),{groupBy}"
    
    result = client.query(query, parameters=params)

    #convert result to expected structure
    data = []
    for row in result.result_rows:
      obj = {}
      for idx, val in enumerate(result.column_names):
        if isinstance(row[idx], datetime):
          obj[val] = row[idx].isoformat()
        else:
          obj[val] = row[idx]
      data.append(obj)

    return JSONResponse(status_code=200, content={'results': data})

  except ValueError as e:
    logger.exception(e)
    return JSONResponse(status_code=405, content={"description": "Invalid input"})

  except Exception as e:
    logger.exception("An error occurred while processing the request.")
    return JSONResponse(status_code=400, content={"description": "Internal error"})
