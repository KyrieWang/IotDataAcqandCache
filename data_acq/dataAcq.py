# -*- coding: utf-8 -*-
#!/usr/bin/env python

'send modbus request and collect data from slave'

__author__ = 'WangNima'

from queue import Queue
from data_acq.queryrequest import queryrequest
from data_acq.modbus import ModbusRequest
from data_acq.savedata_thread import SaveDataThreadA, SaveDataThreadD
from data_acq.collectdata_thread import CollectDataThread
from data_acq.database import DataBase

def dataAcq():
    db_local = DataBase('plcdaq', 'root', 'root')
    req_vars = queryrequest(db_local)
    request_list = []
    response_queneA = Queue()
    response_queneD = Queue()

    for var in req_vars:
        request_list.append(ModbusRequest(var))

    #for var in request_list:
    #   print(var.data_addr,var.data_length,var.fun_code,var.dev_unit)

    CollectDataThread(response_queneA, response_queneD, request_list, 5).start()
    SaveDataThreadA(response_queneA, db_local).start()
    SaveDataThreadD(response_queneD, db_local).start()
    print('acq data start!!!!!!!!!!!!!!!!!!!!!!')

if __name__ == '__main__':
    dataAcq()