# pySerialServer
a local websocket server link serial port to webpage on windows OS.
通过在本地启动websocket的小服务器，从而实现网页和串口通信的目的，websocket为长连接。理论上启动了websocket服务器后，只要刷新网页就可以重连接。
需要的依赖包为：
* <a href="https://github.com/Pithikos/python-websocket-server/">websocket-server</a> websocket server模块
* <a href="https://www.wxpython.org/">wxpython</a> gui界面模块
* <a href="https://pypi.python.org/pypi/pyserial">pyserial</a> 串口模块
* <a href="http://www.py2exe.org/>py2exe</a> 打包模块
* 此外需要<a href="http://www.microsoft.com/en-us/download/details.aspx?id=15336">VC2008</a> 注意给的依赖为64，32位没测试过

