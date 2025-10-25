#!/usr/bin/env python3
import asyncio
import json
import ssl
import websockets

async def test_client():
    """测试客户端"""
    # uri = "wss://d16.nps.uassist.cn:59132"
    uri = "wss://0.tcp.jp.ngrok.io:13631"
    
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
            
            # 测试设置命令 - 修改name和tag_id
            # set_msg = {
            #     "id": "test_set_001",
            #     "command": "set",
            #     "content": {
            #         "name": "测试服务器名称",
            #         "tag_id": "013018938419238"
            #     }
            # }
            # await websocket.send(json.dumps(set_msg))
            # print(f"发送设置命令: {set_msg}")
            
            # response = await websocket.recv()
            # print(f"收到响应: {response}")
            
            # 测试设置命令 - 只修改name
            # set_name_msg = {
            #     "id": "test_set_002",
            #     "command": "set",
            #     "content": {
            #         "name": "新服务器名称"
            #     }
            # }
            # await websocket.send(json.dumps(set_name_msg))
            # print(f"发送设置命令: {set_name_msg}")
            
            # response = await websocket.recv()
            # print(f"收到响应: {response}")
            
            # # 测试设置命令 - 只修改tag_id
            # set_tag_msg = {
            #     "id": "test_set_003",
            #     "command": "set",
            #     "content": {
            #         "tag_id": "987654321098765"
            #     }
            # }
            # await websocket.send(json.dumps(set_tag_msg))
            # print(f"发送设置命令: {set_tag_msg}")
            
            # response = await websocket.recv()
            # print(f"收到响应: {response}")
            
            # 测试get命令 - 获取当前配置
            get_msg = {
                "id": "test_get_001",
                "command": "get"
            }
            await websocket.send(json.dumps(get_msg))
            print(f"发送获取配置命令: {get_msg}")
            
            response = await websocket.recv()
            print(f"收到响应: {response}")
            
            # 再次握手查看更新后的配置
            handshake_msg2 = {
                "command": "handshake",
                "id": "test_handshake_002"
            }
            await websocket.send(json.dumps(handshake_msg2))
            print(f"发送握手命令查看更新: {handshake_msg2}")
            
            response = await websocket.recv()
            print(f"收到响应: {response}")
            
    except Exception as e:
        print(f"客户端错误: {e}")

if __name__ == "__main__":
    asyncio.run(test_client())
    