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
import discordSuperUtils

connected = False


players = {}
queues = {}


async def donne_url(url, ctx):
    x = str(url)
    if '-play' in x:
        x = x[6:]
    if '-p' in x:
        x = x[3:]
    if 'youtu.be' in x:
        x = 'https://www.youtube.com/watch?v='+x[17:]
        return x
    if "loca" in x:
        await ctx.send("Va baiser tes morts sale pd")
        return "https://www.youtube.com/watch?v=VmyPUPcrCFw"
    if "shakira" in x:
        await ctx.send("Va baiser tes morts sale fdp")
        return "https://www.youtube.com/watch?v=VmyPUPcrCFw"
    if not "youtube" in x:
        videosSearch = VideosSearch(x, limit=1)
        url2 = videosSearch.result()['result'][0]['link']
        return url2
    if "youtube" in x:
        return x




client = commands.Bot(command_prefix="-")
MusicManager = MusicManager(client, spotify_support=False)

@MusicManager.event()
async def on_play(ctx, player):
    await ctx.send(f"ça turn up sur : {player.title}")

@MusicManager.event()
async def on_inactivity_disconnect(ctx):
    print("Quitté a cause d'inactivité")




@client.command(name='play', aliases=['p'])
async def play(ctx,):
    global connected

    URL = await donne_url(ctx.message.content, ctx)
    if URL is None:
        await ctx.send("J'ai pas trouvé le son")
        return
        
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
            await ctx.send("Ajouté a la grosse QUEUE")


@client.command(name='showqueue', aliases=["sq","queue"])
async def showQueue(ctx):
    await ctx.send("Tema la grosse queue!")
    formatted_queue = [f"Title: '{x.title}\nRequester: {x.requester.mention}" for x in (await MusicManager.get_queue(ctx)).queue]
    embeds = discordSuperUtils.generate_embeds(formatted_queue,
                                               "La queue : ",
                                               f"En ce moment: {await MusicManager.now_playing(ctx)}",
                                               25,
                                               string_format="{}")

    page_manager = discordSuperUtils.PageManager(ctx, embeds, public=True)
    await page_manager.run()

@client.command(name='purge', aliases=["pq"])
async def purgeQueue(ctx):
    await MusicManager.clear()
    await ctx.send("La queue est purgée")

@client.command(name='loop', aliases=["l"])
async def loop(ctx):
    isLooping = await MusicManager.loop(ctx)
    if isLooping:
        await ctx.send("Mode loop activé")
    else:
        await ctx.send("Mode loop desactivé")

@client.command(name='loopqueue', aliases=["lq"])
async def loopQueue(ctx):
    isLooping = await MusicManager.queueloop(ctx)
    if isLooping:
        await ctx.send("Mode loop de la queue activé")
    else:
        await ctx.send("Mode loop de la queue desactivé")


@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
        connected = False
    else:
        await ctx.send("Gros con le bot est pas connecté")


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
