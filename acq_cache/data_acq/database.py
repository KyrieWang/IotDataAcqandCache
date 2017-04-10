# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""Module docstring.

database info
"""

__author__ = 'WangNima'

class DataBase(object):
    def __init__(self, db_name, user, passwd, db_host='localhost', port='3306'):
        self.__db_connect = ('mysql+mysqlconnector://' + user +
                             ':' + passwd + '@' + db_host +
                             ':' + port + '/' + db_name)

    def get_dbconnect(self):
        return self.__db_connect