# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""Module docstring.

upload datas from local to remote database
"""

__author__ = 'WangNima'

import logging
import time
from queue import Queue

from acq_cache.data_acq.database import DataBase
from acq_cache.data_acq.savedata_thread import SaveDataThreadA, SaveDataThreadD
from acq_cache.data_upload.cachedata_thread import CacheDataThreadA, CacheDataThreadD
from acq_cache.data_upload.historydata import Base
from acq_cache.data_upload.restart_thread import RestartSava_thread

logging.basicConfig(level=logging.INFO)

class DataUpload(object):
    """Summary of class here.

    upload datas from local to remote database
    """
    def __init__(self):
        self.cache_th_a = None
        self.cache_th_d = None
        self.sda_remote = None
        self.sdd_remote = None
        self.thread_check = None

    def upload_start(self, db_name, user, passwd, db_host, port='3306'):
        """
        start uploading modbus data from local database to remote database
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
        initThreadsName = ['Thread:savedataA_remote', 'Thread:savedataD_remote']
        restart_info = {'Thread:savedataA_remote': [data_queneA, db_remote, Base],
                        'Thread:savedataD_remote': [data_queneD, db_remote, Base]}

        self.cache_th_a = CacheDataThreadA(data_queneA, db_local)
        self.cache_th_d = CacheDataThreadD(data_queneD, db_local)

        self.sda_remote = SaveDataThreadA(data_queneA, db_remote, Base)
        self.sda_remote.setName(initThreadsName[0])
        self.sdd_remote = SaveDataThreadD(data_queneD, db_remote, Base)
        self.sdd_remote.setName(initThreadsName[1])

        self.thread_check = RestartSava_thread(initThreadsName, restart_info)
        self.thread_check.setName('Thread:check')

        self.cache_th_a.start()
        self.cache_th_d.start()
        self.sda_remote.start()
        self.sdd_remote.start()
        self.thread_check.start()

        logging.debug('upload data start!!!')

    def upload_stop(self):
        """
        Stop uploading modbus data
        :return: no
        """
        self.cache_th_a.stop()
        self.cache_th_d.stop()
        self.sda_remote.stop()
        self.sdd_remote.stop()
        self.thread_check.stop()

#test
if __name__ == '__main__':
    data_upload = DataUpload()
    data_upload.upload_start('plcdaq', 'root', '123456','172.16.10.77')
    time.sleep(10)
    data_upload.upload_stop()
    #time.sleep(10)
    #data_upload.upload_start('plcdaq', 'root', '123456', '172.16.10.77')