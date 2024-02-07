import logging
import uvicorn
import os
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Query, Request
from fastapi.exceptions import RequestValidationError
from datetime import datetime
from typing import Optional
from models import Event
from db import Database
from helpers import validate_params
from queries import build_stats_sql_query

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

db = Database(host='clickhouse', port=8123, database='sample')

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def value_error_exception_handler(request: Request, exc: RequestValidationError):
  logger.error("Request validation error: %s", exc, extra={'request_id': request.headers.get('Request-ID')})
  return JSONResponse(status_code=405, content={"description": "Invalid input"})

@app.post('/event')
async def add_event(event: Event):
  try:
    db.insert_event('events', event)
    logger.info("Successfully added event: %s", event)
    return JSONResponse(status_code=200, content={"description": "Successful operation"})
  except Exception as e:
    logger.exception("An error occurred while processing the request: %s", e)
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

    logger.info("Request received: groupBy=%s, filters=%s, metrics=%s, granularity=%s, startDate=%s, endDate=%s",
                groupBy, filters, metrics, granularity, startDate, endDate)

    validate_params(groupBy, filters, metrics, granularity, startDate, endDate)

    query, params = build_stats_sql_query(groupBy, filters, metrics, granularity, startDate, endDate)
    result = db.query(query, params)

    data = []
    for row in result.result_rows:
      obj = {}
      for idx, val in enumerate(result.column_names):
        if isinstance(row[idx], datetime):
          obj[val] = row[idx].isoformat()
        elif isinstance(row[idx], float):
          obj[val] = "{:.2f}".format(row[idx])
        else:
          obj[val] = row[idx]
      data.append(obj)
    
    logger.info("The requested data: %s", data)
    return JSONResponse(status_code=200, content={'results': data})

  except ValueError as e:
    logger.exception("Value error occurred: %s", e)
    return JSONResponse(status_code=405, content={"description": "Invalid input"})

  except Exception as e:
    logger.exception("An error occurred while processing the request: %s", e)
    return JSONResponse(status_code=400, content={"description": "Internal error"})

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
