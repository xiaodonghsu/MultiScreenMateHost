#!/usr/bin/env python3
import asyncio
import base64
import json
import logging
import os
import ssl
import tempfile
import pyautogui
import pyperclip
import websockets
import ctypes
from typing import Any
from datetime import datetime
from functions.avatar_switch import sendAvatarText

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
    def __init__(self):
        self.config = self.load_config()
        self.port = self.config.get('host_port', 56789)
        self.host_name = self.config.get('host_name', 'WebSocketServer')
        self.tag_id = self.config.get('tag_id', '')
        self.funasr_host = self.config.get('funasr_host', '')

    async def handle_connection(self, websocket):
        """处理客户端连接"""
        client_ip = websocket.remote_address[0]
        connection_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"客户端连接 - IP: {client_ip}, 时间: {connection_time}")
        
        try:
            async for message in websocket:
                logger.info(f"收到消息: {message[:150]}...")
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
            msg_id = data.get('msg_id')
            client_id = data.get('client_id')
            
            if not msg_id:
                await self.send_error(websocket, "消息ID不能为空")
                return

            if command == 'handshake':
                await self.handle_handshake(websocket, msg_id)
            elif command == 'key' and content:
                await self.handle_key_command(websocket, content, msg_id)
            elif command == 'set' and content:
                await self.handle_set_command(websocket, content, msg_id)
            elif command == 'text' and content:
                await self.handle_text_command(websocket, content, msg_id)
            elif command == 'voice' and content:
                await self.handle_voice_command(websocket, content, msg_id)
            elif command == 'image' and content:
                await self.handle_image_command(websocket, content, msg_id)
            elif command == 'function' and content:
                await self.handle_function_command(websocket, content, msg_id)
            else:
                logger.info(f"未知命令: {command}")
                await self.send_error(websocket, f"未知命令: {command}")
                
        except json.JSONDecodeError:
            await self.send_error(websocket, "JSON格式错误")
        except Exception as e:
            logger.error(f"处理消息时发生错误: {e}")
            await self.send_error(websocket, "服务器内部错误")
    
    async def handle_handshake(self, websocket, msg_id: str):
        """处理握手命令"""
        response = {
            "msg_id": msg_id,
            "result": "success",
            "content": self.config
        }
        await websocket.send(json.dumps(response))
        logger.info(json.dumps(response))
    
    async def handle_key_command(self, websocket, key: str, msg_id: str):
        """处理按键命令"""
        try:
            # 验证按键是否支持
            valid_keys = ['Left', 'Right', 'Space', 'Up', 'Down', 'Enter']
            if key not in valid_keys:
                await self.send_error(websocket, f"不支持的按键: {key}")
                return
                
            # 模拟按键操作
            # 为避免部分101键盘的小键盘num lock键影响上下左右的输出
            # 先检查 num lock 键的状态,如果开启则关闭
            if key in ['Up', 'Down', 'Left', 'Right']:
                if bool(ctypes.windll.user32.GetKeyState(0x90) & 1):
                    pyautogui.press('numlock')

            pyautogui.press(key)
            
            response = {
                "id": msg_id,
                "result": "success"
            }
            await websocket.send(json.dumps(response))
            logger.info(json.dumps(response))
            
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
            new_name = content.get('host_name')
            new_tag_id = content.get('tag_id')
            
            # 检查是否有有效的修改
            if new_name is None and new_tag_id is None:
                await self.send_error(websocket, "未提供有效的修改字段")
                return
            
            # 更新配置
            updated = False
            if new_name is not None and new_name != self.host_name:
                self.host_name = new_name
                self.config['host_name'] = new_name
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
            logger.info(json.dumps(response))
            
        except Exception as e:
            logger.error(f"执行设置命令时发生错误: {e}")
            await self.send_error(websocket, f"设置失败: {str(e)}")
    
    async def handle_text_command(self, websocket, content: str, msg_id: str):
        """处理文本命令"""
        try:
            # 打印语音内容
            logger.info(f"收到文本消息 (ID: {msg_id}): {content}")
            
            # 返回成功响应
            response = {
                "id": msg_id,
                "result": "success"
            }
            await websocket.send(json.dumps(response))
            logger.info(json.dumps(response))
            
        except Exception as e:
            logger.error(f"处理文本命令时发生错误: {e}")
            await self.send_error(websocket, f"文本处理失败: {str(e)}")

    async def handle_voice_command(self, websocket, content: str, msg_id: str):
        """处理语音命令 - 使用FunASR服务进行语音转文字"""
        try:
            # 解码base64语音数据
            logger.info(f"收到语音消息 (ID: {msg_id}): 数据长度 {len(content)}")
            
            # 解码base64
            try:
                audio_data = base64.b64decode(content)
                logger.info(f"Base64解码成功: {len(audio_data)} 字节")
            except Exception as e:
                logger.error(f"Base64解码失败: {e}")
                await self.send_error(websocket, "语音数据格式错误")
                return
            
            # 将语音数据保存为临时文件
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_filename = temp_file.name
            
            logger.info(f"语音数据保存成功: {temp_filename}")

            if self.funasr_host == "":
                logger.error("FunASR服务未配置")
                await self.send_error(websocket, "FunASR服务未配置")
                return

            # 使用FunASR客户端进行语音识别
            text = await self.call_funasr_service(temp_filename, msg_id)

            logger.info("向数字人发送文本消息: %s", text)
            logger.info(sendAvatarText(text))
           
            # 清理临时文件
            try:
                os.unlink(temp_filename)
            except Exception as e:
                logger.info("remove tempfile fail:", e)
                pass
            
            # 指定的位置输入文本
            # if len(text) > 0:
            #     pyperclip.copy(text)
            #     pyautogui.hotkey('ctrl', 'v')

            # 返回成功响应，包含转换的文字
            response = {
                "id": msg_id,
                "result": "success",
                "text": text
            }
            await websocket.send(json.dumps(response))
            logger.info(json.dumps(response))
            
        except Exception as e:
            logger.error(f"处理语音命令时发生错误: {e}")
            await self.send_error(websocket, f"语音处理失败: {str(e)}")

    async def call_funasr_service(self, audio_file_path: str, msg_id: str) -> str:
        """调用FunASR服务进行语音识别"""
        try:
            import asyncio
            import websockets
            import json
            import ssl
            
            # FunASR服务配置（参考funasr_wss_client.py）
            mode = "2pass-online"      #2pass #offline      # 识别模式
            
            # 读取音频文件
            with open(audio_file_path, "rb") as f:
                audio_bytes = f.read()
            
            # 计算音频参数
            sample_rate = 16000
            chunk_size = [5, 10, 5]
            chunk_interval = 10
            stride = int(60 * chunk_size[1] / chunk_interval / 1000 * sample_rate * 2)
            chunk_num = (len(audio_bytes) - 1) // stride + 1
            
            # 连接FunASR服务
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            # uri = "wss://{}:{}".format(funasr_host, funasr_port)
            uri = self.funasr_host
            
            async with websockets.connect(
                uri, subprotocols=["binary"], ping_interval=None, ssl=ssl_context
            ) as websocket:
                
                # 发送初始化消息
                init_message = json.dumps({
                    "mode": mode,
                    "chunk_size": chunk_size,
                    "chunk_interval": chunk_interval,
                    "encoder_chunk_look_back": 4,
                    "decoder_chunk_look_back": 0,
                    "audio_fs": sample_rate,
                    "wav_name": f"voice_{msg_id}",
                    "wav_format": "pcm",
                    "is_speaking": True,
                    "hotwords": "",
                    "itn": True,
                })
                
                await websocket.send(init_message)
                
                # 发送音频数据
                for i in range(chunk_num):
                    beg = i * stride
                    data = audio_bytes[beg : beg + stride]
                    await websocket.send(data)
                    
                    if i == chunk_num - 1:
                        # 发送结束标志
                        end_message = json.dumps({"is_speaking": False})
                        await websocket.send(end_message)
                
                # 接收识别结果
                max_wait_time = 10  # 最大等待时间10秒
                start_time = asyncio.get_event_loop().time()
                asr_text = []
                while True:
                    # 检查是否超时
                    current_time = asyncio.get_event_loop().time()
                    if current_time - start_time > max_wait_time:
                        logger.warning(f"FunASR服务响应超时 (ID: {msg_id})")
                        break
                    
                    try:
                        # 设置接收超时
                        response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                        response_data = json.loads(response)
                        logger.info(f"FunASR识别响应: {response_data}")

                        if "stamp_sents" in response_data:
                            asr_text.append(response_data.get("text", ""))

                        recognized_text = response_data.get("text", "")
                        # 判断结束标记
                        if response_data.get("is_final", False) == True:
                            logger.info(f"FunASR识别结果 (ID: {msg_id}): {recognized_text}")
                            break
                        else:
                            logger.info(f"FunASR识别分段 (ID: {msg_id}): {recognized_text}")

                    except asyncio.TimeoutError:
                        logger.warning(f"等待FunASR响应超时 (ID: {msg_id})")
                        break
                    except websockets.exceptions.ConnectionClosed:
                        logger.warning(f"FunASR连接已关闭 (ID: {msg_id})")
                        break
                    except Exception as e:
                        logger.error(f"接收FunASR响应时发生错误 (ID: {msg_id}): {e}")
                        break
                
                return "".join(asr_text)
                
        except Exception as e:
            logger.error(f"调用FunASR服务失败 (ID: {msg_id}): {e}")
            return f"语音识别服务错误: {str(e)}"
    async def handle_image_command(self, websocket, content: str, msg_id: str):
        logger.info(f"收到图片消息 (ID: {msg_id}): 数据长度 {len(content)}")

    async def handle_function_command(self, websocket, content: str, msg_id: str):
        logger.info(f"收到功能命令 (ID: {msg_id}): {content}")
        try:
            import functions
            func = getattr(functions, content)
            logger.info(f"run function: {func}()")
            run_result = func()
            logger.info(run_result)
            response = {
                "id": msg_id,
                "result": "success",
                "text": f"{run_result}"
            }
            await websocket.send(json.dumps(response))
        except Exception as e:
            logger.info(f"error in run function: {content}:", e)
            response = {
                "id": msg_id,
                "result": "error",
                "text": f"{e}"
            }
            await websocket.send(json.dumps(response))

            

    def load_config(self):
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

    def save_config(self):
        """保存配置到config.json文件"""
        try:
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=4)
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
            
        logger.info(f"主机名称: {self.host_name}")
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
                # 设置更安全的选项
                ssl_context.set_ciphers('ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20:ECDH+AESGCM:DH+AESGCM:ECDH+AES:DH+AES:RSA+AESGCM:RSA+AES:!aNULL:!MD5:!DSS')
                ssl_context.load_cert_chain(cert_file, key_file)
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
                logger.info("SSL上下文创建成功，使用WSS连接")
                return ssl_context
            else:
                logger.warning("未找到SSL证书文件，使用非安全连接")
                logger.info("如需使用WSS，请创建server.crt和server.key文件")
                return None
                
        except Exception as e:
            logger.error(f"创建SSL上下文失败: {e}")
            logger.info("将使用非安全连接")
            return None



async def main():
    """主函数"""
    try:
        server = WebSocketKeyServer()
        await server.start_server()
    except KeyboardInterrupt:
        logger.info("服务器被用户中断")
    except Exception as e:
        logger.error(f"服务器启动失败: {e}")

if __name__ == "__main__":
    import tendo.singleton
    try:
        single = tendo.singleton.SingleInstance()
    except:
        logger.error("Another instance of the program is already running.")
        exit(1)
    # 设置pyautogui安全设置
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1

    asyncio.run(main())