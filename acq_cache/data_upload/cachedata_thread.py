# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""Module docstring.

upload data into dst database
"""

__author__ = 'WangNima'

import logging
import time
from threading import Thread

from sqlalchemy import create_engine

from .historydata import HistoryDataA, HistoryDataD

logging.basicConfig(level=logging.INFO)

class CacheDataThreadA(Thread):
    def __init__(self, queueA, database):
        super(CacheDataThreadA, self).__init__()
        self.queueA = queueA
        self.database = database
        self.stop_flag = False

    def run(self):
        DB_CONNECT_STR = self.database.get_dbconnect()
        engine = create_engine(DB_CONNECT_STR)

        with engine.connect() as con:
            while (not self.stop_flag):
                if (not self.stop_flag):
                    rs = con.execute('SELECT * FROM historydataA LIMIT 20')
                    datas = rs.fetchall()
                    if datas:
                        logging.debug('CacheDataThreadA: cache dataAAAAAAAAAAAAAA')
                        for item in datas:
                            self.queueA.put(HistoryDataA(item))
                        con.execute('DELETE FROM historydataA order by id ASC LIMIT 20')
                    else:
                        con.execute('TRUNCATE TABLE historydataA')
                        logging.debug('CacheDataThreadA: historydataA table is empty')
                        time.sleep(5)
                else:
                    logging.debug('CacheDataThreadA is over')
                    break

    def stop(self):
        self.stop_flag = True

    def restart(self):
        self.stop_flag = False

class CacheDataThreadD(Thread):
    def __init__(self, queueD, database):
        super(CacheDataThreadD, self).__init__()
        self.queueD = queueD
        self.database = database
        self.stop_flag = False

    def run(self):
        DB_CONNECT_STR = self.database.get_dbconnect()
        engine = create_engine(DB_CONNECT_STR)

        with engine.connect() as con:
            while (not self.stop_flag):
                if (not self.stop_flag):
                    rs = con.execute('SELECT * FROM historydataD LIMIT 20')
                    datas = rs.fetchall()
                    if datas:
                        for item in datas:
                            self.queueD.put(HistoryDataD(item))
                        con.execute('DELETE FROM historydataD order by id ASC LIMIT 20')
                        logging.debug('CacheDataThreadD: cache dataDDDDDDDDDDDDD')
                    else:
                        con.execute('TRUNCATE TABLE historydataD')
                        logging.debug('CacheDataThreadD: historydataD table is empty')
                        time.sleep(5)
                else:
                    logging.debug('CacheDataThreadD is over')
                    break

    def stop(self):
        self.stop_flag = True

    def restart(self):
        self.stop_flag = False