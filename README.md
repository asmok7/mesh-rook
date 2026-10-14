# MeshRook - MeshCore bot

MeshRook is a Python bot for MeshCore that connects to a companion radio over BLE and answers commands sent to it over the mesh.

## Key Features

## Screenshots

## Command Interface

Command reference: [docs/commands.md](docs/commands.md)

## Requirements

- Python 3.11 or newer
- A MeshCore companion radio running companion firmware with BLE support, paired with the host
- A host with a Bluetooth LE adapter and BlueZ (tested on Debian)

Python dependencies are installed automatically by `pip`.

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/asmok7/mesh-rook.git
   cd mesh-rook
   ```

2. **Set up the environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```

3. **Configure:**
   ```bash
   cp config.example.toml config.toml
   # Edit config.toml with your companion radio and bot settings
   ```

4. **Run:**
   ```bash
   python -m meshrook
   ```

## Status / Roadmap

| Area | Status |
|------|--------|
| Transport: BLE | Implemented |
| Transport: USB serial | Planned |
| Simulated transport (no radio, for demos and tests) | Planned |
| Environmental and home telemetry module | Planned |
| Local AI assistant module | Planned |

## Author

[@asmok7](https://github.com/asmok7)

## License

Distributed under the MIT License. See `LICENSE` for more information.
