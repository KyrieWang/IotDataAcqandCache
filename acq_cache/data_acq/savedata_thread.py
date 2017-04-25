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
        self.stop_flag = False
        self.run_flag = False

    def run(self):
        DB_CONNECT_STR = self.database.get_dbconnect()
        try:
            engine = create_engine(DB_CONNECT_STR)
            DBSession = sessionmaker(bind=engine)
            session = DBSession()

            self.base.metadata.create_all(engine)
        except:
            self.run_flag = False
            return

        count = 0
        while (not self.stop_flag):
            if (not self.stop_flag):
                dataA = self.queueA.get()
                self.queueA.task_done()
                session.add(dataA)
                count += 1
                if count == 10:
                    try:
                        self.run_flag = False
                        session.commit()
                        self.run_flag = True
                        count = 0
                        logging.debug('SaveDataThreadA: save dataA in db!!!!!!!')
                    except:
                        self.run_flag = False
                        session.close()
                        break
            else:
                self.run_flag = False
                session.close()
                logging.debug('SaveDataThreadA is over!!!!!!!')
                break

    def stop(self):
        self.stop_flag = True
        self.run_flag = False

    def restart(self):
        self.stop_flag = False
        self.run_flag = True

    def run_status(self):
        return self.run_flag

class SaveDataThreadD(Thread):
    def __init__(self, queueD, database, base):
        super(SaveDataThreadD, self).__init__()
        self.queueD = queueD
        self.database = database
        self.base = base
        self.stop_flag = False
        self.run_flag = False

    def run(self):
        DB_CONNECT_STR = self.database.get_dbconnect()
        try:
            engine = create_engine(DB_CONNECT_STR)
            DBSession = sessionmaker(bind=engine)
            session = DBSession()

            self.base.metadata.create_all(engine)
        except:
            self.run_flag = False
            return

        count = 0
        while not self.stop_flag:
            if(not self.stop_flag):
                dataD = self.queueD.get()
                self.queueD.task_done()
                session.add(dataD)
                count += 1
                if count == 10:
                    try:
                        self.run_flag = False
                        session.commit()
                        self.run_flag = True
                        count = 0
                        logging.debug('SaveDataThreadD: save dataD in db!!!!!!!')
                    except:
                        self.run_flag = False
                        session.close()
                        break
            else:
                self.run_flag = False
                session.close()
                logging.debug('SaveDataThreadD is over!!!!!!!')
                break

    def stop(self):
        self.stop_flag = True
        self.run_flag = False

    def restart(self):
        self.stop_flag = False
        self.run_flag = True

    def run_status(self):
        return self.run_flag