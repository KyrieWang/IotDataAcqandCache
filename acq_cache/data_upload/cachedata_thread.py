# -*- coding: utf-8 -*-
#!/usr/bin/env python

'upload data into dst database'

__author__ = 'WangNima'

import time
from threading import Thread
from sqlalchemy import create_engine
from .historydata import HistoryDataA, HistoryDataD

class CacheDataThreadA(Thread):
    def __init__(self, queueA, database):
        super(CacheDataThreadA, self).__init__()
        self.queueA = queueA
        self.database = database

    def run(self):
        DB_CONNECT_STR = self.database.get_dbconnect()
        engine = create_engine(DB_CONNECT_STR)

        with engine.connect() as con:
            while True:
                rs = con.execute('SELECT * FROM historydataA LIMIT 20')
                datas = rs.fetchall()
                if datas:
                    for item in datas:
                        self.queueA.put(HistoryDataA(item))
                    con.execute('DELETE FROM historydataA order by id ASC LIMIT 20')
                    print('cache dataAAAAAAAAAAAAAA')
                else:
                    time.sleep(5)

class CacheDataThreadD(Thread):
    def __init__(self, queueD, database):
        super(CacheDataThreadD, self).__init__()
        self.queueD = queueD
        self.database = database

    def run(self):
        DB_CONNECT_STR = self.database.get_dbconnect()
        engine = create_engine(DB_CONNECT_STR)

        with engine.connect() as con:
            while True:
                rs = con.execute('SELECT * FROM historydataD LIMIT 20')
                datas = rs.fetchall()
                if datas:
                    for item in datas:
                        self.queueD.put(HistoryDataD(item))
                    con.execute('DELETE FROM historydataD order by id ASC LIMIT 20')
                    print('cache dataDDDDDDDDDDDDDDDD')
                else:
                    time.sleep(5)