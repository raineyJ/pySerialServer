# -*- coding:gbk -*-
import wx
# import SerialUtils as mycu
import threading
import serial
import serial.tools.list_ports as st
import websocket_server

global connstatus
global server
global serialport
global testvalue
testvalue = 24


def new_client(client, server):
    print("New client connected and was given id %d" % client['id'])
    server.send_message_to_all("Hey all, a new client has joined us")


def client_left(client, server):
    print("Client(%d) disconnected" % client['id'])


def message_received(client, server, message):
    if len(message) > 200:
        message = message[:200] + '..'
    print("Client(%d) said: %s" % (client['id'], message))


# ��ʼ��server serialport
def __init__ser():
    global server, serialport
    server = websocket_server.WebsocketServer(12315)
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)
    # ����
    serialport = MySerialPort()


def sent_all(msg):
    global server
    print 'L40:' + msg
    server.send_message_to_all(msg)


class ExamplePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        # self.quote = wx.StaticText(self, label="Your quote :", pos=(20, 30))

        # A multiline TextCtrl - This is here to show how the events work in this program don't need to care
        self.logger = wx.TextCtrl(self, pos=(350, 50), size=(300, 400), style=wx.TE_MULTILINE | wx.TE_READONLY)

        self.clearbtn = wx.Button(self, id=100, label="���", pos=(350, 460))
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.clearbtn)

        # A button
        self.button = wx.Button(self, id=101, label="test", pos=(200, 365))
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button)

        # conn/dis Button
        self.connflag = True
        #self.connbtn = wx.Button(self, id=102, label="���Ӵ���", pos=(40, 150))
        #self.disconnbtn = wx.Button(self, id=103, label="�Ͽ�����", pos=(180, 150))
        #self.disconnbtn.Enable(False)
        #self.Bind(wx.EVT_BUTTON, self.OnClick, self.connbtn)
        #self.Bind(wx.EVT_BUTTON, self.OnClick, self.disconnbtn)

        # server on/off Btn
        #self.seron = wx.Button(self, id=104, label="����server", pos=(40, 300))
        # self.seroff = wx.Button(self, id=105, label="�ر�server", pos=(180, 300))
        #self.Bind(wx.EVT_BUTTON, self.OnClick, self.seron)
        # self.Bind(wx.EVT_BUTTON, self.OnClick, self.seroff)

        # the combobox Control
        self.sampleList = ['friends', 'advertising', 'web search', 'Yellow Pages']

        self.portsList = []
        tempList = list_ava_ports()

        for port in tempList:
            if port[1]:
                self.portsList.append(port[0] + ':  true')
            else:
                self.portsList.append(port[0] + ':  false')

        self.lblhear = wx.StaticText(self, label="����ѡ��", pos=(20, 15))
        self.connrefresh = wx.Button(self, id=109, label="ˢ�´���", pos=(20, 65))
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.connrefresh)
        self.edithear = wx.ComboBox(self, pos=(100, 12), size=(500, -1), choices=self.portsList, style=wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.edithear)
        self.Bind(wx.EVT_COMBOBOX, self.EvtCheckBox, self.edithear)

    # ���¼�
    # def EvtText(self,event):
    #     self.logger.AppendText('EventText:%s\n'% event.GetString())

    def EvtComboBox(self, event):
        self.logger.AppendText('EvtComboBox: %s\n' % event.GetString())
        # print event.GetString()[0:4]

    def OnClick(self, event):
        global connstatus, server, serialport

        self.logger.AppendText(" Click on object with Id %d\n" % event.GetId())
        evtid = event.GetId()
        if evtid == 100:  # ���
            self.logger.Clear()
            return

        if evtid == 101:  # test
            print self.edithear.GetValue()
            sent_all('test msg from server')
            return

        # if evtid == 102:  # ��������
        #
        #     # У���Ƿ���ѡ�񴮿�
        #     if self.edithear.CurrentSelection == -1:
        #         dlg = wx.MessageDialog(self, "��ѡ�񴮿�", "About Sample Editor", wx.OK)
        #         dlg.ShowModal()  # Show it
        #         dlg.Destroy()  #
        #         print 'port Name is empty by selection'
        #         return
        #
        #     # ��ȡ��ѡֵ
        #     tempvalue = self.edithear.GetValue()
        #     # ��ȡ�˿����� & �˿�״̬
        #     portname = tempvalue[0:4]
        #     status = tempvalue[-4:]
        #     print 'portname:', portname, 'status:', status
        #
        #     # �ж϶˿��Ƿ����
        #     if status in 'true':
        #         print 'status is in true'
        #
        #         # �������Ӷ˿ڰ�ť & ���öϿ��˿ڰ�ť
        #         self.connbtn.Enable(False)
        #         self.disconnbtn.Enable(True)
        #
        #         # ���ö˿�����
        #         serialport.portName = portname
        #         print 'line 135:', serialport.portName, serialport
        #
        #         th1 = threading.Thread(target=serialport.conn)
        #         serialport.flag = True
        #         print 'th1obj::', th1
        #         th1.start()
        #         print serialport
        #
        #     # �˿ڲ�����
        #     else:
        #         print 'status is in false'
        #         dlg = wx.MessageDialog(self, "�˿��ѱ�ռ�ã���ѡ�������˿�", "About Sample Editor", wx.OK)
        #         dlg.ShowModal()  # Show it
        #         dlg.Destroy()  #
        #         return
        #
        # if evtid == 103:  # �رմ���
        #     self.connbtn.Enable(True)
        #     self.disconnbtn.Enable(False)
        #     serialport.flag = False
        #     print u'�رմ���', serialport, 'flag:', serialport.flag
        #     return
        #
        # if evtid == 104:  # ����server
        #
        #     print 'line 161:', server
        #     th1 = threading.Thread(target=server.run_forever)
        #     th1.setDaemon(True)
        #     th1.start()
        #
        #     self.seron.Enable(False)
        #     return
        #
        # if evtid == 105:  # �ر�server
        #     print server
        #     server.server_close()
        #     return

        if evtid == 109:  # refresh �����б�
            print 'refresh btn'
            temports = list_ava_ports()
            appendList = []
            for port in temports:
                if port[1]:
                    appendList.append(port[0] + ':  true')
                else:
                    appendList.append(port[0] + ':  false')
                self.edithear.Clear()
            self.edithear.AppendItems(appendList)

    def EvtCheckBox(self, event):
        self.logger.AppendText("EvtCheckBox: %s\n" % event.GetString())
        self.logger.AppendText('EvtCheckBox: %d\n' % event.Checked())
        # 1.���Ӵ���
        # ��ȡ��ѡֵ
        tempvalue = self.edithear.GetValue()
        # ��ȡ�˿����� & �˿�״̬
        portname = tempvalue[0:4]
        status = tempvalue[-4:]
        print 'portname:', portname, 'status:', status

        # �ж϶˿��Ƿ����
        if status in 'true':
            print 'status is in true'

            # �������Ӷ˿ڰ�ť & ���öϿ��˿ڰ�ť
            # self.connbtn.Enable(False)
            # self.disconnbtn.Enable(True)

            # ���ö˿�����
            serialport.portName = portname
            print 'line 135:', serialport.portName, serialport

            th1 = threading.Thread(target=serialport.conn)
            serialport.flag = True
            print 'th1obj::', th1
            th1.start()
            print serialport

            # 2.����server
            print 'line 161:', server
            th1 = threading.Thread(target=server.run_forever)
            th1.setDaemon(True)
            th1.start()

            #self.seron.Enable(False)
            return

        # �˿ڲ�����
        else:
            print 'status is in false'
            dlg = wx.MessageDialog(self, "�˿��ѱ�ռ�ã���ѡ�������˿�", "About Sample Editor", wx.OK)
            dlg.ShowModal()  # Show it
            dlg.Destroy()  #
            return



    #def EvtSelectSerial(self, event):


