from database import SessionLocal
import psycopg2
from configparser import ConfigParser

from sqlalchemy.orm.session import sessionmaker

import initialize
import cruds, schemas
from database import engine, get_db

from fastapi import Depends


def config(filename="database.ini", section="postgresql"):
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

def connect():
  """ Connect to the PostgreSQL database server """

  connection = None

  try:

    # read connection parameters
    db_params = config()

    # connect to the PostgreSQL server
    print("Conntcting to the PostgreSQL database ...")
    connection = psycopg2.connect(**db_params)

    cur = connection.cursor()

    """
    print("PostgreSQL database version:")
    cur.execute("SELECT version()")

    db_version = cur.fetchone()
    print(db_version)
    """

    cur.close()
  except (Exception, psycopg2.DatabaseError) as error:
    print(error)
  finally:
    if connection is not None:
      connection.close()
      print("Database connection closed.")




if __name__=="__main__":
  #connect()
  initialize.initialize_table(engine=engine)

  ## add
  session = SessionLocal()

  res = cruds.add_questionnaire_report(
    db = session,
    satisfaction_level=5,
    recommendation_level=5,
    topics="Git",
    participation_level=5,
    presentation_level=5,
    free_comment="良い感じでした",
    holding_num=1
  )

  session.close()  
