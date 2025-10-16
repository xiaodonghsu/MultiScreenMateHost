@echo off
echo 正在安装依赖...
pip install -r requirements.txt

echo 启动WebSocket服务器...
python server.py

pause