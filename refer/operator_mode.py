#even after importing the OPCUA library the error occurs of the buffer size and timeout. 
#need to do change for value of the following variable in the C:\Python\Python38-32\Lib\site-packages\opcua\client\client.py file 
#self.secure_channel_timeout = 3600000
#self.max_messagesize = 2159607808  


from opcua import Client
import time

url = "opc.tcp://192.168.1.1:4840"  #ip address if KLI:4840

client = Client(url)

client.set_user("OpcUaOperator")
client.set_password("kuka")
client.connect()

print ("Connected")

while 1 :
    
    variablename = "Model"
    variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.$MODE_OP.RawValue")
    variabledata = variableid.get_value()
    variabledata = variabledata[1:]
    print('Mode:',variabledata)


    print('------------')
    time.sleep(1)

    
