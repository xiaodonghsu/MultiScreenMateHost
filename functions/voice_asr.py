class VoiceASR:
    def __init__(self, funasr_host=""):
        self.funasr_host = funasr_host

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
                        print(f"FunASR服务响应超时 (ID: {msg_id})")
                        break
                    
                    try:
                        # 设置接收超时
                        response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                        response_data = json.loads(response)
                        print(f"FunASR识别响应: {response_data}")

                        if "stamp_sents" in response_data:
                            asr_text.append(response_data.get("text", ""))

                        recognized_text = response_data.get("text", "")
                        # 判断结束标记
                        if response_data.get("is_final", False) == True:
                            print(f"FunASR识别结果 (ID: {msg_id}): {recognized_text}")
                            break
                        else:
                            print(f"FunASR识别分段 (ID: {msg_id}): {recognized_text}")

                    except asyncio.TimeoutError:
                        print(f"等待FunASR响应超时 (ID: {msg_id})")
                        break
                    except websockets.exceptions.ConnectionClosed:
                        print(f"FunASR连接已关闭 (ID: {msg_id})")
                        break
                    except Exception as e:
                        print(f"接收FunASR响应时发生错误 (ID: {msg_id}): {e}")
                        break
                
                return "".join(asr_text)
                
        except Exception as e:
            print(f"调用FunASR服务失败 (ID: {msg_id}): {e}")
            return f"语音识别服务错误: {str(e)}"