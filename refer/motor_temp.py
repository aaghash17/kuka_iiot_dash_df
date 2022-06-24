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
    variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.$MOT_TEMP[]")
    variabledata = variableid.get_value()
    print('Axis1:',variabledata[0])
    print('Axis2:',variabledata[1])
    print('Axis3:',variabledata[2])
    print('Axis4:',variabledata[3])
    print('Axis5:',variabledata[4])
    print('Axis6:',variabledata[5])

    print('------------')
    time.sleep(1)

    
