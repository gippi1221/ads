import logging
import uvicorn
import os
import json
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Query, Request
from fastapi.exceptions import RequestValidationError
from datetime import datetime
from typing import Optional
from models import Event
from db import Database
from helpers import validate_params, convert_data_to_output
from queries import build_stats_sql_query
from producer import KafkaProducer
from fastapi.middleware.cors import CORSMiddleware

#make sure the production logger has ERROR or CRITICAL
#as it can signifitly decrease the processing capability due to IO consuption
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

db = Database(host='clickhouse', port=8123, database='sample')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)

producer = KafkaProducer()

@app.on_event("startup")
async def startup_event():
  await producer.setup()

@app.on_event("shutdown")
async def shutdown_event():
  await producer.close()

@app.exception_handler(RequestValidationError)
async def value_error_exception_handler(request: Request, exc: RequestValidationError):
  logger.error("Request validation error: %s", exc, extra={'request_id': request.headers.get('Request-ID')})
  return JSONResponse(status_code=405, content={"description": "Invalid input"})

@app.post('/event')
async def add_event(event: Event):
  """
  This method is to create a new event in the DB
  """
  try:
    if producer.producer is None:
      logger.exception("The kafka producer is not ready: %s", e)
      return JSONResponse(status_code=400, content={"description": "Internal error"})
    
    # Produce message to Kafka topic
    await producer.send_data_to_kafka(event.model_dump_json())
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
  """
  This method is to provide aggregated data
  """
  try:

    logger.info("Request received: groupBy=%s, filters=%s, metrics=%s, granularity=%s, startDate=%s, endDate=%s",
                groupBy, filters, metrics, granularity, startDate, endDate)

    #validate incoming parameters
    validate_params(groupBy, filters, metrics, granularity, startDate, endDate)

    #build parametrized sql query
    query, params = build_stats_sql_query(groupBy, filters, metrics, granularity, startDate, endDate)

    #query data
    result = db.query(query, params)

    #convert data to expected result
    data = convert_data_to_output(result)
    
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
