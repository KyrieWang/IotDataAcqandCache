# -*- coding: utf-8 -*-
#!/usr/bin/env python

'send modbus request and collect data from slave'

__author__ = 'WangNima'

import logging
from queue import Queue
from acq_cache.data_acq.queryrequest import queryrequest
from acq_cache.data_acq.modbus import ModbusRequest
from acq_cache.data_acq.savedata_thread import SaveDataThreadA, SaveDataThreadD
from acq_cache.data_acq.collectdata_thread import CollectDataThread
from acq_cache.data_acq.database import DataBase
from acq_cache.data_acq.modbus import Base

logging.basicConfig(level=logging.INFO)

def dataAcq(acfrequency = 1):
    """
    Fetches modbus response data from industrial controllers
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

    #for var in request_list:
    #   print(var.data_addr,var.data_length,var.fun_code,var.dev_unit)

    CollectDataThread(response_queneA, response_queneD, request_list, acfrequency).start()
    SaveDataThreadA(response_queneA, db_local, Base).start()
    SaveDataThreadD(response_queneD, db_local, Base).start()
    logging.info('acq data start!!!!!!!!!!!!!!!!!!!!!!')

if __name__ == '__main__':
    dataAcq(5)