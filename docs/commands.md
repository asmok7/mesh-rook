# Command reference

Scope defines who may use a command:

- **public**: anyone who can reach the bot (public channel or direct message)
- **trusted**: direct messages from allow-listed contacts only
- **admin**: direct messages from admin contacts only

## Basic

| Command | Scope | Description |
|---------|-------|-------------|
| `ping` | public | Replies to confirm the bot is alive |
| `test` | public | Replies with reception details of the received message (hops, signal) |
| `path` | public | Replies with the path the received message travelled |
| `info` | public | Short information about the bot |

## Diagnostics

| Command | Scope | Description |
|---------|-------|-------------|
| `adverts` | trusted | List of received 0-hop adverts with signal level |
| `status` | trusted | Bot status: battery, uptime, temperature |
| `trace <path>` | trusted | Runs a trace along the given path |
| `flood <text>` | trusted | Sends a flood message |
| `msg <path> <text>` | trusted | Sends a message along the given path |

## Environmental telemetry (planned module)

| Command | Scope | Description |
|---------|-------|-------------|
| `weather` | public | Outdoor sensors: temperature, humidity, pressure, air pollution |
| `weather home` | trusted | Home sensors: temperature and humidity list, outlet on/off state |

## Management

| Command | Scope | Description |
|---------|-------|-------------|
| `join <channel>` | admin | Bot starts reacting to commands on the given channel |
| `part <channel>` | admin | Bot stops listening on the given channel (alias: `left`) |
| `ai on` / `ai off` | admin | Attaches or detaches the local AI assistant (planned module) |
