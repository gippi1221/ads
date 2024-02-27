import logging
import uvicorn
import os
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from kafka.producer import producer

from routers import analytics
from routers import events

#make sure the production logger has ERROR or CRITICAL
#as it can signifitly decrease the processing capability due to IO consuption
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
)

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

app.include_router(events.router)
app.include_router(analytics.router)

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
