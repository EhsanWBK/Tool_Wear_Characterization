''' ## Post-Processing Functions '''
import cv2
import numpy as np
import pandas as pd
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from sklearn.cluster import DBSCAN
from utensils.generalUtensils import getTimeStamp

COLOR_LIST = ['blue', 'orange', 'green', 'purple', 'cyan', 'pink']

#  =========================================
#  	     Flank Wear Evaluation		
#  =========================================

def measurementVB(predMask) -> list:
    ASPECT_RESIZE = (2000,1400)
    frame = predMask[0,:,:,0]
    img = cv2.resize(frame, ASPECT_RESIZE, interpolation=cv2.INTER_LINEAR)
    ret, thresh = cv2.threshold(img, 127, 255, 0)
    thresh = cv2.convertScaleAbs(thresh)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    result = getCountourIndices(contours)
    VBmax_AX = []; fitImg = []
    for i in result:
        min_max_list = []
        CNT = contours[i]; RECT = cv2.minAreaRect(CNT); BOX = cv2.boxPoints(RECT); BOX = np.int0(BOX)
        imgColor = cv2.cvtColor(np.copy(img), cv2.COLOR_GRAY2BGR)
        FIT = cv2.drawContours(np.copy(imgColor), [BOX], 0, (0, 0, 255), 3); fitImg.append(FIT)
    
        coordinates = BOX.reshape((-1, 1, 2))
        mask = np.zeros_like(img) # Create a mask image with the same dimensions as the original image
        mask = cv2.fillPoly(mask, [coordinates], (255, 255, 255)) # Draw a filled polygon (ROI) on the mask using the defined coordinates
        mask = mask.astype(np.uint8)
        roi = cv2.bitwise_and(img, img, mask=mask) # Perform a bitwise AND operation between the original image and the mask to extract the ROI
        roi = roi.astype(np.uint8)
        edges = cv2.Canny(roi, 180, 500)
        kernel = np.ones((3, 3), np.uint8) # Dilate the edges to increase thickness
        edges_dilated = cv2.dilate(edges, kernel, iterations=1)
        White_Pixels = np.argwhere(edges_dilated == 255)
        White_Pixels_tolist = White_Pixels.tolist()

        for y, x in White_Pixels_tolist:
            found = False
            for entry in min_max_list:
                if entry[0] == y: entry[1] = min(entry[1], x); entry[2] = max(entry[2], x); found = True; break
            if not found: min_max_list.append([y, x, x, 0])
        for entry in min_max_list: entry[3] = round(np.cross(BOX[1] - BOX[0], np.array([entry[2], entry[0]]) - BOX[0]) / np.linalg.norm(BOX[1] - BOX[0]), 2)
        for entry in min_max_list: y, min_x, max_x, difference = entry
        Dis = [sublist[3] for sublist in min_max_list]
        VBmax_AX.append(round(float(max(Dis)) * 1.725, 2))
    return max(VBmax_AX)

def getCountourIndices(contours):
    valid_indices = []
    for i in range(len(contours)):
        if len(contours[i]) > 100: 
            for j in range(len(contours[i])):
                if 1100 < contours[i][j][0][0] + contours[i][j][0][1] < 2000:valid_indices.append(i); break
    return valid_indices

#  =========================================
#  	     Crater Wear Evaluation		
#  =========================================

def measurementCW():
    return

#  =========================================
#  	            Mask Display		
#  =========================================



#  =========================================
#  	        Wear Curve Display		
#  =========================================

COLOR_LIST = ['blue', 'orange', 'green', 'purple', 'cyan', 'pink']

def createWearCurve(xIn: list, yIn: list, title:str, label:list = [''], cutsPerRun:int = 5, bias:int = 30):
    
    X_LIM = max(max(sublist) for sublist in xIn) * cutsPerRun
    Y_LIM = max(max(sublist) for sublist in yIn) - bias
    fig, ax = plt.subplots(figsize=(12, 8))
    for plotIdx in range(len(xIn)): 
        x = [i * cutsPerRun for i in xIn[plotIdx]]  # Scale x-values
        y = [i - bias for i in yIn[plotIdx]]  # Shift bias y-values
        ax.plot(x, y, marker='o', linestyle='None', color=COLOR_LIST[plotIdx % len(COLOR_LIST)], label=label[plotIdx])
    
    # Plot aesthetics
    tickPos = list(range(0, X_LIM + 1, 10 * cutsPerRun))  # Ensure tick positions are in range
    tickLbl = [str(i) for i in tickPos]  # Labels for the tick positions
    ax.set_xticks(tickPos)  # Set tick positions
    ax.set_xticklabels(tickLbl, rotation=45)  # Set tick labels
    ax.set_xlabel('Cuts', fontsize=28)
    ax.set_ylabel(f'VB [μm]', fontsize=28)
    ax.set_title(f'Wear Curve for {title}', fontsize=34)
    ax.set_xlim(left=0, right=X_LIM + 20)
    ax.set_ylim(bottom=0, top=Y_LIM + 20)
    ax.legend(loc='upper left', fontsize=24)
    ax.tick_params(axis='both', which='major', labelsize=24)
    ax.grid(True, linestyle='--')
    plt.tight_layout()

    return fig

