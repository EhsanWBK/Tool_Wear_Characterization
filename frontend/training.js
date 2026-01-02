"use strict";

// =============================================
// 	  Model Training - Widget Initialization			
// =============================================

const buttonTrainModel = document.getElementById('trainModelButton');

const tableAugmentation = document.getElementById('augmentTable');

// Needed when more model architectures:
const checkUNet = document.getElementById('unet_arch');
const checkFlankWear = document.getElementById('flankWear');
const checkCraterWear = document.getElementById('craterWear');

const checkRandomSelection = document.getElementById('randomSelection');

const checkSelectAugmentation = document.getElementById('selectAug');
const checkCropping = document.getElementById('cropping');
const checkHorizontalFlip = document.getElementById('horizontalFlip');
const checkVerticalFlip = document.getElementById('verticalFlip');
const checkRot90Deg = document.getElementById('rot90deg');
const checkBrightness = document.getElementById('brightness');
const checkContrast = document.getElementById('contrast');
const checkTransferLearn = document.getElementById('transferLearn');
const checkShuffleTrain = document.getElementById('shuffleTrain');

const inputModelName = document.getElementById('modelName');
// const inputModelSaveDir = document.getElementById('modelSavingDir');
const inputTrainImgNr = document.getElementById('trainingImgNr');
const inputImageHeigth = document.getElementById('imageHeight');
const inputImageWidth = document.getElementById('imageWidth');
const inputNrChannels = document.getElementById('nrChannels');
const inputValSize = document.getElementById('validationSize');
const inputRandomState = document.getElementById('randomState');
const inputBatchSize = document.getElementById('batchSize');
const inputNrEpochs = document.getElementById('nrEpochs');
const inputEarlyStopping = document.getElementById('earlyStopping');

// =========================================
// 	  Model Training - HTML Functions			
// =========================================

// buttonSaveModel.disabled = true;

function augmentationSelected() {
	if (checkSelectAugmentation.checked){ tableAugmentation.style.display = 'block'; }
	if (checkSelectAugmentation.checked==false){ tableAugmentation.style.display = 'none'; }
}


function disableNavigation() {
	
}

// =========================================
// 	  Model Training - Python Functions			
// =========================================

function py_train() {

	var parDict = {};

	parDict['modelName'] = inputModelName.value;
	parDict['unet_arch'] = checkUNet.value;

	parDict['nrTrainImages'] = inputTrainImgNr.value;
	parDict['flank'] = checkFlankWear.value;
	parDict['crater'] = checkCraterWear.value;

	parDict['imageHeight'] = inputImageHeigth.value;
	parDict['imageWidth'] = inputImageWidth.value;
	parDict['nrChannels'] = inputNrChannels.value;

	parDict['validationSize'] = inputValSize.value;
	parDict['randomState'] = inputRandomState.value;
	parDict['randomSelection'] = checkRandomSelection.checked;
	parDict['batchSize'] = inputBatchSize.value;
	parDict['nrEpochs'] = inputNrEpochs.value;
	parDict['patience'] = inputEarlyStopping.value;
	parDict['transferLearn'] = checkTransferLearn.checked;
	parDict['shuffleTrain'] = checkShuffleTrain.checked;

	parDict['selectAug'] = checkSelectAugmentation.checked;
	parDict['cropping'] = checkCropping.checked;
	parDict['brightness'] = checkBrightness.checked;
	parDict['contrast'] = checkContrast.checked;
	parDict['flip_horizontal'] = checkHorizontalFlip.checked;
	parDict['flip_vertical'] = checkVerticalFlip.checked;
	parDict['rotate90'] = checkRot90Deg.checked;

	console.table(parDict);
	eel.trainModel(parDict)();
}

eel.expose(updateResults);
function updateResults(loss, acc, iou, pr, f1){
	lossDisp.src = "data:image/jpeg;base64," + loss;
	accDisp.src = "data:image/jpeg;base64," + acc;
	iouDisp.src = "data:image/jpeg;base64," + iou;
	prDisp.src = "data:image/jpeg;base64," + pr;
	f1Disp.src = "data:image/jpeg;base64," + f1;
}

function py_displayResults(){
	eel.displayResults()();
}

