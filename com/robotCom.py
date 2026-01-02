''' ## Communication with HORST600 
Creating OPC UA Client listening to server. '''

from opcua.client.client import Client
from opcua.ua import DataValue, Variant, VariantType

LOCAL_URL = "opc.tcp://127.0.0.1:12345"
URL = "opc.tcp://172.22.192.172:12345"
# URL = LOCAL_URL # connection locally for debugging; Server must be hosted

class HorstClient:

    def __init__(self) -> None:
        self.client = Client(url=URL)
        self.client.connect()
        self.client.get_namespace_array()
        self.objects = self.client.get_objects_node()
        self.nodes = self.objects.get_children()

        self.resultNode = self.nodes[1]
        self.resStatus = self.resultNode.get_children()[0]
        self.resTypeBool = self.resultNode.get_children()[1]
        self.resTypeFloat = self.resultNode.get_children()[2]
        self.resValBool = self.resultNode.get_children()[3]
        self.resValFloat = self.resultNode.get_children()[4]

        self.commNode = self.nodes[2]
        self.commStatus = self.commNode.get_children()[0]
        self.commTypeBool = self.commNode.get_children()[1]
        self.commTypeFloat = self.commNode.get_children()[2]
        self.commTypeString = self.commNode.get_children()[3]
        self.commCommand = self.commNode.get_children()[4]
        self.commValBool = self.commNode.get_children()[5]
        self.commValFloat = self.commNode.get_children()[6]
        self.commValString = self.commNode.get_children()[7]

        self.flagNode = self.nodes[3]
        self.operating = self.flagNode.get_children()[0]

    def sendCmd(self, cmd, val=[0.0,0.0]):
        self.commStatus.set_value(DataValue(Variant(True, VariantType.Boolean)))
        self.commCommand.set_value(DataValue(Variant(cmd, VariantType.String)))
        if type(val)==bool:
            self.commTypeBool.set_value(DataValue(Variant(True, VariantType.Boolean)))
            self.commValBool.set_value(DataValue(Variant(val, VariantType.Boolean)))
            return True
        if type(val)==list:
            if type(val[-1])==str: 
                self.commTypeString.set_value(DataValue(Variant(True, VariantType.Boolean)))
                self.commValString.set_value(DataValue(Variant(val.pop(), VariantType.String)))
            self.commTypeFloat.set_value(DataValue(Variant(True, VariantType.Boolean)))
            self.commValFloat.set_value(DataValue(Variant(val, VariantType.Float)))
            return True
        return False

    def readResult(self):
        try:
            if self.resStatus.get_value():
                if self.resTypeBool.get_value(): result = self.resValBool.get_value()
                elif self.resTypeFloat.get_value(): result = self.resValFloat.get_value()
                else: 
                    print('No Command could be matched')
                    result = None
                self.resetResult()
                return True, result
            else: return False, None
        except: return False, None
        
    def resetResult(self):
        self.resStatus.set_value(DataValue(Variant(False, VariantType.Boolean)))
        self.resTypeBool.set_value(DataValue(Variant(False, VariantType.Boolean)))
        self.resTypeFloat.set_value(DataValue(Variant(False, VariantType.Boolean)))
        self.resValBool.set_value(DataValue(Variant(False, VariantType.Boolean)))
        self.resValFloat.set_value(DataValue(Variant([0.0], VariantType.Float)))

    def isRunning(self):
        return self.operating.get_value()

    def stopClient(self):
        self.client.disconnect()
