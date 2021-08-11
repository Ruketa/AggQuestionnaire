import uuid
from typing import List
from sqlalchemy.orm import Session
from db import model
from db import schemas

def select_questionnaire_all(db: Session)->List[schemas.Questionnaire]:
  return db.query(model.questionnaire).all()

def select_questionnaire_by_holding_num(
  db: Session,
  holding_num: int
  )->List[schemas.Questionnaire]:
  return db.query(model.questionnaire).filter(model.questionnaire.holding_num == holding_num).all()

def add_questionnaire_report(
  db: Session,
  satisfaction_level: int,
  recommendation_level: int,
  topics: str,
  participation_level: int, 
  presentation_level: int,
  free_comment: str,
  holding_num: int,
  commit: bool = True
  )->schemas.Questionnaire:

  questionnaire_id = str(uuid.uuid4())[:6]
  data = model.questionnaire(
    id = questionnaire_id,
    satisfaction_level = satisfaction_level,
    recommendation_level = recommendation_level,
    topics = topics,
    participation_level = participation_level,
    presentation_level = presentation_level,
    free_comment = free_comment,
    holding_num = holding_num
  )

  db.add(data)

  if commit:
    db.commit()
    db.refresh(data)

  return data
