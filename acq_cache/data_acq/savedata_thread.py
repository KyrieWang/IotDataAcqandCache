# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""Module docstring.

modbusTcp request class
"""

__author__ = 'WangNima'

import logging
from threading import Thread

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO)

class SaveDataThreadA(Thread):
    def __init__(self, queueA, database, base):
        super(SaveDataThreadA, self).__init__()
        self.queueA = queueA
        self.database = database
        self.base = base
        self.stop_flag = True

    def run(self):
        DB_CONNECT_STR = self.database.get_dbconnect()
        try:
            engine = create_engine(DB_CONNECT_STR)
            DBSession = sessionmaker(bind=engine)
            session = DBSession()

            self.base.metadata.create_all(engine)
        except:
            return

        count = 0
        while self.stop_flag:
            dataA = self.queueA.get()
            self.queueA.task_done()
            session.add(dataA)
            count += 1
            if count == 10:
                try:
                    session.commit()
                    count = 0
                    logging.debug('SaveDataThreadA: save dataA in db!!!!!!!')
                except:
                    session.close()
                    break

    def stop(self):
        self.stop_flag = False

class SaveDataThreadD(Thread):
    def __init__(self, queueD, database, base):
        super(SaveDataThreadD, self).__init__()
        self.queueD = queueD
        self.database = database
        self.base = base

    def run(self):
        DB_CONNECT_STR = self.database.get_dbconnect()
        try:
            engine = create_engine(DB_CONNECT_STR)
            DBSession = sessionmaker(bind=engine)
            session = DBSession()

            self.base.metadata.create_all(engine)
        except:
            return

        count = 0
        while True:
            dataD = self.queueD.get()
            self.queueD.task_done()
            session.add(dataD)
            count += 1
            if count == 10:
                try:
                    session.commit()
                    count = 0
                    logging.debug('SaveDataThreadD: save dataD in db!!!!!!!')
                except:
                    session.close()
                    break

    def stop(self):
        self.stop_flag = False