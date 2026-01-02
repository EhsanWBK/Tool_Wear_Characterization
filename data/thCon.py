import sqlite3 as sql
import os
from data.dbCon import insertEntry

TOOL_HISTORY_PATH = os.path.join(os.getcwd(),'toolHistory.db')
connTH = sql.connect(TOOL_HISTORY_PATH)

def setupToolHistory(conn: sql.Connection):
    cursor = conn.cursor()
    
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS experiment (

        refNr int, 
        nameExp text, 
        dateExp text, 
        workpieceID int, 
        processID int, 
        toolID int,
        nC int,
        nCT int, 
        lC real,
        firstImg, int,
        lastImg int,
        nrImg int,
        duration int
        
        )'''
    ) 
    
    # cursor.execute(
    #     '''CREATE TABLE IF NOT EXISTS workpiece (
    #     refNr int, 
    #     wpMat text
        
    #     )'''
    # )
    
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS process (
        refNr int, 
        vC real, 
        n real, 
        vf real, 
        fz real, 
        ap real,
        ae real
        
        )'''
    ) 
    
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS tool (
        refNr int,
        toolName text, 
        coatMat text, 
        toolMat text, 
        Z int,
        DC real, 
        angleHel real,
        angleEdge real, 
        L real,
        LC real
        
        )'''
    )

# Entry Dictionaries

processDict = {
    'refNr':    2,
    'vC':       133.0,
    'n':        8500.0,
    'vf':       1700.0,
    'fz':       0.05,
    'ap':       2.5,
    'ae':       1.5
}

toolDict = {
    'refNr':    7,
    'toolName': 'HOLEX Pro Steel VHM-Schruppfräser HPC, TiAlN, ⌀ DC: 16mm',
    'coatMat':  'TiAlN',
    'toolMat':  'VHM',
    'Z':        4,
    'DC':       16.0,
    'angleHel': 38.0,
    'angleEdge':45.0,
    'L':        92.0,
    'LC':       32.0
}

expDict = {
    'refNr':        3,
    'nameExp':      'WKZ3',
    'dateExp':      '28.05.2024',
    'workpieceID':  1,
    'processID':    3,
    'toolID':       1,
    'nC':           395,
    'nCT':          1975,
    'lC':           29.625,
    'firstImg':     3528,
    'lastImg':      5492,
    'nrImg':        1591,
    'duration':     11

}

# INSERTING ENTRIES
# insertEntry(conn=connTH, tableName='tool', entry=toolDict)