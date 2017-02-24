# -*- coding:GBK -*-
import serial
import serial.tools.list_ports as st
import Application


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
                Application.sent_all(line)
                # print server
        ser.close()
        print "self conn is down"
        return


if __name__ == '__main__':
    print 'ConnUtils.py __main__'

    lists = list_ava_ports()
    for port in lists:
        print port

        # for i in range(2):
        # //lists = list_ava_ports()
        # print len(lists)
        # serrr = serial.Serial('COM3',9600)
        # #serrr.open()
        # data = serrr.readline()
        # print data
