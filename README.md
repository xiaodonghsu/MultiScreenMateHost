# MultiScreenMate Host Server

**主程序：server.py**

一个基于 Python 的 WebSocket 服务器，用于接收客户端命令并执行系统按键操作，支持多屏幕协同控制。

## 功能特性

- WebSocket 协议通信
- 支持握手验证
- 执行系统按键命令
- 可配置端口和服务名称

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置说明

编辑 `config.json` 文件：

```json
{
  "port": 8765,
  "name": "WebSocket Key Server",
  "mac_addr": "00:1B:44:11:3A:B7"
}
```

- `port`: WebSocket 服务端口
- `name`: 服务名称（握手时返回）
- `mac_addr`: MAC地址（握手时返回）

## 主程序说明

本项目的主程序是 `server.py`，负责启动 WebSocket 服务器并处理客户端连接。

## 启动服务器

运行主程序：
```bash
python server.py
```

或者使用批处理文件：
```bash
start_server.bat
```

## 客户端协议

### 1. 握手命令

客户端发送：
```json
{
  "command": "handshake",
  "id": "unique_id_123"
}
```

服务端响应：
```json
{
  "id": "unique_id_123",
  "result": "success",
  "name": "WebSocket Key Server",
  "mac": "00:1B:44:11:3A:B7"
}
```

### 2. 按键命令

客户端发送：
```json
{
  "command": {"key": "PageUp"},
  "id": "unique_id_456"
}
```

服务端响应：
```json
{
  "id": "unique_id_456",
  "result": "success"
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
  "result": "error",
  "message": "错误描述"
}
```

## 项目结构

```
├── server.py          # 主程序 - WebSocket 服务器
├── test_client.py     # 测试客户端
├── test_scan_server.py # 服务器扫描工具
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