#!/usr/bin/env python3
import asyncio
import json
import logging
import os
import ssl
import pyautogui
import websockets
from typing import Any
from datetime import datetime

# 创建logs目录
logs_dir = "logs"
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# 配置日志文件
log_filename = datetime.now().strftime("server_%Y%m%d_%H%M%S.log")
log_filepath = os.path.join(logs_dir, log_filename)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filepath, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
logger.info(f"日志文件已创建: {log_filepath}")

class WebSocketKeyServer:
    def __init__(self, config: dict[str, Any]):
        self.config = config
        self.port = config.get('port', 56789)
        self.server_name = config.get('name', 'WebSocket Key Server')
        self.tag_id = config.get('tag_id', '')
        
    async def handle_connection(self, websocket):
        """处理客户端连接"""
        client_ip = websocket.remote_address[0]
        connection_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"客户端连接 - IP: {client_ip}, 时间: {connection_time}")
        
        try:
            async for message in websocket:
                await self.handle_message(websocket, message, client_ip)
        except websockets.exceptions.ConnectionClosed:
            disconnect_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"客户端断开连接 - IP: {client_ip}, 连接时间: {connection_time}, 断开时间: {disconnect_time}")
        except Exception as e:
            disconnect_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.error(f"客户端连接异常 - IP: {client_ip}, 连接时间: {connection_time}, 断开时间: {disconnect_time}, 错误: {e}")
    
    async def handle_message(self, websocket, message: str, client_ip: str):
        """处理客户端消息"""
        try:
            data = json.loads(message)
            command = data.get('command')
            content = data.get('content')
            msg_id = data.get('id')
            
            if not msg_id:
                await self.send_error(websocket, "消息ID不能为空")
                return
                
            if command == 'handshake':
                await self.handle_handshake(websocket, msg_id)
            elif command == 'keypress' and content:
                await self.handle_keypress_command(websocket, content, msg_id)
            elif command == 'set' and content:
                await self.handle_set_command(websocket, content, msg_id)
            else:
                await self.send_error(websocket, f"未知命令: {command}")
                
        except json.JSONDecodeError:
            await self.send_error(websocket, "JSON格式错误")
        except Exception as e:
            logger.error(f"处理消息时发生错误: {e}")
            await self.send_error(websocket, "服务器内部错误")
    
    async def handle_handshake(self, websocket, msg_id: str):
        """处理握手命令"""
        response = {
            "id": msg_id,
            "result": "success",
            "name": self.server_name,
            "tag_id": self.tag_id

        }
        await websocket.send(json.dumps(response))
        logger.info(f"握手成功: {msg_id}")
        logger.info(json.dumps(response))
    
    async def handle_keypress_command(self, websocket, key: str, msg_id: str):
        """处理按键命令"""
        try:
            # 验证按键是否支持
            valid_keys = ['Left', 'Right', 'Space', 'Up', 'Down', 'Enter']
            if key not in valid_keys:
                await self.send_error(websocket, f"不支持的按键: {key}")
                return
                
            # 模拟按键操作
            pyautogui.press(key)
            
            response = {
                "id": msg_id,
                "result": "success"
            }
            await websocket.send(json.dumps(response))
            logger.info(f"按键执行成功: {key} (ID: {msg_id})")
            
        except pyautogui.FailSafeException:
            await self.send_error(websocket, "安全保护触发，无法执行按键")
        except Exception as e:
            logger.error(f"执行按键 {key} 时发生错误: {e}")
            await self.send_error(websocket, f"执行按键失败: {key}")
    
    async def handle_set_command(self, websocket, content: dict, msg_id: str):
        """处理设置命令"""
        try:
            # 验证内容格式
            if not isinstance(content, dict):
                await self.send_error(websocket, "内容格式错误，应为字典")
                return
                
            # 获取要修改的字段
            new_name = content.get('name')
            new_tag_id = content.get('tag_id')
            
            # 检查是否有有效的修改
            if new_name is None and new_tag_id is None:
                await self.send_error(websocket, "未提供有效的修改字段")
                return
            
            # 更新配置
            updated = False
            if new_name is not None and new_name != self.server_name:
                self.server_name = new_name
                self.config['name'] = new_name
                updated = True
                logger.info(f"更新服务器名称: {new_name}")
                
            if new_tag_id is not None and new_tag_id != self.tag_id:
                self.tag_id = new_tag_id
                self.config['tag_id'] = new_tag_id
                updated = True
                logger.info(f"更新tag_id: {new_tag_id}")
            
            # 保存配置到文件
            if updated:
                self.save_config()
            
            response = {
                "id": msg_id,
                "result": "success",
                "updated": updated
            }
            await websocket.send(json.dumps(response))
            logger.info(f"设置命令执行成功 (ID: {msg_id})")
            
        except Exception as e:
            logger.error(f"执行设置命令时发生错误: {e}")
            await self.send_error(websocket, f"设置失败: {str(e)}")
    
    def save_config(self):
        """保存配置到config.json文件"""
        try:
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            logger.info("配置已保存到config.json")
        except Exception as e:
            logger.error(f"保存配置失败: {e}")
            raise
    
    async def send_error(self, websocket, error_msg: str):
        """发送错误响应"""
        error_response = {
            "result": "error",
            "message": error_msg
        }
        await websocket.send(json.dumps(error_response))
    
    async def start_server(self):
        """启动WebSocket服务器"""
        # 创建SSL上下文
        ssl_context = self.create_ssl_context()
        
        if ssl_context:
            server = await websockets.serve(
                self.handle_connection, 
                "0.0.0.0", 
                self.port, 
                ssl=ssl_context
            )
            logger.info(f"WSS服务器启动成功，监听端口: {self.port}")
        else:
            server = await websockets.serve(
                self.handle_connection, 
                "0.0.0.0", 
                self.port
            )
            logger.info(f"WS服务器启动成功，监听端口: {self.port}")
            
        logger.info(f"服务名称: {self.server_name}")
        logger.info(f"tag_id: {self.tag_id}")

        # 保持服务器运行
        await server.wait_closed()
    
    def create_ssl_context(self):
        """创建SSL上下文"""
        try:
            # 检查证书文件是否存在
            cert_file = "server.crt"
            key_file = "server.key"
            
            if os.path.exists(cert_file) and os.path.exists(key_file):
                ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
                ssl_context.load_cert_chain(cert_file, key_file)
                return ssl_context
            else:
                logger.warning("未找到SSL证书文件，使用非安全连接")
                logger.info("如需使用WSS，请创建server.crt和server.key文件")
                return None
                
        except Exception as e:
            logger.error(f"创建SSL上下文失败: {e}")
            return None

def load_config():
    """加载配置文件"""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("配置文件 config.json 未找到")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"配置文件格式错误: {e}")
        raise

async def main():
    """主函数"""
    try:
        config = load_config()
        server = WebSocketKeyServer(config)
        await server.start_server()
    except KeyboardInterrupt:
        logger.info("服务器被用户中断")
    except Exception as e:
        logger.error(f"服务器启动失败: {e}")

if __name__ == "__main__":
    # 设置pyautogui安全设置
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1
    
    asyncio.run(main())