# WebSocket 按键服务器

一个基于 Python 的 WebSocket 服务器，用于接收客户端命令并执行系统按键操作。

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

## 启动服务器

```bash
python server.py
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

## 安全说明

- 服务默认监听所有网络接口 (0.0.0.0)
- 包含安全保护机制，防止意外操作
- 建议在生产环境中配置防火墙规则