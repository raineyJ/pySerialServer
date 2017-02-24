from distutils.core import setup
import py2exe
# import serial
import serial.tools.list_ports
from glob import glob

data_files = [
    ("Microsoft.VC90.CRT", glob(r'C:\Program Files (x86)\Microsoft.VC90.CRT\*.*'))]
setup(data_files=data_files)

setup(console=[r'D:\work\python\PyCharmProjects\SerialServer\package\Application.py'],
      options={"py2exe": {"dll_excludes": ["MSVCP90.dll"]  # , "bundle_files": 1
                          }})

# serial.VERSION
# setup(console=[r'D:\work\python\PyCharmProjects\SerialServer\package\SerialUtils.py'],
#       options={"py2exe": {"includes": ["serial"]}})
#
# setup(console=[r'D:\work\python\PyCharmProjects\SerialServer\package\SerialUtils.py'])
