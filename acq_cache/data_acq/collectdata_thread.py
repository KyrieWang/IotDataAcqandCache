# -*- coding: utf-8 -*-
#!/usr/bin/env python

'Thread:send modbus request and collect data from slave'

__author__ = 'WangNima'

import time
import logging
from threading import Thread
import modbus_tk.modbus_tcp as modbus_tcp
from .modbus import ModbusResponseA, ModbusResponseD
from .modbus import send_modbus

logging.basicConfig(level=logging.INFO)

class CollectDataThread(Thread):
    def __init__(self, queueA, queueD, modbusRequest_list, acfrequency):
        super(CollectDataThread, self).__init__()
        self.queueA = queueA
        self.queueD = queueD
        self.modbusRequest_list = modbusRequest_list
        self.acfrequency = acfrequency

    def run(self):
        master = modbus_tcp.TcpMaster(host = self.modbusRequest_list[0].dev_addr)
        while True:
            for request in self.modbusRequest_list:
                data = send_modbus(request, master)
                if request.fun_code == 3 or request.fun_code == 4:
                    self.queueA.put(ModbusResponseA(request, data))
                    logging.info('put into queueA')
                else:
                    self.queueD.put(ModbusResponseD(request, data))
                    logging.info('put into queueD')
            time.sleep(self.acfrequency)