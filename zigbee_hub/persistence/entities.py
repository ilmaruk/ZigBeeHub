# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, DateTime, Float, BigInteger
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Device(Base):
    __tablename__ = "devices"

    euid64 = Column(String(16), primary_key=True)
    type = Column(String(3), nullable=True)
    network_addr = Column(String(4), nullable=False)


class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(BigInteger, primary_key=True)
    network_addr = Column(String(4), nullable=False)
    date_time = Column(DateTime, default=func.now())
    value = Column(Float)


class Heartbeat(Base):
    __tablename__ = "heartbeats"

    node_id = Column(String(4), primary_key=True)
    last_seen = Column(DateTime, default=func.now())
