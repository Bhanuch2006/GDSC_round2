import os
import discord
from discord.ext import commands
import google.generativeai as genai
import asyncio
from datetime import datetime, timedelta
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

DISCORD_TOKEN = "MTM0NjM0NTc2MDAyMjg1OTc3Ng.GLObVf.7BxXqCjCYqRPAj3xgHWk5pEyuC6dh3Rvd9NlUQ"
GEMINI_API_KEY = "AIzaSyCPMH9q_aXf0iVGZXcQWARjB-6VD9mqWzs"
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=":", intents=intents)

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command(name="chat")
async def chat(ctx, *, message: str):
    try:
        response = model.generate_content(message)
        await ctx.send(response.text)
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
@bot.command(name="remind")
async def remind(ctx, time: str, *, task: str):
    try:
        # Parse time (e.g., 10m, 1h, 2d)
        if time.endswith('m'):
            delay = int(time[:-1]) * 60
        elif time.endswith('h'):
            delay = int(time[:-1]) * 3600
        elif time.endswith('d'):
            delay = int(time[:-1]) * 86400
        else:
            await ctx.send("Invalid time format. Use '10m', '1h', or '2d'.")
            return

        await ctx.send(f"Reminder set for {time}: {task}")
        await asyncio.sleep(delay)
        await ctx.send(f"⏰ Reminder for {ctx.author.mention}: {task}")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
@bot.command(name="poll")
async def poll(ctx, question: str, *options: str):
    if len(options) > 10:
        await ctx.send("You can only provide up to 10 options.")
        return
    poll_message = f"**Poll: {question}**\n\n"
    for i, option in enumerate(options):
        poll_message += f"{i+1}. {option}\n"
    message = await ctx.send(poll_message)
    for i in range(len(options)):
        await message.add_reaction(f"{i+1}\u20e3")

@bot.command(name="play")
async def play(ctx, url: str):
    if not ctx.author.voice:
        await ctx.send("You are not in a voice channel.")
        return

    channel = ctx.author.voice.channel
    voice_client = await channel.connect()
    ydl_opts = {'format': 'bestaudio'}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        voice_client.play(FFmpegPCMAudio(url2))

@bot.command(name="leave")
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
bot.run(DISCORD_TOKEN)