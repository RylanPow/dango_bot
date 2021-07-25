import discord
import random
import time
import youtube_dl
import os
from discord.ext import commands

client = commands.Bot(command_prefix = '.')#Need to set prefix to use commands. To use command named "toaster",
                                           #with client cmd prefix ".", one would say ".toaster"

@client.command(pass_context = True)
async def join(ctx, channel = "General"): #ctx is "context" given to the function.  See discord.py documentation for further reference
    if(ctx.author.voice):
        channel = ctx.message.author.voice.channel #find VC that person who issued command is in
        await channel.connect()
    else:
        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=channel) #else use given channel name
        await voiceChannel.connect()



@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect() #leave voice channel

@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount+1) #amount+1 to delete the command you gave to delete in the first place
    msg = await ctx.send(str(amount) + " lines have been deleted. This message will delete in 3 seconds.")
    time.sleep(3)
    await msg.delete()
    #await ctx.channel.purge(limit=1) #obviously, this way wouldn't work if someone typed a message right after
                                    #that message would be deleted instead of the bot's message

@client.command()
async def play(ctx, url : str, channel="General"): #must install youtube_dl and FFMPEG to interact w/ VCs
    currentSong = os.path.isfile("song.mp3")
    try:
        if currentSong:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for current song to end or use 'stop' command")
        return
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=channel)
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': "bestaudio/best",
        'postprocessors': [{
            'key':'FFmpegExtractAudio',
            'preferredcodec': "mp3",
            'preferredquality': "192",
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")             #every video downloaded will be named to song.mp3 to overwrite
    voice.play(discord.FFmpegPCMAudio("song.mp3"))  #each file as it goes to prevent storing a ton of .mp3 files





@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("No audio currently playing.")

@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("Audio not currently paused.")





@client.command()
async def wakeup(ctx, member : discord.Member, interval = 5, repetitions = 8): #alarm/reminder system
    counter = interval #to keep track of how many seconds it has been since start
    for i in range(repetitions):
        msg = await ctx.send(member.mention + " WAKE UP!" + " It has been: " + "**" + str(counter) + "**" + " SECONDS!!!!")
        counter += interval
        time.sleep(int(interval))



@client.event #events can also trigger the bot, just like commands!  Except they aren't triggered with the "command prefix"
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.lower().startswith("cats or dogs?"): #as this line suggests, they can be triggered by these lines
        await message.channel.send(random.choice(responses1))
    if message.content.lower().startswith("!cmds"):
        await message.channel.send(commands[0:len(commands)])
    if message.content.lower().startswith(("dango!", "dango")): #originally designed for use with Dangos!
        await message.channel.send(file=discord.File("FILE PATH GOES HERE")) #this can be used to upload an image from your computer
    if message.content.lower().startswith(("dance!", "dance", ".dance")):
        await message.channel.send(file=discord.File(r"FILE PATH GOES HERE.  SUPPORTS GIFS!"))#This uploads from discords website, allowing
        #the bot to be able to upload the image regardless of whose computer the bot is hosted on.  The .File method above obviously gets
        #the image from your specific computer, so someone else hosting the bot.  Hosting the image on Discord
    if message.content.lower().startswith((".youtube trending", ".trending")): #useful for youtube links!
        myEmbed = discord.Embed(title="TITLE",
                                description="DESCRIPTION. CAN PUT LINK HERE.", color=0x0303ff)
        myEmbed.add_field(name="ANOTHER DESCRIPTION",
                          inline=False)
        myEmbed.set_image(
            url="https://media.discordapp.net/attachments/GET THIS IMAGE FROM VIEWING DISCORD IMAGE")
        myEmbed.set_author(name="NAME GOES HERE")
        await message.channel.send(embed=myEmbed)
    await client.process_commands(message) #need this line to stop command reads and do events




commands = [
    "NOTE: THESE ARE NOT CASE SENSITIVE: ",
    "cats or dogs?",
    "dango",
    "dango!",
    ".trending",
    ".dance,"
    ".play(url, voice channel[default: general])",
    ".pause, .resume, .stop",
    ".join, .leave",
    ".wakeup(user, interval[default: 5])",
    ".clear(how many to delete)",
]
responses1 = [
    ":cat: Cats!",
    ":dog: Dogs!",
    "Dangos!",
]


@client.event
async def on_ready():
    print("Bot is ready")


client.run('BOT TOKEN GOES HERE')
