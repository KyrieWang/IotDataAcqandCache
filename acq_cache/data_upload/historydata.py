# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""Module docstring.

history data
"""

__author__ = 'WangNima'

from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class HistoryDataA(Base):
    def __init__(self, data):
        self.DataName = data[1]
        self.DataType = data[6]
        self.DataUnit = data[5]
        self.Timestamp = data[3]
        self.DataAddress = data[8]
        self.DeviceName = data[9]
        self.DeviceAddress = data[2]
        self.DevicePort = data[10]
        self.DeviceUnit = data[11]
        self.DataValue = data[4]
        self.FunCode = data[12]
        self.DataLenth = data[7]

    __tablename__ = 'historydataA'
    id = Column(Integer, primary_key=True, autoincrement=True)
    DataName = Column(String(50))
    DeviceAddress = Column(String(50))
    Timestamp = Column(String(50))
    DataValue = Column(Float)
    DataUnit = Column(String(50))
    DataType = Column(String(50))
    DataLenth = Column(Integer)
    DataAddress = Column(Integer)
    DeviceName = Column(String(50))
    DevicePort = Column(Integer)
    DeviceUnit = Column(Integer)
    FunCode = Column(Integer)

class HistoryDataD(Base):
    def __init__(self, data):
        self.DataName = data[1]
        self.DataType = data[5]
        self.Timestamp = data[3]
        self.DataAddress = data[7]
        self.DeviceName = data[8]
        self.DeviceAddress = data[2]
        self.DevicePort = data[9]
        self.DeviceUnit = data[10]
        self.DataValue = data[4]
        self.FunCode = data[11]
        self.DataLenth = data[6]

    __tablename__ = 'historydataD'
    id = Column(Integer, primary_key=True, autoincrement=True)
    DataName = Column(String(50))
    DeviceAddress = Column(String(50))
    Timestamp = Column(String(50))
    DataValue = Column(Float)
    DataType = Column(String(50))
    DataLenth = Column(Integer)
    DataAddress = Column(Integer)
    DeviceName = Column(String(50))
    DevicePort = Column(Integer)
    DeviceUnit = Column(Integer)
    FunCode = Column(Integer)