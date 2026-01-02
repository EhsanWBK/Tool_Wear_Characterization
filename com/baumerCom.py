from opcua.client.client import Client
from opcua.ua import DataValue, Variant, VariantType
import base64
from numpy import frombuffer, uint8
from cv2 import imdecode
from time import sleep

NAMESPACE = 'CameraSpace'

class CamClient:
    def __init__(self, url) -> None:
        print('Initializing Client')
        self.client = Client(url=url, timeout=100000)
        self.client.connect()
        self.client.get_namespace_array()

        self.objects = self.client.get_objects_node()
        self.nodes = self.objects.get_children()
        self.streamNode = self.nodes[1]
        self.flagNode = self.nodes[2]
        self.triggerNode = self.nodes[3]
        print('Nodes found on OPC UA Server:\n',self.nodes)

        self.triggerModeOn= self.triggerNode.get_children()[0]
        self.triggerModeOff = self.triggerNode.get_children()[1]
        self.triggerSet = self.triggerNode.get_children()[2]
        self.triggerImg =  self.triggerNode.get_children()[3]

        self.baumerStream = self.streamNode.get_children()[0]
        self.webcamStream = self.streamNode.get_children()[1]
        self.qrcamStream = self.streamNode.get_children()[2]
        

        self.qrFlag = self.flagNode.get_children()[0]
        self.qrReset = self.flagNode.get_children()[1]

    def getBaumer(self):
        ''' Read out bytestring from Baumer camera stream. '''
        jpegString = self.baumerStream.get_value()
        jpeg = base64.b64decode(jpegString)
        jpegNp = frombuffer(jpeg, dtype=uint8)
        return imdecode(jpegNp, flags=1)
    
    def getWebcam(self):
        ''' Read out bytestring from Webcam stream. '''
        try:
            jpegString = self.webcamStream.get_value()
            jpeg = base64.b64decode(jpegString)
            jpegNp = frombuffer(jpeg, dtype=uint8)
            return imdecode(jpegNp, flags=1)
        except: return None

    def getQR(self):
        qrData = self.qrcamStream.get_value()
        self.qrFlag.set_value(DataValue(Variant(False),VariantType.String))
        return qrData

    def getQRFlag(self):
        return self.qrFlag.get_value()
    
    def getTrigger(self):
        # print(self.triggerSet.get_value())
        return self.triggerSet.get_value()
    
    def setTriggerMode(self, on = False, off = False):
        self.triggerModeOn.set_value(DataValue(Variant(on,VariantType.Boolean)))
        self.triggerModeOff.set_value(DataValue(Variant(off,VariantType.Boolean)))
        
    def receivedTrigger(self):
        sleep(.5)
        self.triggerSet.set_value(DataValue(Variant(False,VariantType.Boolean)))
        jpegString = self.triggerImg.get_value()
        jpeg = base64.b64decode(jpegString)
        jpegNp = frombuffer(jpeg, dtype=uint8)
        return imdecode(jpegNp, flags=1)

    def stopClient(self):
        print('\t- Terminated Client.'); self.client.disconnect()
