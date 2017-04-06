# -*- coding: utf-8 -*-
#!/usr/bin/env python

'database info'

__author__ = 'WangNima'

from queue import Queue
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_acq.modbus import Base
from data_acq.savedata_thread import SaveDataThreadA, SaveDataThreadD
from data_upload.cachedata_thread import CacheDataThreadA, CacheDataThreadD
from data_acq.database import DataBase

def dataUpload():
    db_local = DataBase('plcdaq', 'root', 'root')
    db_remote = DataBase('plcdaq', 'root', '123456','172.16.10.77')
    #DB_CONNECT_REMOTE = db_remote.get_dbconnect()
    data_queneA = Queue()
    data_queneD = Queue()

    CacheDataThreadA(data_queneA, db_local).start()
    CacheDataThreadD(data_queneD, db_local).start()
    SaveDataThreadA(data_queneA, db_remote).start()
    SaveDataThreadD(data_queneD, db_remote).start()

    print('upload data start!!!')