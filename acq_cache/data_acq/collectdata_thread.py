# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""Module docstring.

Thread:sends modbus request and collect data from modbus server
"""

__author__ = 'WangNima'

import logging
import time
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
        self.stop_flag = False
        self.run_flag = False

    def run(self):
        master = modbus_tcp.TcpMaster(host = self.modbusRequest_list[0].dev_addr)
        while (not self.stop_flag):
            for request in self.modbusRequest_list:
                if (not self.stop_flag) :
                    try:
                        data = send_modbus(request, master)
                        self.run_flag = True
                    except:
                        self.run_flag = False
                        break
                    if request.fun_code == 3 or request.fun_code == 4:
                        self.queueA.put(ModbusResponseA(request, data))
                        logging.debug('CollectDataThread: put into queueA')
                    else:
                        self.queueD.put(ModbusResponseD(request, data))
                        logging.debug('CollectDataThread: put into queueD')
                else:
                    self.run_flag = False
                    logging.debug('CollectDataThread is over')
                    break
            #self.run_flag = True
            time.sleep(self.acfrequency)

    def stop(self):
        self.stop_flag = True
        self.run_flag = False

    def restart(self):
        self.stop_flag = False
        self.run_flag = True

    def run_status(self):
        return self.run_flag