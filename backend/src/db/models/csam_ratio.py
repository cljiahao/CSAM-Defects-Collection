from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from db.base_class import Base


class CSAM_RATIO(Base):
    id = Column(Integer, primary_key=True, index=False)
    date = Column(DateTime, default=datetime.now)
    lot_no = Column(String, nullable=False, index=True)
    plate_no = Column(String, nullable=False, index=True)
    no_of_batches = Column(Integer, nullable=False)
    no_of_chips = Column(Integer, nullable=False)
    chip_type = Column(String, nullable=False)
    no_of_ng = Column(Integer)
    no_of_others = Column(Integer)
    ng_ratio = Column(String)
    other_ratio = Column(String)
