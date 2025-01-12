# Meshboi

[English](README.md) | 简体中文

一个用于与 [Meshtastic](https://meshtastic.org/) 设备交互的机器人。Meshboi 提供了一个机器人平台，可以通过串口或 WiFi 连接与 Meshtastic 节点通信。

## 功能特性

- 支持串口和 WiFi 连接
- 内置命令：
  - `#test` - 测试机器人连接
  - `#help` - 显示可用命令
  - `#ping` - 测试机器人延迟（包含信号信息）
- 支持 Docker 部署

## 安装

### 环境要求

- Python 3.13
- Poetry（Python 包管理器）
- Meshtastic 设备

### 使用 Poetry 安装

```bash
# 克隆仓库
git clone https://github.com/LeslieLeung/meshboi
cd meshboi

# 安装依赖
poetry install
```

### 使用 Docker

```bash
# 使用串口连接运行（将 /dev/ttyUSB0 替换为你的设备路径）
docker run --device=/dev/ttyUSB0 leslieleung/meshboi --connection-type serial --serial-port /dev/ttyUSB0

# 使用 WiFi 连接运行
docker run leslieleung/meshboi --connection-type wifi --hostname your-device-ip
```

## 使用方法

### 命令行选项

```bash
python main.py [--connection-type {serial,wifi}] [--hostname HOSTNAME] [--serial-port SERIAL_PORT]
```

- `--connection-type`：选择连接方式，可选 "serial"（串口）或 "wifi"（默认：serial）
- `--hostname`：WiFi 连接必需，指定 Meshtastic 设备的 IP 地址
- `--serial-port`：串口连接可选，指定设备路径（如不指定则自动发现）

### 可用命令

- `#test`、`#測試`、`#测试` - 测试机器人连接
- `#help`、`#幫助`、`#帮助` - 显示可用命令
- `#ping` - 测试机器人延迟（返回信号信息）

### 环境变量

- `DEBUG`：设置为 "true" 启用调试级别日志（默认：false）

## 开发

本项目使用 Poetry 进行依赖管理。要设置开发环境：

```bash
# 安装开发依赖
poetry install

# 运行机器人
poetry run python main.py
```

## 致谢

- [meshtastic/python](https://github.com/meshtastic/python)
- [hayschan/outdoorMeshBot](https://github.com/hayschan/outdoorMeshBot)
- [meshcn.net](https://meshcn.net/)
