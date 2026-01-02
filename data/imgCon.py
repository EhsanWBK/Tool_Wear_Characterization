import sqlite3 as sql
import os
from pathlib import Path
from data.dbCon import insertEntry, returnRefID

IMAGE_DATA_PATH = os.path.join(os.getcwd(),'imageDatabase.db')
connIMG = sql.connect(IMAGE_DATA_PATH)

def setupImageDataSet(conn: sql.Connection):
    cursor = conn.cursor()

    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS segTraining (
        imgName TEXT, 
        wearType TEXT, 
        expDate TEXT, 
        expName TEXT,
        nrCuts INTEGER,
        nrCutsTot INTEGER
        )'''
    )

    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS segExperiment (
        imgName TEXT, 
        wearType TEXT, 
        expDate TEXT, 
        expName TEXT,
        nrCuts INTEGER,
        nrCutsTot INTEGER
        )'''
    )

    # cursor.execute(
    #     '''CREATE TABLE IF NOT EXISTS objDectTraining (
    #     imgNr INT, 
    #     imgPath TEXT
        
    #     )'''
    # )

    conn.commit()
    cursor.close()

def refSegImg(conn: sql.Connection, tableName: str, imgPath: str, wearType: str, expName: str, expDate: str, nrCuts: int = 4):
    for imgName in os.listdir(imgPath):
        imgNr = returnRefID(conn=conn, tableName=tableName)
        imgExpDict = {
            'imgNr':    imgNr,
            'imgName':  imgName,
            'wearType': wearType,
            'expData':  expDate,
            'expName':  expName,
            'nrCuts': nrCuts # NUMBER OF CUTS TO BE IMPLEMENTED: GROUP 4 IMAGES
        }
        insertEntry(conn=conn, tableName=tableName, entry=imgExpDict)

def insertImgData(imgName, wearType, expDate, expName, nrCuts, nrCutsTot):
    conn = sql.connect(IMAGE_DATA_PATH); cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO segExperiment (imgName, wearType, expDate, expName, nrCuts, nrCutsTot)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (imgName, wearType, expDate, expName, nrCuts, nrCutsTot))
    conn.commit(); conn.close()

def process_folders(base_path,expDate, wearType = 'flank'):
    
    # for folder in Path(base_path).iterdir():
    #     if folder.is_dir():
    #         images = sorted([f for f in folder.iterdir() if f.suffix.lower() in ['.jpg', '.png', '.jpeg']])
    #         total_cuts = len(images) // 4
            
    #         # Assign wear type and experiment data based on folder
    #         label = 1 if wearType=='flank' else 2
    #         experiment_name = folder.name
            
    #         for idx, image in enumerate(images):
    #             num_cuts = (idx // 4) + 1
    #             insert_image_data(image.name, label, expDate, experiment_name, num_cuts, total_cuts)
                
    #         print(f"Processed folder: {folder.name}, Total images: {len(images)}, Total cuts: {total_cuts}")

    images = sorted([f for f in Path(base_path).iterdir() if f.suffix.lower() in ['.jpg', '.png', '.jpeg']])
    total_cuts = len(images) // 4
    
    # Assign wear type and experiment data
    label = 1 if wearType=='flank' else 2
    experiment_name = Path(base_path).name
    
    for idx, image in enumerate(images):
        num_cuts = (idx // 4) + 1
        insertImgData(image.name, label, expDate, experiment_name, num_cuts, total_cuts)
    
    print(f"Processed folder: {base_path}, Total images: {len(images)}, Total cuts: {total_cuts}")
