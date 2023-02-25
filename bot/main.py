import discord
from discord.ext import commands
from os import environ as env
from models import *


bot = commands.Bot(command_prefix=env["PREFIX"], intents=discord.Intents.all())


def ch_id_conv(string, channels):
    for channel in channels:
        if string and (channel.id == int(string[0][2:-1]) or string[0].isnumeric() and channel.id == int(string[0])):
            return channel.id
    return


@bot.event
async def on_ready():
    if Settings().checkServers([guild.id for guild in bot.guilds]):
        Settings().regServers([guild.id for guild in bot.guilds])


@bot.event
async def on_guild_join(guild):
    if Settings().checkServers([guild.id]):
        Settings().regServers([guild.id])
    

@bot.command()
async def add_listen_channel(ctx, *args):
    channel = ch_id_conv(args, ctx.guild.text_channels)
    if channel:
        Settings().addLChannel(ctx.guild.id, channel)
        await ctx.send("Successfully added! :smirk_cat:")
    else:
        await ctx.send("This channel is incorrect :crying_cat_face: Please, use channel link (#channel-name)")


@bot.command()
async def del_listen_channel(ctx, *args):
    channel = ch_id_conv(args, ctx.guild.text_channels)
    if channel:
        Settings().delLChannel(ctx.guild.id, channel)
        await ctx.send("Successfully removed! :cloud_tornado:")
    else:
        await ctx.send("This channel is incorrect :crying_cat_face: Please, use channel link (#channel-name)")


@bot.command()
async def get_settings(ctx, *args):
    await ctx.send(f":eye: Channels to audit ⮧\n\t- {' | '.join(Settings().getLChannels(ctx.guild.id))}")


@bot.event
async def on_reaction_add(reaction, user):
    await bot.get_channel(reaction.message.channel.id).send("Reacted!")


bot.run(env["TOKEN"])
