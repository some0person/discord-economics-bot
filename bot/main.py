import discord
from discord.ext import commands
from config import settings


bot = commands.Bot(command_prefix=settings["prefix"], intents=discord.Intents.all())


def ch_id_conv(string, channels):
    for channel in channels:
        if string and (channel.id == int(string[0][2:-1]) or string[0].isnumeric() and channel.id == int(string[0])):
            return channel.id
    return


@bot.command()
async def set_listen_channel(ctx, *args):
    channel = ch_id_conv(args, ctx.guild.text_channels)
    if channel:
        f = open("channels", 'a').write(str(channel) + '\n')
    else:
        await ctx.send("This channel is incorrect :crying_cat_face: Please, use channel link (#channel-name)")


@bot.event
async def on_reaction_add(reaction, user):
    await bot.get_channel(reaction.message.channel.id).send("Reacted!")


bot.run(settings["token"])
