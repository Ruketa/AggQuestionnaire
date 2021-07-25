from typing import Optional
from pydantic import BaseModel

class Questionnaire(BaseModel):
  id: str
  satisfaction_level: int
  recommendation_level: int
  topics: Optional[str]
  participation_level: int
  presentation_level: int
  free_comment: Optional[str]
  holding_num: int

  class Config:
    orm_mode = True

""" check
q = Questionnaire(
  id = 2,
  satisfaction_level = 5,
  recommendation_level = 5,
  topics = "UnrealEngine",
  participation_level = 5,
  presentation_level = 5,
  free_comment = "また参加したいです",
  holding_num = 1
)
print(q.dict())
"""