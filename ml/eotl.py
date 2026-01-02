import pandas as pd
import sqlite3 as sql
from data.imgCon import loadImgData
from data.dbCon import returnRange

def loadImgAndPred(db_name, experiment_name, target_folder, ml_model):
    conn = sql.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT imgName, nrCuts FROM segExperiment WHERE expname = ? ORDER BY nrCuts
    ''', (experiment_name,))
    
    records = cursor.fetchall()
    conn.close()
    
    if not records:
        print("No records found for the given experiment name.")
        return
    class_names = ['crater', 'flank']
    test_img_paths = [path for path in glob.glob(f"{target_folder}/**/*", recursive=True)]
    test_ds = tf.data.Dataset.from_tensor_slices(test_img_paths)
    test_ds = test_ds.map(lambda file_path: process_path(file_path), num_parallel_calls=AUTOTUNE)
    test_ds = configure_for_performance(test_ds)
    num_batches = test_ds.cardinality().numpy()
    cuts_numbers = []; maxWearList = []; classList = []
    for image in test_ds.take(num_batches):
        pred_mask, pred_cls = ml_model.predict(image, verbose=False)
        # for _image, _pred_mask, _pred_cls in zip(image, pred_mask, pred_cls):
        #     
        #     # Plot
        #     fig, axes = plt.subplots(1, 2, figsize=(15, 5))  # 1 row, 3 columns
            
        #     axes[0].imshow(_image, cmap='gray')
        #     axes[0].set_title('Image')
        #     axes[0].axis('off')  # Hide axes for a cleaner view

        #     axes[1].imshow(_pred_mask > 0.5, cmap='gray')
        #     # axes[2].set_title(f'Prediction: {class_names[(_pred_cls > 0.5).astype(int)[0]]}')
        #     axes[1].axis('off')
            
        #     plt.tight_layout()
        #     plt.show()
        maxVB = measurementVB(frame=pred_mask*255) #if pred_cls == 1 else 0
        classList.append(int(pred_cls[0][0]))
        maxWearList.append(maxVB)
    
    # plotresult(cutNr=np.repeat(np.arange(1,len(records)/4+1),4),predictions=maxWearList)
    # plt.figure(figsize=(10, 5))
    # plt.plot(np.repeat(np.arange(1,len(records)/4+1),4), maxWearList, marker='o', linestyle='-', color='b', label='Prediction')
    # plt.xlabel("Number of Cuts")
    # plt.ylabel("Prediction Output")
    # plt.title(f"ML Predictions for {experiment_name}")
    # plt.legend()
    # plt.grid()
    # plt.show()
    df = pd.DataFrame({'wearType':classList, 'wearMax': maxWearList})
    return df


def getFullExpDF(experiment):
    df = returnRange(conn=connIMG, tableName='segExperiment',key='expName', values=[experiment])
    dfNew = load_images_and_predict(db_name='imageDatabase.db', experiment_name=experiment,target_folder=imageFolder, ml_model=model)
    dfConnect = pd.concat([df,dfNew],axis=1)
    dfSelect = dfConnect[['nrCuts', 'nrCutsTot']]
    dfConnect.drop(columns=['nrCuts', 'nrCutsTot'], inplace=True)
    dfDiff = pd.DataFrame({'cutRemain': dfSelect['nrCutsTot'] - dfSelect['nrCuts']})

    # Connect to TH
    dfExp = returnRange(conn=connTH, tableName='experiment',key='nameExp',values=[experiment])
    toolVal = str(dfExp['toolID'][0]); wpVal = str(dfExp['workpieceID'][0]); procVal = str(dfExp['processID'][0])
    dfTool = returnRange(conn=connTH, tableName='tool',key='refNr',values=[toolVal])
    # dfWP = returnRange(conn=connTH, tableName='workpiece',key='refNr',values=[wpVal])
    dfProc = returnRange(conn=connTH, tableName='process',key='refNr',values=['2'])

    # Data Cleaning
    dfTool.drop(columns=['toolName'], inplace=True)
    dfTool.drop(columns=['coatMat'], inplace=True)
    dfTool.drop(columns=['toolMat'], inplace=True)

    dfProc.drop(columns=['refNr'], inplace=True)

    for col in dfTool.columns: dfConnect[col] = dfTool[col][0]
    for col in dfProc.columns: dfConnect[col] = dfProc[col][0]

    # Data Cleaning
    dfConnect.drop(columns=['imgName'], inplace=True)
    dfConnect.drop(columns=['expDate'], inplace=True)
    dfConnect.drop(columns=['expName'], inplace=True)

    return dfConnect, dfDiff