def createCombinedWearCurve(dataIn:list, title:str, cutsPerRun:int = 5, linestyle:str = 'None', marker:str = 'o', bias:int = 30): 
    xIn = [x[0] for x in dataIn]
    yIn = [y[1] for y in dataIn]
    X_LIM = max(max(sublist) for sublist in xIn)*cutsPerRun
    Y_LIM = max(max(sublist) for sublist in yIn)-bias
    fig, ax = plt.subplots(figsize=(12, 8))
    for edge in range(len(xIn)): 
        x = [i*cutsPerRun for i in xIn[edge]]; y = [i - bias for i in yIn[edge]]  
        ax.plot(x, y, marker=marker, linestyle=linestyle,color=COLOR_LIST[edge], label=f'Cutting Edge (CE) {edge + 1}')

    # Plot aesthetics
    tickPos = list(range(0, X_LIM + 1, 20 * cutsPerRun))  # Ensure tick positions are in range
    tickLbl = [str(i) for i in tickPos]  # Labels for the tick positions
    ax.set_xticks(tickPos)  # Set tick positions
    ax.set_xticklabels(tickLbl, rotation=45)  # Set tick labels
    ax.set_xlabel('Cuts', fontsize=28)
    ax.set_ylabel(f'VB [μm]', fontsize=28)
    ax.set_title(f'Wear Curve {title}', fontsize=34)
    ax.set_xlim(left=0, right=X_LIM + 20)
    ax.set_ylim(bottom=0, top=Y_LIM + 20)
    ax.legend(loc='upper left', fontsize=15)
    ax.tick_params(axis='both', which='major', labelsize=24)
    ax.grid(True, linestyle='--')
    plt.tight_layout()
    plt.savefig(os.path.join(os.getcwd(),'06_Main_Code','tmp','wearCurveTmp.jpg'))
    return fig, ax

def plotTrendline(dataIn:list, title:str, cutsPerRun:int = 5, linestyle:str = '-', marker:str = 'None', 
                  degree:int = 2, bias:int = 30):
    xIn = [x[0] for x in dataIn]
    yIn = [y[1] for y in dataIn]
    X_LIM = max(max(sublist) for sublist in xIn)*cutsPerRun
    Y_LIM = max(max(sublist) for sublist in yIn)-bias
    fig, ax = plt.subplots(figsize=(12, 8))
    for edge in range(len(xIn)): 
        x = [i*cutsPerRun for i in xIn[edge]]; y = [i - bias for i in yIn[edge]]  # Shift bias y-values
        coeff = np.polyfit(x, y, degree); ployEquation = np.poly1d(coeff)
        xTrend = np.linspace(min(x), max(x),100); yTrend = ployEquation(xTrend)
        ax.plot(xTrend, yTrend, marker=marker, linestyle=linestyle,color=COLOR_LIST[edge], label=f'Cutting Edge (CE) {edge + 1}')
    # Plot aesthetics
    tickPos = list(range(0, X_LIM + 1, 20 * cutsPerRun))  # Ensure tick positions are in range
    tickLbl = [str(i) for i in tickPos]  # Labels for the tick positions
    ax.set_xticks(tickPos)  # Set tick positions
    ax.set_xticklabels(tickLbl, rotation=45)  # Set tick labels
    ax.set_xlabel('Cuts', fontsize=28)
    ax.set_ylabel(f'VB [μm]', fontsize=28)
    ax.set_title(f'Wear Curve {title}', fontsize=34)
    ax.set_xlim(left=0, right=X_LIM + 20)
    ax.set_ylim(bottom=0, top=Y_LIM + 20)
    ax.legend(loc='upper left', fontsize=24)
    ax.tick_params(axis='both', which='major', labelsize=24)
    ax.grid(True, linestyle='--')
    plt.tight_layout()
    return fig, ax

def outlierDetection(yIn:list, eps:int = 7, min_samples:int = 9):
    xVal = np.arange(1, len(yIn)+1)
    data2D = np.column_stack((xVal,yIn))
    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(data2D)
    labels = clustering.labels_
    clusterLbl = (labels != -1); outlierLbl = (labels == -1)
    clusterX = xVal[clusterLbl]; outlierX = xVal[outlierLbl]; #print('Outlier X: ', outlierX)
    clusterY = data2D[clusterLbl]; outlierY = data2D[outlierLbl]
    return [clusterX, clusterY[:,1].tolist()], [outlierX, outlierY[:,1].tolist()]

def wearCurvePlot(wearData:list, nrCE:int = 4, nrExp:int = 1, cutsPerRun:int = 5, wearType:str = 'flank', trendDeg:int = 2):
    globRawData = []; globCleanData = []; globFig = []
    wearSplit = [wearData[i*len(wearData)//nrExp : (i+1)*len(wearData)//nrExp] for i in range(nrExp)]
    for wearExp in wearSplit:
        rawDataList = []; cleanDataList = []; figList = []
        for edgeNr in range(nrCE):
            yRaw = [float(wearExp[i*nrCE+edgeNr]) for i in range(len(wearExp)//nrCE)]; xRaw = np.arange(start=1, stop=len(yRaw)+1,step=1)
            cluster, outlier = outlierDetection(yIn=yRaw)
            rawDataList.append([xRaw, yRaw]); cleanDataList.append([cluster[0], cluster[1]])
        cleanCombinedWearCurve2, _ = createCombinedWearCurve(dataIn=cleanDataList, title='with Data Filtering',linestyle='-',marker='None')
        globFig.append(np.frombuffer(cleanCombinedWearCurve2.canvas.tostring_rgb(),dtype=np.uint8))
    return globRawData, globCleanData, globFig