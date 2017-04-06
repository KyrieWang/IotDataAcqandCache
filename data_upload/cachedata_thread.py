# -*- coding: utf-8 -*-
#!/usr/bin/env python

'upload data into dst database'

__author__ = 'WangNima'

from threading import Thread
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_acq.modbus import ModbusResponseA,ModbusResponseD

class CacheDataThreadA(Thread):
    def __init__(self, queueA, database):
        super(CacheDataThreadA, self).__init__()
        self.queueA = queueA
        self.database = database

    def run(self):
        DB_CONNECT_STR = self.database.get_dbconnect()
        engine = create_engine(DB_CONNECT_STR)
        DBSession = sessionmaker(bind=engine)

        with DBSession() as session:
            while True:
                datas = session.query(ModbusResponseA).filter(ModbusResponseA.id < 10)
                for item in datas:
                    self.queueA.put(item)
                    session.delete(item)
                session.commit()

class CacheDataThreadD(Thread):
    def __init__(self, queueD, database):
        super(CacheDataThreadD, self).__init__()
        self.queueD = queueD
        self.database = database

    def run(self):
        DB_CONNECT_STR = self.database.get_dbconnect()
        engine = create_engine(DB_CONNECT_STR)
        DBSession = sessionmaker(bind=engine)

        with DBSession() as session:
            while True:
                datas = session.query(ModbusResponseD).filter(ModbusResponseD.id < 10)
                for item in datas:
                    self.queueD.put(item)
                    session.delete(item)
                session.commit()