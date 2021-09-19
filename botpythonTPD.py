import discord
from discord.ext import commands
import youtube_dl
import os
from discord.ext import commands
from discord.ext.commands import bot
from youtubesearchpython import VideosSearch
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from discord.ext import commands
from discordSuperUtils import MusicManager

connected = False


players = {}
queues = {}


def donne_url(url, ctx):
    x = str(url)
    if '-play' in x:
        x = x[6:]
    if '-p' in x:
        x = x[3:]
    if not "youtube" in x:
        videosSearch = VideosSearch(x, limit=1)
        url2 = videosSearch.result()['result'][0]['link']
        return url2
    if "youtube" in x:
        return x


client = commands.Bot(command_prefix="-")
MusicManager = MusicManager(client, spotify_support=False)

@MusicManager.event
async def on_play(ctx, player):
    await ctx.send(f"Now playing: {player.title}")



@client.command(name='play', aliases=['p'])
async def play(ctx,):
    global connected
    URL = donne_url(ctx.message.content, ctx)
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=str(ctx.author.voice.channel))
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if not voice is None:
        if not voice.is_connected():
            voice = await voiceChannel.connect()
    else:
        voice = await voiceChannel.connect()
    connected = True
    async with ctx.typing():
        players = await MusicManager.create_player(URL, ctx.author)
        await ctx.send(URL)

    if players:
        if await MusicManager.queue_add(players=players, ctx=ctx) and not await MusicManager.play(ctx):
            await ctx.send("Ajouter a la grosse QUEUE")




@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
        connected = False
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        await ctx.send("https://thumbs.gfycat.com/RawIllinformedGalah-size_restricted.gif")
    else:
        await ctx.send("Y'a pas de musique enculé")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("C'est pas en pause UwU")


@client.command(name='skip', aliases=['s'])
async def skip(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()
    await ctx.send("J'avoue la musique pue la merde")



client.run('token')
