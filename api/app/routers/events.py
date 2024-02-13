import logging
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.event import Event
from kafka.producer import producer

logger = logging.getLogger(__name__)

responses = {
  200: {"description": "Successful operation"},
  405: {"description": "Invalid input"},
}

router = APIRouter(
    prefix="/event",
    tags=["events"],
    responses=responses,
)

@router.post('/')
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
