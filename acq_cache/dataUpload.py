# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""Module docstring.

upload datas from local to remote database
"""

__author__ = 'WangNima'

import logging
from queue import Queue

from acq_cache.data_acq.database import DataBase
from acq_cache.data_acq.savedata_thread import SaveDataThreadA, SaveDataThreadD
from acq_cache.data_upload.cachedata_thread import CacheDataThreadA, CacheDataThreadD
from acq_cache.data_upload.historydata import Base

logging.basicConfig(level=logging.INFO)

def dataUpload(db_name, user, passwd, db_host, port = '3306'):
    """
    Upload modbus data from local database to remote database
    :param db_name: name of remote database
    :param user: user of ...
    :param passwd: password of ...
    :param db_host: IP address of ...
    :param port: port of ... , default port is 3306
    :return: no
    """
    db_local = DataBase('plcdaq', 'root', 'root')
    db_remote = DataBase(db_name, user, passwd, db_host, port)
    data_queneA = Queue(20)
    data_queneD = Queue(20)

    CacheDataThreadA(data_queneA, db_local).start()
    CacheDataThreadD(data_queneD, db_local).start()
    SaveDataThreadA(data_queneA, db_remote, Base).start()
    SaveDataThreadD(data_queneD, db_remote, Base).start()

    logging.debug('upload data start!!!')

if __name__ == '__main__':
    dataUpload('plcdaq', 'root', '123456','172.16.10.77')