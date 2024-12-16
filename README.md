# Botenix

Botenix – an asynchronous Python library for seamless integration with Mattermost. Simplifies automation, message processing, and API interactions. Designed for projects of any complexity.

## Features

- Event handling for messages, buttons, and interactive dialogs.
- Fully asynchronous for high performance.
- Simple DSL for routing and event handling.

## Installation

```bash
uv sync --all-extras
```

## Quick Start

```python
from botenix import Bot

bot = Bot(token="your-mattermost-token")

@bot.message()
async def handle_message(message):
    await message.reply("Hello!")

bot.run()
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
