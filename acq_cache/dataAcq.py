# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""Module docstring.

Fetches modbus response data from industrial controllers and save it in local db
"""

__author__ = 'WangNima'

import logging
import threading
import time
from queue import Queue

from acq_cache.data_acq.collectdata_thread import CollectDataThread
from acq_cache.data_acq.database import DataBase
from acq_cache.data_acq.modbus import Base
from acq_cache.data_acq.modbus import ModbusRequest
from acq_cache.data_acq.modbus import modbus_vars_check
from acq_cache.data_acq.queryrequest import queryrequest
from acq_cache.data_acq.savedata_thread import SaveDataThreadA, SaveDataThreadD
from acq_cache.data_upload.restart_thread import RestartCollec_thread

Lock = threading.Lock()
logging.basicConfig(level=logging.INFO)

class DataAcq(object):
    """Summary of class here.

    Fetches modbus response data from industrial controllers and save it in local db
    """
    __instance = None

    def __init__(self):
        self.__save_th_a = None
        self.__save_th_d = None
        self.__acq_th = None
        self.__check_th = None
        self.__req_vars = None
        self.__request_list = []
        self.__db_local = None
        self.__start_flag = False
        self.__stop_flag = False

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            try:
                Lock.acquire()
                if not cls.__instance:
                    cls.__instance = super(DataAcq, cls).__new__(cls, *args, **kwargs)
            finally:
                Lock.release()
        return cls.__instance

    def acq_start(self, acfrequency=1):
        """
        Start fetching modbus response data from industrial controllers and save it in local db
        :param acfrequency: Frequency of data acquisition,default value is 1s
        :return: A list containing the IDs of illegal modbus requests vars
                 If the list is empty, all modbus vars is correct and dataAcq is starting
        """
        if ((not self.__start_flag) and (not self.__stop_flag)):
            self.__db_local = DataBase('plcdaq', 'root', 'root')
            self.__req_vars = queryrequest(self.__db_local)
            response_queneA = Queue(20)
            response_queneD = Queue(20)

            for var in self.__req_vars:
                self.__request_list.append(ModbusRequest(var))

            var_check = modbus_vars_check(self.__request_list)

            start_check = []
            if var_check:
                start_check.append(False)
                logging.debug('some modbus vars are wrong!!!')
            else:
                start_check.append(True)
                logging.debug('modbus vars are all right!!!')
                initThreadsName = ['Thread:collectdata']
                restart_info = {'Thread:collectdata': [response_queneA, response_queneD, self.__request_list, acfrequency]}

                self.__save_th_a = SaveDataThreadA(response_queneA, self.__db_local, Base)
                self.__save_th_d = SaveDataThreadD(response_queneD, self.__db_local, Base)

                self.__acq_th = CollectDataThread(response_queneA, response_queneD, self.__request_list, acfrequency)
                self.__acq_th.setName(initThreadsName[0])

                self.__check_th = RestartCollec_thread(initThreadsName, restart_info)
                self.__check_th.setName('Thread:check')

                self.__save_th_a.start()
                self.__save_th_d.start()
                self.__acq_th.start()
                self.__check_th.start()
                self.__start_flag = True
                logging.debug('acq data start!!!')
            start_check.append(var_check)
            return start_check

        elif (self.__start_flag and self.__stop_flag) :
            for var in queryrequest(self.__db_local):
                if var in self.__req_vars:
                    pass
                else:self.__request_list.append(ModbusRequest(var))

            var_check = modbus_vars_check(self.__request_list)
            start_check = []
            if var_check:
                start_check.append(False)
            else:
                start_check.append(True)

            self.__save_th_a.restart()
            self.__save_th_d.restart()
            self.__acq_th.restart()
            self.__check_th.restart()
            self.__stop_flag = False
            start_check.append(True)
            logging.debug('Restart daq!!!')

            start_check.append(var_check)
            return start_check

        else:
            pass

    def acq_stop(self):
        """
        Stop fetching modbus response data
        :return: no
        """
        if ((self.__start_flag) and (not self.__stop_flag)):
            self.__save_th_a.stop()
            self.__save_th_d.stop()
            self.__acq_th.stop()
            self.__check_th.stop()
            self.__stop_flag = True
            logging.debug('acq data stop!!!')

    def acq_status(self):
        """
        Check if data-acq is running correctly
        :return: Bool, you know
        """
        if self.__start_flag :
            s1 = self.__acq_th.run_status()
            s2 = self.__save_th_d.run_status()
            s3 = self.__save_th_a.run_status()
            return (s1 and s2 and s3)
        else:
            return False

    def start_status(self):
        return self.__start_flag

#test
if __name__ == '__main__':
    dataacq = DataAcq()
    #dataacq.acq_stop()
    dataacq.acq_start()
    print(dataacq.acq_status())
    time.sleep(10)
    #dataacq.acq_stop()
    print(dataacq.acq_status())
    #time.sleep(30)
    #dataacq.acq_start()
    #dataacq.acq_start()
    #print(dataacq.acq_status())