from logging import getLogger
from fastapi import FastAPI

# db
from db import initialize
from db.database import engine

# router
from routers import api, health

logger = getLogger(__name__)

initialize.initialize_table(engine=engine, checkfirst=True)

app = FastAPI(
  titile= "S2SQuestionnaire_DB_Service",
  description = "S2S Questionnaire db service" ,
  version = "0.1" 
)

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(api.router, prefix="/api", tags=["api"])