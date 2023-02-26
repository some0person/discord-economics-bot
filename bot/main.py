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
        await ctx.send("This channel is under monitoring now! :smirk_cat:")
    else:
        await ctx.send("This channel is incorrect :crying_cat_face: Please, use channel link (#channel-name)")


@bot.command()
async def del_listen_channel(ctx, *args):
    channel = ch_id_conv(args, ctx.guild.text_channels)
    if channel:
        Settings().delLChannel(ctx.guild.id, channel)
        await ctx.send("This channel is no longer under monitoring! :cloud_tornado:")
    else:
        await ctx.send("This channel is incorrect :crying_cat_face: Please, use channel link (#channel-name)")


@bot.command()
async def set_star_channel(ctx, *args):
    channel = ch_id_conv(args, ctx.guild.text_channels)
    if channel:
        Settings().setSChannel(ctx.guild.id, channel)
        await ctx.send("This channel is starred now! :smirk_cat:")
    else:
        await ctx.send("This channel is incorrect :crying_cat_face: Please, use channel link (#channel-name)")
        

@bot.command()
async def del_star_channel(ctx, *args):
    Settings().delSChannel(ctx.guild.id)
    await ctx.send("This channel isn't starred now! :cloud_tornado:")


@bot.command()
async def set_rcost(ctx, *args):
    if args and args[0].isnumeric():
        Settings().setRCost(ctx.guild.id, args[0])
        await ctx.send(f"Reaction reward is set to {args[0]} :coin:")
    else:
        await ctx.send(f"Please, specify new reward size after command :crying_cat_face: \
Now it's {Settings().getRCost(ctx.guild.id)}")


@bot.command()
async def set_award(ctx, *args):
    if args and args[0].isnumeric():
        Settings().setAward(ctx.guild.id, args[0])
        await ctx.send(f"Star channel award is set to {args[0]} :sparkles:")
    else:
        await ctx.send(f"Please, specify new star channel award size after command :crying_cat_face: \
Now it's {Settings().getAward(ctx.guild.id)}")


@bot.command()
async def get_settings(ctx, *args):
    row = f""":eye: Channels to audit ⮧\n\t- {Settings().getLChannels(ctx.guild.id)}\n
:star: Star channel ⮧\n\t- {Settings().getSChannel(ctx.guild.id)}\n
:coin: Reaction reward ⮧\n\t- {Settings().getRCost(ctx.guild.id)}\n
:sparkles: Star channel award ⮧\n\t- {Settings().getAward(ctx.guild.id)}"""

    await ctx.send(row)


@bot.event
async def on_reaction_add(reaction, user):
    await bot.get_channel(reaction.message.channel.id).send("Reacted!")


bot.run(env["TOKEN"])
