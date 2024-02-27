import logging
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from helpers.utils import validate_params, convert_data_to_output
from helpers.queries import build_stats_sql_query
from enum import Enum
from db.client import db
from models.analytics import AnalyticsQueryParams

logger = logging.getLogger(__name__)

class Granularity(str, Enum):
  hourly = "hourly"
  daily = "daily"

responses = {
  200: {"description": "Successful operation"},
  405: {"description": "Invalid input"},
}

router = APIRouter(
  prefix="/analytics",
  tags=["analytics"],
  responses=responses,
)

@router.get('/query')
async def get_data(qp: AnalyticsQueryParams = Depends()):

  qp: AnalyticsQueryParams = Depends()
  """
  This method is to provide aggregated data
  """
  try:

    logger.info("Request received: %s", qp) 

    #build parametrized sql query
    query, params = build_stats_sql_query(qp.groupBy, qp.filters, qp.metrics, qp.granularity, qp.startDate, qp.endDate)

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
