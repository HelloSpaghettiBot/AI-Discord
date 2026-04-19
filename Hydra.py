import discord
from discord.ext import commands, tasks
import random
import os
import asyncio
import logging

# ==========================================
# CONFIGURATION - API KEYS & IDs REMOVED
# ==========================================
# Ensure you use a .env file locally and add it to your .gitignore
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "YOUR_DISCORD_BOT_TOKEN_HERE")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "YOUR_OPENROUTER_API_KEY_HERE")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "YOUR_GROQ_API_KEY_HERE")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")

# ID Configuration (Leave as 0/empty for public GitHub repo)
GUILD_ID = 0  
TARGET_CHANNEL_ID = 0  
TARGET_USERS = []  # IDs of users designated for targeted banter

# ==========================================
# BOT SETUP & LOGGING
# ==========================================
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("DarknoudHydra")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ==========================================
# DYNAMIC PROVIDER ROTATION & MEMORY
# ==========================================
class AIPool:
    def __init__(self):
        self.providers = ["Gemini", "Groq", "OpenRouter"]
        self.current_index = 0
        # Base context memory loaded into the system prompt
        self.context_memory = "Context: Endless Online history, server emulation, and asset archiving."

    def get_next_provider(self):
        provider = self.providers[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.providers)
        return provider

    async def generate_response(self, prompt, persona):
        provider = self.get_next_provider()
        logger.info(f"Routing request to provider: {provider}")
        
        # TODO: Implement your specific REST calls or SDK logic here 
        # using the selected provider's API key.
        # System Prompt construction = self.context_memory + persona
        
        return f"[{provider}] Generated response utilizing the '{persona}' persona."

ai_pool = AIPool()

# ==========================================
# FALLBACK GIF LIBRARY
# ==========================================
FALLBACK_GIFS = [
    "https://media.giphy.com/media/placeholder1/giphy.gif",
    "https://media.giphy.com/media/placeholder2/giphy.gif"
    # Populate with your custom meme/GIF library URLs
]

# ==========================================
# CORE EVENTS
# ==========================================
@bot.event
async def on_ready():
    logger.info(f"Logged in successfully as {bot.user}")
    scheduled_alerts.start()
    logger.info("Background tasks and alert loops started.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Stealth mentions: Bot responds if pinged or named without a command prefix
    if bot.user in message.mentions or "darknoud" in message.content.lower():
        await handle_mention(message)
        return

    await bot.process_commands(message)

# ==========================================
# PERSONA LOGIC & MESSAGE HANDLING
# ==========================================
async def handle_mention(message):
    # Dynamic Persona Switcher
    if message.author.id in TARGET_USERS:
        # Strictly playful gaming banter mode
        persona = "playful gaming banter, make fun, sarcastic but compliant" 
    else:
        persona = "friendly, helpful, and polite"

    try:
        async with message.channel.typing():
            response = await ai_pool.generate_response(message.content, persona)
            await message.channel.send(response)
    except Exception as e:
        logger.error(f"Provider failover exhausted or API error: {e}")
        # Fallback mechanism if LLM generation fails
        fallback = random.choice(FALLBACK_GIFS)
        await message.channel.send(f"Neural net overloaded. Have a GIF instead: {fallback}")

# ==========================================
# SCHEDULED AUTOMATION
# ==========================================
@tasks.loop(hours=6) # Adjust the loop interval as needed
async def scheduled_alerts():
    channel = bot.get_channel(TARGET_CHANNEL_ID)
    if not channel:
        return

    alerts = [
        "vuuuuuulllttt", 
        "Dead game check!",
        "Routine server emulation status ping."
    ]
    alert = random.choice(alerts)
    await channel.send(alert)

@scheduled_alerts.before_loop
async def before_alerts():
    await bot.wait_until_ready()

# ==========================================
# ENTRY POINT
# ==========================================
if __name__ == "__main__":
    if DISCORD_BOT_TOKEN != "YOUR_DISCORD_BOT_TOKEN_HERE":
        bot.run(DISCORD_BOT_TOKEN)
    else:
        logger.warning("Bot token not found. Please set DISCORD_BOT_TOKEN in your environment variables.")
