import base


class Strains(base.Base):

    def __init__(self, **kwargs):
        # Name is required, other values optional
        self._name = kwargs['name']
        self._strainType = kwargs['strainType'] if 'strainType' in kwargs else None
        self._thc = kwargs['thc'] if 'thc' in kwargs else None
        self._cbd = kwargs['cbd'] if 'cbd' in kwargs else None
    
    def __string__(self):
        print(self._name, ' ', self._strainType)

    def sqlAddStrain(self, server):
        # Requires strainType to be present
        # Use base.Base.sqlExecuteQuery
        # Checks for type of cannabis. Couldn't pass a var to fully qualified path on SQL Stored Procedure
        if self._strainType == 'indica':
            storedProcedure = 'CreateNewIndicaStrain'
        if self._strainType == 'sativa':
            storedProcedure = 'CreateNewSativaStrain'
        # Tries to format SQL command to run create strain stored procedure
        try:
            queryString = '{0}{1}{2}{3}{4}{5}{6}{7}{8}'.format("""
                USE [strains]

                EXEC	[dbo].[""", storedProcedure, """]
                    @name = N'""", self._name, """',
                    @thc = N'""", self._thc, """',
                    @cbd = N'""", self._cbd, """'
                """)
        except:
            return(self._strainType, " is not valid. Please use Indica, Sativa, or Hybrid.")
        # server should be an object defined in your script using base.Base
        server.sqlExecuteQuery(queryString)
        # Can't format a self._name value
        name = self._name
        return(f'200 {name} created')
  
    def sqlStrainSearch(self, server):
        # Will check if strain Type passed, if not it will check all strain tables
        try:
            queryString = '{0}{1}{2}{3}{4}'.format("SELECT name,thc,cbd,cbg FROM strains.", 
                        self._strainType, ".strains WHERE name = '", self._name, "'")
            returnValue = server.sqlStrainQuery(queryString)
            strainDict = {'Strain': returnValue[0][0], 'Type': self._strainType,
                        'THC': returnValue[0][1], 'CBD': returnValue[0][2], 'CBG': returnValue[0][3]}
            return(strainDict)
        except:
            pass
        # This function will search for a strain and return JSON if it exists
        # Need to add Hybrid
        strainTypeList = ['Sativa', 'Indica']
        # Searches each table for a match 
        for strainType in range(0,len(strainTypeList)):
            try:
                queryString = '{0}{1}{2}{3}{4}'.format("SELECT name,thc,cbd,cbg FROM strains.", 
                        strainTypeList[strainType], ".strains WHERE name = '", self._name, "'")
                returnValue = server.sqlStrainQuery(queryString)
                strainDict = {'Strain': returnValue[0][0], 'Type': strainTypeList[strainType],
                        'THC': returnValue[0][1], 'CBD': returnValue[0][2], 'CBG': returnValue[0][3]}
                return(strainDict)
            except:
                continue
        return('No Strain found')