# serialutils
# import Application

def check(port):
    try:
        ser = serial.Serial(port, 9600)
        return ser.isOpen()
    except serial.serialutil.SerialException:
        return False
    finally:
        pass


# ��ȡ���ж˿�
def get_ports():
    return list(st.comports())


"""
������¼����������Ƿ����
[<serial.tools.list_ports_common.ListPortInfo>,True/False]
"""


# У��˿��Ƿ�ռ��
def list_ava_ports():
    ports = get_ports()
    ava_ports = []
    if len(ports) <= 0:
        print "THE SERIAL PORT NOT FOUND"
        return ava_ports
    else:
        print len(ports)
        for port in ports:
            res = check(port[0])
            # ava_ports.append([port, res])
            ava_ports.append([' '.join([port.device, port.description]), res])
        return ava_ports


# �Զ��崮����
class MySerialPort:
    portName = ''
    br = 0
    to = 0
    flag = True

    def __init__(self, name='COM1', b=9600, t=0.1):
        self.portName = name
        self.br = b
        self.to = t

    def conn(self):
        ser = serial.Serial(self.portName, self.br, timeout=self.to)
        print '### conn is on:\t conn to %s, at rate=%s and timeout=%s' % (self.portName, self.br, self.to)
        while self.flag:
            line = ser.readline()
            if len(line) != 0:
                print 'msg:', line
                sent_all(line)
                # print server
        ser.close()
        print "self conn is down"
        return

if __name__ == '__main__':
    __init__ser()
    app = wx.App(False)
    frame = wx.Frame(None, size=(700, 600))
    panel = ExamplePanel(frame)
    frame.Show()
    app.MainLoop()
