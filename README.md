# Hydra

Hydra is a Discord bot built with `discord.py` that responds to mentions, rotates between multiple AI providers, switches personas based on target users, and sends scheduled automated alerts to a designated channel.

This version is set up for safe public sharing, with API keys and IDs removed and expected to be loaded from environment variables.

---

## Features

- Responds when mentioned directly
- Responds when its name is typed in chat (`hydra`)
- Rotates between multiple AI providers:
  - Gemini
  - Groq
  - OpenRouter
- Uses dynamic persona switching:
  - Friendly/helpful for normal users
  - Playful banter mode for target users
- Sends scheduled alert messages every 6 hours
- Falls back to meme/GIF responses if AI generation fails
- Uses environment variables for sensitive credentials

---

## Requirements

- Python 3.10+
- A Discord bot application and token
- Required Python package:

```bash
pip install discord.py
```

---

## Environment Variables

Create a `.env` file in your project folder and add your real keys there.

Example:

```env
DISCORD_BOT_TOKEN=your_discord_bot_token
OPENROUTER_API_KEY=your_openrouter_key
GROQ_API_KEY=your_groq_key
GEMINI_API_KEY=your_gemini_key
```

> Do **not** commit your `.env` file to GitHub.

---

## Suggested `.gitignore`

```gitignore
.env
__pycache__/
*.pyc
```

---

## Configuration

Inside the script, these values are intentionally left blank or zeroed for public sharing:

```python
GUILD_ID = 0
TARGET_CHANNEL_ID = 0
TARGET_USERS = []
```

### What they do

- `GUILD_ID`  
  Your Discord server ID

- `TARGET_CHANNEL_ID`  
  The channel where scheduled alerts will be posted

- `TARGET_USERS`  
  A list of Discord user IDs that trigger the banter persona

Example:

```python
GUILD_ID = 123456789012345678
TARGET_CHANNEL_ID = 987654321098765432
TARGET_USERS = [111111111111111111, 222222222222222222]
```

---

## How It Works

### Mention Handling
The bot listens for messages and responds when:

- it is directly mentioned
- the word `hydra` appears in the message

### Persona Switching
When a message is handled:

- users in `TARGET_USERS` get a sarcastic/playful gaming banter response
- everyone else gets a friendly/helpful response

### AI Provider Rotation
Each response cycles through:

1. Gemini
2. Groq
3. OpenRouter

This is managed by the `AIPool` class.

### Scheduled Alerts
A background task runs every 6 hours and posts a random alert message to the configured target channel.

### Fallback Response
If AI generation fails for any reason, the bot sends a fallback GIF from the local GIF list.

---

## Current Placeholder Behavior

Right now, the AI response system is stubbed out and does **not** yet make real API calls.

This part:

```python
async def generate_response(self, prompt, persona):
```

currently returns a mock response like:

```text
[Gemini] Generated response utilizing the 'friendly, helpful, and polite' persona.
```

You still need to connect your real provider API logic inside that function.

---

## Running the Bot

Start the bot with:

```bash
python your_script_name.py
```

If `DISCORD_BOT_TOKEN` is missing, the bot will not start and will log a warning instead.

---

## Project Structure

Example layout:

```bash
Hydra/
├── bot.py
├── .env
├── .gitignore
└── README.md
```

---

## Customization

### Change Bot Trigger Name
This line controls the text-name trigger:

```python
if bot.user in message.mentions or "hydra" in message.content.lower():
```

You can replace `"hydra"` with any keyword you want.

### Change Scheduled Alert Timing
This line controls how often alerts are sent:

```python
@tasks.loop(hours=6)
```

You can change it to something else, like:

```python
@tasks.loop(hours=1)
```

### Change Alert Messages
Edit the `alerts` list:

```python
alerts = [
    "vuuuuuulllttt",
    "Dead game check!",
    "Routine server emulation status ping."
]
```

### Change Fallback GIFs
Replace the placeholder GIF links in:

```python
FALLBACK_GIFS = [
    "https://media.giphy.com/media/placeholder1/giphy.gif",
    "https://media.giphy.com/media/placeholder2/giphy.gif"
]
```

with your own real GIF or meme URLs.

---

## Security Notes

- Never hardcode real API keys in your source code
- Never upload your `.env` file
- Never commit production Discord IDs or tokens in public repos
- Rotate your tokens immediately if they are ever exposed

---

## Future Improvements

- Add actual REST or SDK integration for Gemini, Groq, and OpenRouter
- Add provider failover if one service is down
- Store per-user conversation memory
- Add slash commands
- Add admin-only controls for alerts and persona targets
- Add rate limiting and cooldown handling
- Load config from `.env` or JSON instead of editing the script directly

---

## License

Use, modify, and expand as needed for your own bot project.

---

## Notes

This repo version is intentionally sanitized for safe sharing. Before running it in production, make sure you:

- set your real environment variables
- install required packages
- configure your Discord IDs
- implement the actual AI provider request logic
