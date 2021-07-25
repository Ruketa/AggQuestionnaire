from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from configparser import ConfigParser

def read_config(filename="database.ini", section="postgresql"):
  # create parser
  parser = ConfigParser()
  # read config
  parser.read(filename)

  db_config = {}
  if parser.has_section(section):
    for item in parser.items((section)):
      db_config[item[0]] = item[1]
  else:
    raise Exception("Section {0} not found in the {1} file".format(section, filename))

  return db_config

db_config = read_config()
hostname  = db_config["host"]
port      = db_config["port"] 
db_name   = db_config["database"]
user      = db_config["user"]
password  = db_config["password"]
server_url = f"postgresql://{hostname}:{port}/{db_name}?user={user}&password={password}"
engine = create_engine(
  server_url,
  encoding = "utf-8",
  pool_recycle=3600,
  echo=False,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
  db = SessionLocal()
  try:
    yield db
  except:
    db.rollback()
    raise
  finally:
    db.close()

@contextmanager
def get_context_db():
  db = SessionLocal()
  try:
    yield db
  except:
    db.rollback()
    raise
  finally:
    db.close()