# MultiScreenMate Host Server

**主程序：server.py**

一个基于 Python 的 WebSocket 服务器，用于来自客户端的按键、语音、图片、文本等；并执行系统按键操作。

## 功能特性

- WebSocket 协议通信
- 支持握手验证
- 执行系统按键命令
- 可配置端口和服务名称

## 安装依赖

```bash
pip install -r requirements.txt
```

## 快速上手

### 1. 配置服务器信息

复制 `config_template.json` 为 `config.json` 文件：

- `port`: WebSocket 服务端口
- `host_name`: 服务器名称（握手时返回）
- `tag_id`: NFC的id（握手时返回）
- `funasr_host`: funasr 的服务协议及地址

### 2. 安卓wss要求加密，制作server的证书

```bash
python generate_cert.py
```

### 3. 启动服务器

运行主程序：
```bash
python server.py
```

## 客户端-服务端协议

### 1. 握手命令

客户端发送：
```json
{
  "client_id": "unique_client_id",
  "msg_id": "unique_message_id",
  "command": "handshake"
}
```

服务端响应：
```json
{
  "msg_id": "unique_message_id",
  "result": "success",
  "content": { 
    "name": "server_name",
    "tag_id": "tag_id",
    "functions": [
        {"name": "人工", "function": "switchToManualMode"},
        {"name": "协同", "function": "switchToCollabrateMode"},
        {"name": "自动", "function": "switchToAutoMode"}
      ]
  }
}
```

### 2. 设置服务端信息命令

客户端发送：
```json
{
  "client_id": "unique_client_id",
  "msg_id": "unique_message_id",
  "command": "set",
  "content": {
    "name": "new_server_name",
    "tag_id": "new_tag_id"
  }
}
```

服务端响应：
```json
{
  "msg_id": "unique_message_id",
  "result": "success"/"error",
  "content": "错误描述"
}
```

### 3. 按键命令

客户端发送：
```json
{
  "client_id": "unique_client_id",
  "msg_id": "unique_message_id",
  "command": "key",
  "content": "PageUp"
}
```

服务端响应：
```json
{
  "msg_id": "unique_message_id",
  "result": "success"/"error",
  "content": "错误描述"
}
```

### 4. 鼠标命令

客户端发送：
```json
{
  "client_id": "unique_client_id",
  "msg_id": "unique_message_id",
  "command": "mouse",
  "content": {
    "x": 100,
    "y": 200, 
    "button": "left"
  }
}
```

服务端响应：
```json
{
  "msg_id": "unique_message_id",
  "result": "success"/"error",
  "content": "错误描述"
}
```

### 5. 文本命令

客户端发送：
```json
{
  "client_id": "unique_client_id",
  "msg_id": "unique_message_id",
  "command": "text",
  "content": "文本内容"
}
```

服务端响应：
```json
{
  "msg_id": "unique_message_id",
  "result": "success"/"error",
  "content": "错误描述"
}
```

### 6. 语音命令

客户端发送：
```json
{
  "client_id": "unique_client_id",
  "msg_id": "unique_message_id",
  "command": "voice",
  "content": "语音的BASE64编码"
}
```

服务端响应：
```json
{
  "msg_id": "unique_message_id",
  "result": "success"/"error",
  "content": "错误描述"
}
```

### 7. 图片命令

客户端发送：
```json
{
  "client_id": "unique_client_id",
  "msg_id": "unique_message_id",
  "command": "image",
  "content": "图片的BASE64编码"
}
```

服务端响应：
```json
{
  "msg_id": "unique_message_id",
  "result": "success"/"error",
  "content": "错误描述"
}
```

### 8. 图片命令

客户端发送：
```json
{
  "client_id": "unique_client_id",
  "msg_id": "unique_message_id",
  "command": "function",
  "content": "function content"
}
```

服务端响应：
```json
{
  "msg_id": "unique_message_id",
  "result": "success"/"error",
  "content": "错误描述"
}
```

### 支持的按键

支持所有 `pyautogui` 支持的按键，例如：
- `PageUp`, `PageDown`
- `Home`, `End`
- `Enter`, `Space`, `Tab`
- `Up`, `Down`, `Left`, `Right`
- `F1` - `F12`
- 字母和数字键等

## 错误处理

服务端错误响应格式：
```json
{
  "msg_id": "unique_message_id",
  "result": "error",
  "content": "错误描述"
}
```

## 项目结构

```
├── server.py          # 主程序 - WebSocket 服务器
├── generate_cert.py   # SSL证书生成工具
├── config.json        # 配置文件
├── requirements.txt   # Python依赖
└── README.md          # 项目说明
```

## 安全说明

- 服务默认监听所有网络接口 (0.0.0.0)
- 包含安全保护机制，防止意外操作
- 建议在生产环境中配置防火墙规则
- 敏感文件（logs、证书文件）已通过.gitignore排除


## 编译成exe文件
pyinstaller .\server.spec --workpath $env:TEMP --distpath "..\dist" --clean

copy server.crt ..\dist\server\server.crt
copy server.key ..\dist\server\server.key
copy config.json ..\dist\server\config.json
copy config_template.json ..\dist\server\config_template.json
