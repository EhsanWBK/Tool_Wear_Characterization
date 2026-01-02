const canvasRob1 = document.getElementById('robScreen1')
const canvasRob2 = document.getElementById('robScreen2')

// ===========================================
// 	 Robot - HTML Functions			
// ===========================================

function checkPos() {
    // x,y,z must not be empty
    // x,y,z must be in range (?) -> maybe in python

}

function checkSpeed() {
    // must be int
    // must be not null -> set to 25
}

function checkToolPos() {
    // 
}

// ============================================
// 	  Robot - Python Functions			
// ============================================

eel.expose(updateRobCanvas1);
function updateRobCanvas1(val) { robScreen1.src = "data:image/jpeg;base64," + val; }

eel.expose(updateRobCanvas2);
function updateRobCanvas2(val) { robScreen2.src = "data:image/jpeg;base64," + val; }

eel.expose(displayWearType);
function displayWearType(wearType) { document.getElementById('wearTypeLbl').innerHTML = wearType; }

eel.expose(displayWearLand);
function displayWearLand(wearLand) {document.getElementById('wearLandLbl').innerHTML = wearLand; }

eel.expose(displayEoTL);
function displayEoTL(eotl) { document.getElementById('eotlLbl').innerHTML = eotl; }

function py_moveToPos() {
    var xVal = document.getElementById("xVal").value;
    var yVal = document.getElementById("yVal").value;
    var zVal = document.getElementById("zVal").value;
    var speed = document.getElementById("robotSpeed").value;

    eel.moveToPosXYZ(xVal,yVal,zVal,speed)();
}

function py_moveToInit() {
    var speed = document.getElementById("robotSpeed").value;
    eel.moveToPosDict('init',speed)();
}

function py_moveToCam() {
    var speed = document.getElementById("robotSpeed").value;
    eel.moveToPosDict('cam',speed)();
}

function py_moveToCalibrate() {
    var speed = document.getElementById("robotSpeed").value;
    eel.moveToCalibrate()();
}

function py_moveToTool() {
    var toolRow = document.getElementById("toolRowIn").value;
    var toolCol = document.getElementById("toolColIn").value;
    var toolPos = toolRow+toolCol;
    eel.moveToToolPos(toolPos)();
}

function py_singleSeq() {
    var toolRow = document.getElementById("toolRowIn").value;
    var toolCol = document.getElementById("toolColIn").value;
    var toolPos = toolRow+toolCol;
    eel.singleSeq(toolPos)();
}

function py_fullSeq() {
    eel.fullSeq()();
}

function py_releaseGripper(){
    eel.gripOFF()();
}