#!/usr/bin/env python3
import asyncio
import json
import ssl
import websockets

async def test_client(ip_addr: str):
    """测试客户端"""
    uri = f"wss://{ip_addr}:56789"
    
    # 创建SSL上下文，禁用证书验证（仅用于测试）
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    try:
        async with websockets.connect(uri, ssl=ssl_context) as websocket:
            print("连接服务器成功")
            
            # 测试握手命令
            handshake_msg = {
                "command": "handshake",
                "id": "test_handshake_001"
            }
            await websocket.send(json.dumps(handshake_msg))
            print(f"发送握手命令: {handshake_msg}")
            
            response = await websocket.recv()
            print(f"收到响应: {response}")
            
            # 测试按键命令 - Left
            key_msg_left = {
                "id": "test_key_left_001",
                "command": "key",
                "content": "Left"
            }
            await websocket.send(json.dumps(key_msg_left))
            print(f"发送按键命令: {key_msg_left}")
            
            response = await websocket.recv()
            print(f"收到响应: {response}")
            
            # 测试按键命令 - Right
            key_msg_right = {
                "id": "test_key_right_001",
                "command": "key",
                "content": "Right"
            }
            await websocket.send(json.dumps(key_msg_right))
            print(f"发送按键命令: {key_msg_right}")
            
            response = await websocket.recv()
            print(f"收到响应: {response}")
            
            # 测试按键命令 - Space
            key_msg_space = {
                "id": "test_key_space_001",
                "command": "key",
                "content": "Space"
            }
            await websocket.send(json.dumps(key_msg_space))
            print(f"发送按键命令: {key_msg_space}")
            
            response = await websocket.recv()
            print(f"收到响应: {response}")
            
    except Exception as e:
        print(f"客户端错误: {e}")

if __name__ == "__main__":
    asyncio.run(test_client("192.168.41.91"))
    