import sqlite3 as sql
import pandas as pd
import os
from data.dbHeader import CONN_IMG_DB, CONN_TH
import glob

# Get Single Image
# Get Stack of Images
# Get joint Image Info

def getTableNames(conn: sql.Connection) -> str:
    cursor = conn.cursor(); query = "SELECT name FROM sqlite_master WHERE type='table';"
    cursor.execute(query); tables = cursor.fetchall(); tableNames = [table[0] for table in tables]; cursor.close()
    return tableNames

def getColumnNames(conn: sql.Connection, tableName: str) -> str:
    cursor = conn.cursor(); query = f"PRAGMA table_info ({tableName});"
    cursor.execute(query); columns = cursor.fetchall(); colNames = [column[1] for column in columns]; cursor.close()
    return colNames

# Data return

def returnRange(conn: sql.Connection, tableName: str, key: str, values: list) -> pd.DataFrame:
    ''' key: column name; values: list of discrete entries; '''
    cursor = conn.cursor(); temp = ', '.join(['?']*len(values)); query = f"SELECT * FROM {tableName} WHERE {key} = ({temp});"
    cursor.execute(query, values); data = cursor.fetchall(); colNames = [description[0] for description in cursor.description]
    cursor.close(); df = pd.DataFrame(data, columns=colNames); return df

def returnColumn(conn: sql.Connection, tableName: str, column: str) -> pd.DataFrame:
    query = f'SELECT {column} FROM {tableName}'; df = pd.read_sql_query(query, conn); return df

def returnRefID(conn: sql.Connection, tableName: str, ref: str = 'refNr') -> pd.DataFrame:
    idDF = returnColumn(conn=conn, tableName=tableName, column=ref)
    newID = 1 if idDF.empty else idDF.iloc[-1].to_list()[0] + 1
    return newID

def returnTableDB(conn: sql.Connection, tableName: str) -> pd.DataFrame:
    query = f"SELECT * FROM {tableName}"; df = pd.read_sql_query(query, conn); return df

# Check DB

def checkForEntry(conn: sql.Connection, tableName: str, values: tuple, ref: str = 'refNr'):
    ''' Checks the table for occurance of values in table. Returns True/False and ID/IDList'''
    cursor = conn.cursor(); columns = getColumnNames(conn=conn, tableName=tableName)[1:]
    statement = [f'{column} = ?' for column in columns]; condition = ' AND '.join(statement); query = f'SELECT {ref} FROM {tableName} WHERE {condition}'
    cursor.execute(query, values); data = cursor.fetchall()
    if data: return True, data[0][0]
    else: return False, returnRefID(conn=conn, tableName=tableName, ref=ref)

# Insert Entry

def insertEntry(conn: sql.Connection, tableName: str, entry: dict) -> None:
    cursor = conn.cursor();# inTable, id = checkForEntry(conn=conn, tableName=tableName, values=entry)
    columns = ', '.join(entry.keys()); temp = ', '.join(['?']*len(entry)); query = f"INSERT INTO {tableName} ({columns}) VALUES ({temp});"
    cursor.execute(query, tuple(entry.values())); conn.commit(); cursor.close()

# Display

def displayDB(conn: sql.Connection):
    tableNames = getTableNames(conn=conn); allDF = []
    for name in tableNames:
        df = returnTableDB(conn=conn, tableName=name); # display(df)
        allDF.append(df)
    # allDF = [returnTableDB(conn=conn, tableName=name) for name in tableNames]
    return allDF

# Remove Database Entry

def deleteEntry(conn: sql.Connection, tableName: str, condition: list) -> None:
    ''' Example: condition = "columnA < 15" or condition = "id = 1" '''
    cursor = conn.cursor(); command = f"DELETE FROM {tableName} WHERE {condition}"
    cursor.execute(command); conn.commit(); cursor.close()

def deleteRange(conn: sql.Connection, tableName: str, key: str, values: list) -> None:
    cursor = conn.cursor(); temp = ', '.join(['?']*len(values)); command = f"DELETE FROM {tableName} WHERE {key} IN ({temp});"
    cursor.execute(command, values); conn.commit(); cursor.close()

def deleteTable(conn: sql.Connection, tableName: str) -> None:
    cursor = conn.cursor(); command = f'DROP TABLE {tableName}'
    cursor.execute(command); conn.commit(); cursor.close()

def deleteDB(dbPath):
    if os.path.exists(dbPath): os.remove(dbPath)

def pathCreator(expName: str = ''):
    CLASS_NAMES = ['crater','flank']
    # if expName == '': imgNameFromDB = returnRange(conn=CONN_IMG_DB, tableName='segTraining')
    # else:
    imgNameFromDB = returnRange(conn=CONN_IMG_DB, tableName='segExperiment', key='expName', values=[expName]); DIR = os.path.join(os.getcwd(),'data', 'experiment')
    imgPath = [os.path.join(DIR, 'images', className, imgName) for className in CLASS_NAMES
               for imgName in imgNameFromDB]
    return imgPath

def imageReader(path):
    return

