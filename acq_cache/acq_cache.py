# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""Module docstring.

Data acq and cache
"""

__author__ = 'WangNima'

import time

from acq_cache.dataAcq import DataAcq
from acq_cache.dataUpload import DataUpload

dataacq = DataAcq()
dataupload = DataUpload()

def data_acq_start(acfrequency=1):
    """
    Start fetching modbus response data from industrial controllers and save it in local db
    :param acfrequency: Frequency of data acquisition,default value is 1s
    :return: A list containing the starting state and IDs of illegal modbus requests vars
             The first element is bool.
             True : all modbus vars is correct ,dataAcq is starting and
             the first element is an empty list.
             False : some modbus vars is wrong or the connection is not available, and the second
             element is a list containing IDs of illegal modbus requests vars
    """
    global dataacq
    return dataacq.acq_start(acfrequency)

def data_acq_stop():
    """
    Stop fetching modbus response data
    :return: Bool.
             True,success;False,fail
    """
    global dataacq
    dataacq.acq_stop()
    return (not dataacq.acq_status())

def data_acq_status():
    """
    Check if data-acq is running correctly
    :return: Bool
             True,running;False,stopped
    """
    global dataacq
    return dataacq.acq_status()

def data_acq_start_status():
    """
    Check if data-acq has started already
    :return: Bool
             True,has started;False,has not start
    """
    global dataacq
    return dataacq.start_status()

def data_upload_start(db_name, user, passwd, db_host, port='3306'):
    """
    Start uploading modbus data from local database to remote database
    :param db_name: name of remote database
    :param user: user of ...
    :param passwd: password of ...
    :param db_host: IP address of ...
    :param port: port of ... , default port is 3306
    :return: no
    """
    global dataupload
    dataupload.upload_start(db_name, user, passwd, db_host, port)

def data_upload_stop():
    """
    Stop uploading modbus data
    :return: Bool
            True,success;False,fail
    """
    global dataupload
    dataupload.upload_stop()
    return (not dataupload.upload_status())

def data_upload_status():
    """
    Check if data-upload is running correctly
    :return: True,running;False,stopped
    """
    global dataupload
    return dataupload.upload_status()

def data_upload_start_status():
    """
    Check if data-upload has started already
    :return: Bool
             True,has started;False,has not start
    """
    global dataupload
    return dataupload.start_status()

if __name__ == '__main__':
    if True:
        #data_acq_stop()
        data_acq_start()
        # data_acq_start()
        time.sleep(10)
        print(data_acq_start_status())
        print(data_acq_status())
        data_acq_stop()
        print(data_acq_status())
        print(data_acq_start_status())
    else:
        #data_upload_stop()
        data_upload_start('plcdaq', 'root', '123456', '172.16.10.77')
        #data_upload_start('plcdaq', 'root', '123456', '172.16.10.77')
        time.sleep(10)
        print(data_upload_start_status())
        print(data_upload_status())
        data_upload_stop()
        print(data_upload_status())
        print(data_upload_start_status())

