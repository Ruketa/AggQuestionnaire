from logging import getLogger
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

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

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(api.router, prefix="/api", tags=["api"])