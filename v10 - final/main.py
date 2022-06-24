from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, QTime, Qt
from ui_main import Ui_MainWindow  # importing our generated file
import sys
import os
import time
from opcua import Client
import goto
import pyodbc as odbc
import pandas as pd

print('CONNECTING TO KUKA...')
print('.....................')

url = "opc.tcp://192.168.1.1:4840"  #ip address if KLI:4840
client = Client(url)
client.set_user("OpcUaOperator")
client.set_password("kuka")
variablename = "Model"

try:
    client.connect()
    print('KUKA CONNECTED')
    print('.....................')
except Exception as e:
    print(e)
    print('KUKA CONNECT FAILED')
    print('.....................')
    print('RETRY')
    time.sleep(3)
    sys.exit()

print('CONNECTING TO DB...')
print('.....................')

DRIVER = 'SQL Server'
SERVER_NAME = 'DESKTOP-1AVGRC3'
DATABASE_NAME = 'KUKA'

conn_string = f"""
    Driver={{{DRIVER}}};
    Server={SERVER_NAME};
    Database={DATABASE_NAME};
    Trust_Connection=yes;
"""

try:
    conn = odbc.connect(conn_string)
    print('CONNECTED TO DB')
    print('.....................')
except Exception as e:
    print(e)
    print('CONNECTION TERMINTED')
    print('.....................')
    sys.exit()
else:
    cursor = conn.cursor()

print('OPENING UI...')

variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.$ROBNAME[]")
rob_name1 = variableid.get_value()

class mywindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
         
        self.ui.setupUi(self)

        timer = QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(200)

        self.ui.btn_pos_data.clicked.connect(self.btn_pos_data)
        self.ui.btn_mot_data.clicked.connect(self.btn_mot_data)
        self.ui.btn_status.clicked.connect(self.btn_status)
        self.ui.btn_rob_info.clicked.connect(self.btn_rob_info)
        self.ui.btn_report.clicked.connect(self.btn_report)
        self.ui.btn_file_path.clicked.connect(self.btn_file_path)
        self.ui.btn_gen_rep.clicked.connect(self.btn_gen_rep)
        self.ui.btn_exit.clicked.connect(self.btn_page_exit)
        
    def update(self):

        #Axis position values
        
        variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.R1.$AXIS_ACT.A1")
        axis_a1 = variableid.get_value()
        self.ui.axis_a1.setText(str(axis_a1))

        variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.R1.$AXIS_ACT.A2")
        axis_a2 = variableid.get_value()
        self.ui.axis_a2.setText(str(axis_a2))

        variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.R1.$AXIS_ACT.A3")
        axis_a3 = variableid.get_value()
        self.ui.axis_a3.setText(str(axis_a3))

        variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.R1.$AXIS_ACT.A4")
        axis_a4 = variableid.get_value()
        self.ui.axis_a4.setText(str(axis_a4))

        variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.R1.$AXIS_ACT.A5")
        axis_a5 = variableid.get_value()
        self.ui.axis_a5.setText(str(axis_a5))

        variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.R1.$AXIS_ACT.A6")
        axis_a6 = variableid.get_value()
        self.ui.axis_a6.setText(str(axis_a6))

        #TCP position values

        try:     
            variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.R1.$POS_ACT.CartesianCoordinates.X")
            tcp_x = variableid.get_value()
            self.ui.tcp_x.setText(str(tcp_x))

            variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.R1.$POS_ACT.CartesianCoordinates.Y")
            tcp_y = variableid.get_value()
            self.ui.tcp_y.setText(str(tcp_y))

            variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.R1.$POS_ACT.CartesianCoordinates.Z")
            tcp_z = variableid.get_value()
            self.ui.tcp_z.setText(str(tcp_z))
            
            variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.R1.$POS_ACT.Orientation.A")
            tcp_a = variableid.get_value()
            self.ui.tcp_a.setText(str(tcp_a))
            
            variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.R1.$POS_ACT.Orientation.B")
            tcp_b = variableid.get_value()
            self.ui.tcp_b.setText(str(tcp_b))
            
            variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.R1.$POS_ACT.Orientation.C")
            tcp_c = variableid.get_value()
            self.ui.tcp_c.setText(str(tcp_c))

            self.ui.error_tool.setText('')
        
        except Exception as e:
            print(e)
            self.ui.error_tool.setText("Error : Tool not selected")

        #Current Base Number
        
        try:
            variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.R1.$ACT_BASE")
            a_base_no = variableid.get_value()
            self.ui.a_base_no.setText(str(a_base_no))
            self.ui.error_base.setText('')
        except Exception as e:
            print(e)
            self.ui.error_base.setText("Error : Base not selected") 

        #Current Tool Number

        try:
            variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.R1.$ACT_TOOL")
            a_tool_no = variableid.get_value()
            self.ui.a_tool_no.setText(str(a_tool_no))
            self.ui.error_tool.setText('')

        except Exception as e:
            print(e)
            self.ui.error_tool.setText("Error : Tool not selected")

        # Current Tool Data

        try:
            variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.R1.$TOOL.CartesianCoordinates.X")
            a_tool_x = variableid.get_value()
            self.ui.a_tool_x.setText(str(a_tool_x))
            
            variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.R1.$TOOL.CartesianCoordinates.Y")
            a_tool_y = variableid.get_value()
            self.ui.a_tool_y.setText(str(a_tool_y))
            
            variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.R1.$TOOL.CartesianCoordinates.Z")
            a_tool_z = variableid.get_value()
            self.ui.a_tool_z.setText(str(a_tool_z))
            
            variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.R1.$TOOL.Orientation.A")
            a_tool_a = variableid.get_value()
            self.ui.a_tool_a.setText(str(a_tool_a))
            
            variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.R1.$TOOL.Orientation.B")
            a_tool_b = variableid.get_value()
            self.ui.a_tool_b.setText(str(a_tool_b))
            
            variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.R1.$TOOL.Orientation.C")
            a_tool_c = variableid.get_value()
            self.ui.a_tool_c.setText(str(a_tool_c))

            self.ui.error_tool.setText('')

        except Exception as e:
            print(e)
            self.ui.error_tool.setText("Error : Tool not selected")
            
        # Current Base Data

        try:
            variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.R1.$BASE.CartesianCoordinates.X")
            a_base_x = variableid.get_value()
            self.ui.a_base_x.setText(str(a_base_x))
            
            variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.R1.$BASE.CartesianCoordinates.Y")
            a_base_y = variableid.get_value()
            self.ui.a_base_y.setText(str(a_base_y))

            variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.R1.$BASE.CartesianCoordinates.Z")
            a_base_z = variableid.get_value()
            self.ui.a_base_z.setText(str(a_base_z))
            
            variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.R1.$BASE.Orientation.A")
            a_base_a = variableid.get_value()
            self.ui.a_base_a.setText(str(a_base_a))

            variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.R1.$BASE.Orientation.B")
            a_base_b = variableid.get_value()
            self.ui.a_base_b.setText(str(a_base_b))

            variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.R1.$BASE.Orientation.C")
            a_base_c = variableid.get_value()
            self.ui.a_base_c.setText(str(a_base_c))

            self.ui.error_base.setText('')
        
        except Exception as e:
            print(e)
            self.ui.error_base.setText("Error : Base not selected") 
        
        #Motor current values

        variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.$CURR_ACT[]")
        mot_cur = variableid.get_value()
        self.ui.cur_a1.setText(str(mot_cur[0]))
        self.ui.cur_a2.setText(str(mot_cur[1]))
        self.ui.cur_a3.setText(str(mot_cur[2]))
        self.ui.cur_a4.setText(str(mot_cur[3]))
        self.ui.cur_a5.setText(str(mot_cur[4]))
        self.ui.cur_a6.setText(str(mot_cur[5]))

        #Motor torque values

        variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.R1.$TORQUE_AXIS_ACT[]")
        mot_tor = variableid.get_value()
        self.ui.tor_a1.setText(str(mot_tor[0]))
        self.ui.tor_a2.setText(str(mot_tor[1]))
        self.ui.tor_a3.setText(str(mot_tor[2]))
        self.ui.tor_a4.setText(str(mot_tor[3]))
        self.ui.tor_a5.setText(str(mot_tor[4]))
        self.ui.tor_a6.setText(str(mot_tor[5]))

        #Motor temperature values

        variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.$MOT_TEMP[]")
        mot_temp = variableid.get_value()
        self.ui.temp_a1.setText(str(mot_temp[0]))
        self.ui.temp_a2.setText(str(mot_temp[1]))
        self.ui.temp_a3.setText(str(mot_temp[2]))
        self.ui.temp_a4.setText(str(mot_temp[3]))
        self.ui.temp_a5.setText(str(mot_temp[4]))
        self.ui.temp_a6.setText(str(mot_temp[5]))

        #override

        variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.$OV_JOG")
        ov_jog = variableid.get_value()
        self.ui.ov_jog.setText(str(ov_jog)+'%')

        variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.$OV_PRO1")
        ov_prg = variableid.get_value()
        self.ui.ov_prg.setText(str(ov_prg)+'%')

        #op_mode

        variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.$MODE_OP.RawValue")
        mode_op = variableid.get_value()
        mode_op = mode_op[1:]
        self.ui.mode_op.setText(str(mode_op))

        #prg_run_mode
        
        variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.$PRO_MODE.RawValue")
        mode_prg = variableid.get_value()
        mode_prg = mode_prg[1:]
        self.ui.mode_prg.setText(str(mode_prg))

        #emergency
        
        variableid = client.get_node("ns=6;s=MotionDeviceSystem.SafetyStates.SafetyState_1.ParameterSet.EmergencyStop")
        emg_stat = variableid.get_value()
        if emg_stat == 1:
            emer_stat_string = 'PRESSED'; 
            self.ui.emg_stat.setText(emer_stat_string)
        else:
            emer_stat_string = 'RELEASED'; 
            self.ui.emg_stat.setText(emer_stat_string)

        #enabling device
        
        variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.$SAFETY_SW.RawValue")
        enb_dev = variableid.get_value()
        enb_dev = enb_dev[1:]
        self.ui.enb_dev.setText(str(enb_dev))

        #robot status
        
        variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.STEU.MADA.$MACHINE.$PRO_MOVE")
        rob_stat = variableid.get_value()
        if rob_stat == 1:
            rob_stat_string = "MOVING"; 
            self.ui.rob_stat.setText(rob_stat_string)
        else:
            rob_stat_string = "STOPPED"; 
            self.ui.rob_stat.setText(rob_stat_string)

        #program status
        
        variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.$PRO_STATE.RawValue")
        prg_stat = variableid.get_value()
        prg_stat = prg_stat[1:]
        prg_stat = str(prg_stat)
        self.ui.prg_stat.setText(str(prg_stat))

        #program select
        
        variableid = client.get_node("ns=6;s=MotionDeviceSystem.Controllers.KRC.TaskControls.Robot.ParameterSet.ExecutionCommandPointer.Module")
        prg_sel = variableid.get_value()
        self.ui.prg_sel.setText(str(prg_sel))
        
        #sql logging

        insert_statement = """
             INSERT INTO [dbo].[Table_1]([Robot_Name],[Axis_A1],[Axis_A2],[Axis_A3]
 ,[Axis_A4],[Axis_A5],[Axis_A6],[TCP_X],[TCP_Y],[TCP_Z],[TCP_A],[TCP_B],[TCP_C],[Active_Tool_No],[Active_Base_No]
 ,[Active_Tool_X],[Active_Tool_Y],[Active_Tool_Z],[Active_Tool_A],[Active_Tool_B],[Active_Tool_C]
 ,[Active_Base_X],[Active_Base_Y],[Active_Base_Z],[Active_Base_A],[Active_Base_B],[Active_Base_C]
 ,[Emergency_State],[Enabling_Device],[Robot_State],[Program_State],[Program_Select]
 ,[Operation_Mode],[Program_Run_Mode],[Jog_Override],[Program_Override],[Axis1_Current],[Axis2_Current]
 ,[Axis3_Current],[Axis4_Current],[Axis5_Current],[Axis6_Current],[Axis1_Torque],[Axis2_Torque]
 ,[Axis3_Torque],[Axis4_Torque],[Axis5_Torque],[Axis6_Torque],[Axis1_Temperature]
 ,[Axis2_Temperature],[Axis3_Temperature],[Axis4_Temperature],[Axis5_Temperature],[Axis6_Temperature])
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
         """
        
        try:
            record = [rob_name1,axis_a1,axis_a2,axis_a3,axis_a4,axis_a5,axis_a6,tcp_x,tcp_y,tcp_z,tcp_a,tcp_b,tcp_c,a_tool_a,a_base_no,a_tool_x,a_tool_y,a_tool_z,a_tool_a,a_tool_b,a_tool_c,a_base_x,a_base_y,a_base_z,a_base_a,a_base_b,a_base_c,emer_stat_string,enb_dev,rob_stat_string,prg_stat,prg_sel,mode_op,mode_prg,ov_jog,ov_prg,mot_cur[0],mot_cur[1],mot_cur[2],mot_cur[3],mot_cur[4],mot_cur[5],mot_tor[0],mot_tor[1],mot_tor[2],mot_tor[3],mot_tor[4],mot_tor[5],mot_temp[0],mot_temp[1],mot_temp[2],mot_temp[3],mot_temp[4],mot_temp[5]]
        except Exception as e:
            print(e)
            self.ui.sql_stat.setText('<p style="font-size:10pt; color: rgb(255, 0, 0);">SQL Status : Not logging</p>')

        try:
            cursor.execute(insert_statement,record)
            self.ui.sql_stat.setText('<p style="font-size:10pt; color: rgb(0, 255, 0);">SQL Status : Logging</p>')
        except Exception as e:
            cursor.rollback()
            print(e)
            self.ui.sql_stat.setText('<p style="font-size:10pt; color: rgb(255, 0, 0);">SQL Status : Not logging</p>')
        else:
            cursor.commit()

    def btn_pos_data(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_pos_data)

    def btn_mot_data(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_mot_data)

    def btn_status(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_status)

    def btn_rob_info(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_rob_info)

        #battery_status
        
        variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.$ACCU_STATE.RawValue")
        bat_status = variableid.get_value()
        bat_status = bat_status[1:]
        self.ui.bat_status.setPlainText(str(bat_status))
    
        #robot_info

        variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.$ROBNAME[]")
        rob_name = variableid.get_value()
        self.ui.rob_name.setPlainText(str(rob_name))
        
        variableid = client.get_node("ns=6;s=MotionDeviceSystem.ProcessData.SYSTEM.$KR_SERIALNO")
        kr_ser = variableid.get_value()
        self.ui.kr_ser.setPlainText(str(kr_ser))

        variableid = client.get_node("ns=6;s=MotionDeviceSystem.Controllers.KRC.Model")
        kc_mod = str(variableid.get_value())
        kc_mod = kc_mod[44:]
        kc_mod = kc_mod[:5]
        self.ui.kc_mod.setPlainText(kc_mod)

        variableid = client.get_node("ns=6;s=MotionDeviceSystem.Controllers.KRC.Software.KSS.Description")
        kss_ver = variableid.get_value()
        self.ui.kss_ver.setPlainText(str(kss_ver))
        
        variableid = client.get_node("ns=6;s=MotionDeviceSystem.Controllers.KRC.Software.KUKA.DeviceConnector.Model")
        soft1 = str(variableid.get_value())
        soft1 = soft1[44:]
        soft1 = soft1[:20]
        variableid = client.get_node("ns=6;s=MotionDeviceSystem.Controllers.KRC.Software.KUKA.DeviceConnector pre-installed.Model")
        soft2 = str(variableid.get_value())
        soft2 = soft2[44:]
        soft2 = soft2[:34]
        soft = soft1 + ', ' + soft2
        self.ui.kss_soft.setPlainText(str(soft))

        variableid = client.get_node("ns=6;s=MotionDeviceSystem.Controllers.KRC.ParameterSet.IpAddress")
        rob_ip = str(variableid.get_value())
        self.ui.rob_ip.setPlainText(rob_ip)
        
    def btn_report(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_report)

    def btn_file_path(self):
        dialog = QFileDialog()
        fol_dir = dialog.getExistingDirectory(self, 'Select path')
        #print(fol_dir)
        self.ui.textEdit_file_path.setPlainText(str(fol_dir))
        
    def btn_gen_rep(self):
        start_date1=self.ui.dateEdit_start.date()
        start_date1=str(start_date1)
        splitting = start_date1.split(',')
        splitting2=splitting[0].split('(')
        splitting3=splitting[2].split(')')
        start_date=splitting2[1] + '-' + splitting[1][1:] + '-' + splitting3[0][1:]

        end_date1=self.ui.dateEdit_end.date()
        end_date1=str(end_date1)
        splitting = end_date1.split(',')
        splitting2=splitting[0].split('(')
        splitting3=splitting[2].split(')')
        end_date=splitting2[1] + '-' + splitting[1][1:] + '-' + splitting3[0][1:]
        
        file_name=self.ui.textEdit_file_name.toPlainText()
        file_path=self.ui.textEdit_file_path.toPlainText()

        start_date=start_date+' 00:00:00.000'
        end_date=end_date+' 23:59:59.999'
        #print(start_date)
        #print(end_date)
        query='SELECT * FROM [KUKA].[dbo].[Table_1] WHERE EntryTimestamp BETWEEN '+"'"+start_date+"' AND '"+end_date+"'"
        #print(query)
        sql_query = pd.read_sql_query(query,conn)
        df = pd.DataFrame(sql_query)
        if df.empty:
            msg = '<p style="font-size:10pt; color: #FFF;">No records found on selected dates</p>'
            QMessageBox.about(self, "Error", msg)
            return
        if not file_path:
            msg = '<p style="font-size:10pt; color: #FFF;">File path not selected</p>'
            QMessageBox.about(self, "Error", msg)
            return
        if not file_name:
            msg = '<p style="font-size:10pt; color: #FFF;">File name not entered</p>'
            QMessageBox.about(self, "Error", msg)
            return
            
        #print(file_path)
        file_name = file_name + '.csv'
        #print(file_name)
        try:
            df.to_csv (os.path.join(file_path,file_name), index = False)
            msg = '<p style="font-size:10pt; color: #FFF;">File export completed</p>'
            QMessageBox.about(self, "Error", msg)
            return
        except Exception as e:
            print(e)
            msg = '<p style="font-size:10pt; color: #FFF;">File not exported</p>'
            QMessageBox.about(self, "Error", msg)
            return

    def btn_page_exit(self):
        print('DISCONNECTING DB...')
        cursor.close()
        print('EXITING...')
        time.sleep(1)
        sys.exit()

def gui():
    app = QtWidgets.QApplication([])
    application = mywindow()
    #application.showFullScreen()
    application.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    gui()
