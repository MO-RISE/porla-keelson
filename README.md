# porla-keelson
This is an extension to [`porla`](https://github.com/MO-RISE/porla).

## What

This extension provides interoperability with the keelson data format through [brefv](https://github.com/MO-RISE/keelson/tree/main/brefv).

### Built-in functionality

Binaries for working with envelopes:
* `enclose`
* `uncover`

Binaries for working with payloads:
* TODO

### 3rd-party tools

This extension bundles [`zenoh-cli`](https://github.com/MO-RISE/zenoh-cli).

## Usage

### Examples
```yaml
version: '3.8'

services:
    sink_1:
        image: ghcr.io/mo-rise/porla-keelson
        network_mode: host
        restart: always
        command: ["from_bus 3 | base64 --encode | brefv encode '{payload_b64}' '{envelope}' | zenoh put --base64 --key my/key/expression --line '{message}'"]

```
