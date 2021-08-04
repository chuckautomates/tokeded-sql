from __future__ import absolute_import, division, print_function
import pyodbc
import time

class Base(object):

    def __init__(self, **kwargs):
        self._server = kwargs['server']
        self._database = kwargs['database']
        self._username = kwargs['username']
        self._password = kwargs['password']
    
    def __string__(self):
        print(self._server, ' ', self._database)

    def sqlExecuteQuery(self, queryString):
        # This function will run a stored Procedure to create values
        cnxn = pyodbc.connect(driver = '{SQL Server}', 
            server = self._server, 
            database = self._database, 
            uid = self._username, 
            pwd = self._password)
        cursor = cnxn.cursor()
        cursor.execute(queryString)
        # While block fixes this issue https://stackoverflow.com/questions/7753830/mssql2008-pyodbc-previous-sql-was-not-a-query
        while cursor.nextset():   # NB: This always skips the first resultset
            try:
                results = cursor.fetchall()
                return(results)
            except pyodbc.ProgrammingError:
                continue
        # Wait two seconds or else you get an error
        time.sleep(2)
        cursor.commit()
        cursor.close()
        return()

    def sqlStrainQuery(self, queryString):
        # This function will run a Search Query
        cnxn = pyodbc.connect(driver = '{SQL Server}', 
            server = self._server, 
            database = self._database, 
            uid = self._username, 
            pwd = self._password)
        cursor = cnxn.cursor()
        cursor.execute(queryString)
        returnValue = cursor.fetchall()
        cursor.close()
        return(returnValue)

