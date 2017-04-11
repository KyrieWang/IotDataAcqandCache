# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""Module docstring.

Fetches modbus response data from industrial controllers and save it in local db
"""

__author__ = 'WangNima'

import logging
import time
from queue import Queue

from acq_cache.data_acq.collectdata_thread import CollectDataThread
from acq_cache.data_acq.database import DataBase
from acq_cache.data_acq.modbus import Base
from acq_cache.data_acq.modbus import ModbusRequest
from acq_cache.data_acq.queryrequest import queryrequest
from acq_cache.data_acq.savedata_thread import SaveDataThreadA, SaveDataThreadD
from acq_cache.data_upload.restart_thread import RestartCollec_thread

logging.basicConfig(level=logging.INFO)

class DataAcq(object):
    """Summary of class here.

    Fetches modbus response data from industrial controllers and save it in local db
    """
    def __init__(self):
        self.save_th_a = None
        self.save_th_d = None
        self.acq_th = None
        self.check_th = None

    def acq_start(self, acfrequency=1):
        """
        Start fetching modbus response data from industrial controllers and save it in local db
        :param acfrequency: frequency of data acquisition,default value is 1s
        :return: no
        """
        db_local = DataBase('plcdaq', 'root', 'root')
        req_vars = queryrequest(db_local)
        request_list = []
        response_queneA = Queue(20)
        response_queneD = Queue(20)

        for var in req_vars:
            request_list.append(ModbusRequest(var))

        initThreadsName = ['Thread:collectdata']
        restart_info = {'Thread:collectdata': [response_queneA, response_queneD, request_list, acfrequency]}

        self.save_th_a = SaveDataThreadA(response_queneA, db_local, Base)
        self.save_th_d = SaveDataThreadD(response_queneD, db_local, Base)

        self.acq_th = CollectDataThread(response_queneA, response_queneD, request_list, acfrequency)
        self.acq_th.setName(initThreadsName[0])

        self.check_th = RestartCollec_thread(initThreadsName, restart_info)
        self.check_th.setName('Thread:check')

        self.save_th_a.start()
        self.save_th_d.start()
        self.acq_th.start()
        self.check_th.start()

        logging.debug('acq data start!!!!!!!!!!!!!!!!!!!!!!')

    def acq_stop(self):
        """
        Stop fetching modbus response data
        :return: no
        """
        self.save_th_a.stop()
        self.save_th_d.stop()
        self.acq_th.stop()
        self.check_th.stop()

#test
if __name__ == '__main__':
    dataacq = DataAcq()
    dataacq.acq_start()
    time.sleep(10)
    dataacq.acq_stop()
    #time.sleep(60)
    #dataacq.acq_start()