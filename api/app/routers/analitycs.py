import logging
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from helpers.utils import validate_params, convert_data_to_output
from helpers.queries import build_stats_sql_query
from typing import Optional
from db.client import db

logger = logging.getLogger(__name__)

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