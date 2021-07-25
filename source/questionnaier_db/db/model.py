from sqlalchemy.sql.expression import null
from db.database import Base
from sqlalchemy import Column, Integer, Text, String

class questionnaire(Base):
  __tablename__ = "questionnaire"

  id = Column(
    String(255),
    primary_key=True,
    nullable = False,
    comment="主キー"
  )

  satisfaction_level = Column(
    Integer,
    nullable=False,
    comment="満足度"
  )

  recommendation_level = Column(
    Integer,
    nullable=False,
    comment="他の人に推薦したい内容だったか"
  )

  topics = Column(
    Text,
    nullable=True,
    comment="取り上げて欲しいトピック"
  )

  participation_level = Column(
    Integer,
    nullable=False,
    comment="次回も参加したいか"
  )

  presentation_level = Column(
    Integer,
    nullable=False,
    comment="発表してみたいか"
  )

  free_comment = Column(
    Text,
    nullable=True,
    comment="自由回答"
  )

  holding_num = Column(
    Integer,
    nullable=False,
    comment="開催回"
  )

