# -*- coding: utf-8 -*-
#!/usr/bin/env python

'modbusTcp request class'

__author__ = 'WangNima'

from threading import Thread
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class SaveDataThreadA(Thread):
    def __init__(self, queueA, database):
        super(SaveDataThreadA, self).__init__()
        self.queueA = queueA
        self.database = database

    def run(self):
        DB_CONNECT_STR = self.database.get_dbconnect()
        engine = create_engine(DB_CONNECT_STR)
        DBSession = sessionmaker(bind=engine)
        count = 0
        with DBSession() as session:
            while True:
                dataA = self.queueA.get()
                self.queueA.task_done()
                session.add(dataA)
                print('add dataA!!!!!!!')
                count += 1
                if count == 10:
                    session.commit()
                    count = 0

class SaveDataThreadD(Thread):
    def __init__(self, queueD, database):
        super(SaveDataThreadD, self).__init__()
        self.queueD = queueD
        self.database = database

    def run(self):
        DB_CONNECT_STR = self.database.get_dbconnect()
        engine = create_engine(DB_CONNECT_STR)
        DBSession = sessionmaker(bind=engine)
        count = 0
        with DBSession() as session:
            while True:
                dataD = self.queueD.get()
                self.queueD.task_done()
                session.add(dataD)
                print('add dataD!!!!!!!')
                count += 1
                if count == 10:
                    session.commit()
                    count = 0