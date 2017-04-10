# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""Module docstring.

query all vars from database
"""

__author__ = 'WangNima'

from sqlalchemy import create_engine

from .database import DataBase


def queryrequest(database):
    DB_CONNECT_STR = database.get_dbconnect()
    engine = create_engine(DB_CONNECT_STR, echo=False)

    with engine.connect() as con:
        rs = con.execute('SELECT * FROM datasources')
        values = rs.fetchall()
        #print(values)
        return values

if __name__ == '__main__':
    queryrequest(DataBase('plcdaq', 'root', '123456'))