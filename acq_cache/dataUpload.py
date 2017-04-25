# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""Module docstring.

upload datas from local to remote database
"""

__author__ = 'WangNima'

import logging
import threading
import time
from queue import Queue

from acq_cache.data_acq.database import DataBase
from acq_cache.data_acq.savedata_thread import SaveDataThreadA, SaveDataThreadD
from acq_cache.data_upload.cachedata_thread import CacheDataThreadA, CacheDataThreadD
from acq_cache.data_upload.historydata import Base
from acq_cache.data_upload.restart_thread import RestartSava_thread

logging.basicConfig(level=logging.INFO)
Lock = threading.Lock()

class DataUpload(object):
    """Summary of class here.

    upload datas from local to remote database
    """
    __instance = None

    def __init__(self):
        self.__cache_th_a = None
        self.__cache_th_d = None
        self.__sda_remote = None
        self.__sdd_remote = None
        self.__thread_check = None
        self.__start_flag = False
        self.__stop_flag = False

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            try:
                Lock.acquire()
                if not cls.__instance:
                    cls.__instance = super(DataUpload, cls).__new__(cls, *args, **kwargs)
            finally:
                Lock.release()
        return cls.__instance

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
        if (not self.__start_flag):
            db_local = DataBase('plcdaq', 'root', 'root')
            db_remote = DataBase(db_name, user, passwd, db_host, port)
            data_queneA = Queue(20)
            data_queneD = Queue(20)
            initThreadsName = ['Thread:savedataA_remote', 'Thread:savedataD_remote']
            restart_info = {'Thread:savedataA_remote': [data_queneA, db_remote, Base],
                            'Thread:savedataD_remote': [data_queneD, db_remote, Base]}

            self.__cache_th_a = CacheDataThreadA(data_queneA, db_local)
            self.__cache_th_d = CacheDataThreadD(data_queneD, db_local)

            self.__sda_remote = SaveDataThreadA(data_queneA, db_remote, Base)
            self.__sda_remote.setName(initThreadsName[0])
            self.__sdd_remote = SaveDataThreadD(data_queneD, db_remote, Base)
            self.__sdd_remote.setName(initThreadsName[1])

            self.__thread_check = RestartSava_thread(initThreadsName, restart_info)
            self.__thread_check.setName('Thread:check')

            self.__cache_th_a.start()
            self.__cache_th_d.start()
            self.__sda_remote.start()
            self.__sdd_remote.start()
            self.__thread_check.start()
            self.__start_flag = True
            self.__stop_flag = False

            logging.debug('upload data start!!!')

        else:
            pass

    def upload_stop(self):
        """
        Stop uploading modbus data
        :return: no
        """
        if ((self.__start_flag) and (not self.__stop_flag)):
            self.__cache_th_a.stop()
            self.__cache_th_d.stop()
            self.__sda_remote.stop()
            self.__sdd_remote.stop()
            self.__thread_check.stop()
            self.__stop_flag = True
            self.__start_flag = False
            logging.debug('upload data Rstart!!!')

    def upload_status(self):
        """
        Check if data-upload is running correctly
        :return: Bool, you know
        """
        if self.__start_flag :
            return (self.__sda_remote.run_status() or self.__sdd_remote.run_status())
        else:
            return False

    def start_status(self):
        return self.__start_flag


#test
if __name__ == '__main__':
    data_upload = DataUpload()
    #data_upload.upload_stop()
    print(data_upload.upload_status())
    data_upload.upload_start('plcdaq', 'root', '123456','172.16.10.77')
    print(data_upload.upload_status())
    time.sleep(10)
    #data_upload.upload_stop()
    print(data_upload.upload_status())
    #time.sleep(30)
    #data_upload.upload_start('plcdaq', 'root', '123456', '172.16.10.77')
    #data_upload.upload_start('plcdaq', 'root', '123456', '172.16.10.77')
    #print(data_upload.upload_status())