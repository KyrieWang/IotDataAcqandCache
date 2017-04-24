# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""Module docstring.

restart the dead threads
"""

import logging
import time
from threading import Thread
from threading import enumerate

from acq_cache.data_acq.collectdata_thread import CollectDataThread
from acq_cache.data_acq.savedata_thread import SaveDataThreadA, SaveDataThreadD

logging.basicConfig(level=logging.INFO)

class RestartSava_thread(Thread):
    def __init__(self, initThreadsName, threadInfo):
        super(RestartSava_thread, self).__init__()
        self.initThreasName = initThreadsName
        self.threadInfo = threadInfo
        self.stop_flag = False

    def run(self):
        while not self.stop_flag:
            if(not self.stop_flag):
                nowThreadsName = []
                nowthreads = enumerate()
                for thread in nowthreads:
                    nowThreadsName.append(thread.getName())

                for threadname in self.initThreasName:
                    if threadname in nowThreadsName:
                        pass
                    else:
                        logging.debug('thread {0} is dead'.format(threadname))
                        res_info = self.threadInfo[threadname]

                        if threadname == 'Thread:savedataA_remote':
                            thread = SaveDataThreadA(res_info[0], res_info[1], res_info[2])
                        else:
                            thread = SaveDataThreadD(res_info[0], res_info[1], res_info[2])

                        thread.setName(threadname)
                        thread.start()
                        logging.debug('thread {0} restart'.format(threadname))

                time.sleep(120)
            else:
                logging.debug('RestartSava_thread is over')
                break

    def stop(self):
        self.stop_flag = True

    def restart(self):
        self.stop_flag = False

class RestartCollec_thread(Thread):
    def __init__(self, initThreadsName, threadInfo):
        super(RestartCollec_thread, self).__init__()
        self.initThreasName = initThreadsName
        self.threadInfo = threadInfo
        self.stop_flag = False

    def run(self):
        while True:
            if (not self.stop_flag):
                nowThreadsName = []
                nowthreads = enumerate()
                for thread in nowthreads:
                    nowThreadsName.append(thread.getName())

                for threadname in self.initThreasName:
                    if threadname in nowThreadsName:
                        pass
                    else:
                        logging.debug('thread {0} is dead'.format(threadname))
                        res_info = self.threadInfo[threadname]
                        thread = CollectDataThread(res_info[0], res_info[1], res_info[2], res_info[3])
                        thread.setName(threadname)
                        thread.start()
                        logging.debug('thread {0} restart'.format(threadname))

                time.sleep(60)
            else:
                logging.debug('RestartCollec_thread is over')
                break

    def stop(self):
        self.stop_flag = True

    def restart(self):
        self.stop_flag = False