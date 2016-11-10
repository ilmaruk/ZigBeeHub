# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from entities import Base

engine = create_engine("sqlite:///zigbee_hub.db")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

