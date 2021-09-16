import discord
from discord.ext import commands
import youtube_dl
import os
from youtubesearchpython import VideosSearch
connected = False

client = commands.Bot(command_prefix="-")



@client.command(name='play', aliases=['p'])
async def play(ctx, url: str):
    global connected
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return


    channel = ctx.author.voice.channel
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=str(channel))
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if connected==False:
        await voiceChannel.connect()

    connected = True
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if not "youtube" in ctx.message.content:
        ctx.message.content = ctx.message.content[5:]
        videosSearch = VideosSearch(ctx.message.content, limit=1)
        x = videosSearch.result()['result'][0]['link']
        url = x
        await ctx.send(x)



    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


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
