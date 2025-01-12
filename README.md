# Meshboi

English | [简体中文](README_zh.md)

A bot for interacting with [Meshtastic](https://meshtastic.org/) devices. Meshboi provides a bot platform to communicate with Meshtastic nodes, supporting both serial and WiFi connections.

## Features

- Support for both serial and WiFi connections
- Built-in commands:
  - `#test` - Test the bot connection
  - `#help` - Show available commands
  - `#ping` - Ping the bot (includes signal information)
- Runs on Docker

## Installation

### Prerequisites

- Python 3.13
- Poetry (Python package manager)
- A Meshtastic device

### Using Poetry

```bash
# Clone the repository
git clone https://github.com/LeslieLeung/meshboi
cd meshboi

# Install dependencies
poetry install
```

### Using Docker

```bash
# Run with serial connection (replace /dev/ttyUSB0 with your device path)
docker run --device=/dev/ttyUSB0 leslieleung/meshboi --connection-type serial --serial-port /dev/ttyUSB0

# Run with WiFi connection
docker run leslieleung/meshboi --connection-type wifi --hostname your-device-ip
```

## Usage

### Command Line Options

```bash
python main.py [--connection-type {serial,wifi}] [--hostname HOSTNAME] [--serial-port SERIAL_PORT]
```

- `--connection-type`: Choose between "serial" or "wifi" connection (default: serial)
- `--hostname`: Required for WiFi connection, specify the Meshtastic device's IP address
- `--serial-port`: Optional for serial connection, specify the device path (auto-discovers if not specified)

### Available Commands

- `#test`, `#測試`, `#测试` - Test the bot connection
- `#help`, `#幫助`, `#帮助` - Show available commands
- `#ping` - Ping the bot (returns signal information)

### Environment Variables

- `DEBUG`: Set to "true" for debug-level logging (default: false)

## Development

The project uses Poetry for dependency management. To set up a development environment:

```bash
# Install development dependencies
poetry install

# Run the bot
poetry run python main.py
```

## Credits

- [meshtastic/python](https://github.com/meshtastic/python)
- [hayschan/outdoorMeshBot](https://github.com/hayschan/outdoorMeshBot)
- [meshcn.net](https://meshcn.net/)