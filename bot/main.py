import discord
from emoji import demojize
from os import environ as env
from tools import channelCh, memberCh, numCh, reactionCh, strCh
from models import Settings, Data


client = discord.Bot(ccommand_prefix=env["PREFIX"], description="Thank you for using this bot!", intents=discord.Intents.all())

# Commands groups
settingsGroup = discord.SlashCommandGroup("settings", "Bot setup related commands")
infoGroup = discord.SlashCommandGroup("info", "Info related commands")
editGroup = discord.SlashCommandGroup("edit", "Management related commands")

# Translation
channelEMsg = "This channel is incorrect :crying_cat_face: _Please, use channel link_ __(#channel-name)__"
memberEMsg = "This member is incorrect :crying_cat_face: _Please, use user ping_ __(@user-name)__"
scoreValueEMsg = 'This value is incorrect :crying_cat_face: __Please, use only digits, "+" and "-"__'

channelListenMsg = "{channel} is under monitoring now! :smirk_cat:"
channelNotListenMsg = "{channel} is no longer under monitoring! :cloud_tornado:"
channelStarredMsg = "{channel} is starred now! :smirk_cat:"
channelNotStarredMsg = "{channel} isn't starred now! :cloud_tornado:"
reactionRewardSetMsg = "Reaction reward is set to {cost} :coin:"
reactionRewardSetEMsg = "Please, specify new reward size after command :crying_cat_face: Now it's {cost}"
awardSetMsg = "Star channel award is set to {award} :sparkles:"
awardSetEMsg = "Please, specify new star channel award size after command :crying_cat_face: Now it's {award}"
reactionSetMsg = "Reaction successfully set to {reaction}!"
reactionSetEMsg = "Please, specify new readable reaction after command :crying_cat_face: Now it's {reaction}"

scoreEditMsg = "Successfull change {member}'s score on {value} value"

settingsTitle = "Settings"
settingsColor = "#986a44"
settingsImage = "https://i.redd.it/mgixxs06w7w51.gif"
channelListenTitle = "Channels to audit ⮧"
channelStarredTitle = "Star channel ⮧"
reactionTitle = "Readable reaction ⮧"
reactionRewardTitle = "Reaction reward ⮧"
awardTitle = "Star channel award ⮧"


# !!! Events !!!

@client.event
async def on_ready() -> None:
    print("Bot started successfully...")
    if Settings().checkServers([guild.id for guild in client.guilds]):
        Settings().regServers([guild.id for guild in client.guilds])
    

@client.event
async def on_guild_join(guild: discord.Guild) -> None:
    if Settings().checkServers([guild.id]):
        Settings().regServers([guild.id])


@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent) -> None:
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    if str(payload.channel_id) not in Settings().getLChannels(payload.guild_id):
        return
    if payload.user_id == message.author.id or demojize(payload.emoji.name) != Settings().getReaction(payload.guild_id):
        return
    Data().editScore(payload.guild_id, message.author.id, Settings().getRCost(payload.guild_id))


# !!! Settings commands !!!

@settingsGroup.command(description="Adds channel into monitoring list")
async def addlchan(interaction: discord.Interaction, channel: str) -> None:
    channel = channel[2:-1]
    if not channelCh(interaction.guild, channel):
        await interaction.response.send_message(channelEMsg)
        return
    Settings().addLChannel(interaction.guild.id, channel)
    await interaction.response.send_message(channelListenMsg.format(channel=f"<#{channel}>"))


@settingsGroup.command(description="Removes channel from monitoring list")
async def dellchan(interaction: discord.Interaction, channel: str) -> None:
    channel = channel[2:-1]
    if not channelCh(interaction.guild, channel):
        await interaction.response.send_message(channelEMsg)
        return
    Settings().delLChannel(interaction.guild.id, channel)
    await interaction.response.send_message(channelNotListenMsg.format(channel=f"<#{channel}>"))


@settingsGroup.command(description='Sets "star-channel"')
async def setschan(interaction: discord.Interaction, channel: str) -> None:
    channel = channel[2:-1]
    if not channelCh(interaction.guild, channel):
        await interaction.response.send_message(channelEMsg)
        return
    Settings().setSChannel(interaction.guild.id, channel)
    await interaction.response.send_message(channelStarredMsg.format(channel=f"<#{channel}>"))


@settingsGroup.command(description='Removes "star-channel"')
async def delschan(interaction: discord.Interaction) -> None:
    channel = Settings().getSChannel(interaction.guild.id)
    Settings().delSChannel(interaction.guild.id)
    await interaction.response.send_message(channelNotStarredMsg.format(channel=f"<#{channel}>"))


@settingsGroup.command(description="Sets reaction cost in listen channels")
async def setrcost(interaction: discord.Interaction, cost: str) -> None:
    if not numCh(cost):
        await interaction.response.send_message(reactionRewardSetEMsg.format(cost=Settings().getRCost(interaction.guild.id)))
        return
    Settings().setRCost(interaction.guild.id, cost)
    await interaction.response.send_message(reactionRewardSetMsg.format(cost=cost))


@settingsGroup.command(description='Sets "star-channel" award')
async def setaward(interaction: discord.Interaction, award: str) -> None:
    if not numCh(award):
        await interaction.response.send_message(awardSetEMsg.format(award=Settings().getAward(interaction.guild.id)))
        return
    Settings().setAward(interaction.guild.id, award)
    await interaction.response.send_message(awardSetMsg.format(award=award))


@settingsGroup.command(description='Sets listen reaction. Unsupported symbols: "|`;\'"')
async def setreaction(interaction: discord.Interaction, reaction: str) -> None:
    if not reactionCh(reaction):
        await interaction.response.send_message(reactionSetEMsg.format(reaction=Settings().getReaction(interaction.guild.id)))
        return
    Settings().setReaction(interaction.guild.id, reaction)
    await interaction.response.send_message(reactionSetMsg.format(reaction=reaction))


# !!! Info commands !!!

@infoGroup.command(description="Shows all bot's settings")
async def settings(interaction: discord.Interaction) -> None:
    embed=discord.Embed(color=int(settingsColor[1:], 16))
    embed.set_thumbnail(url=settingsImage)
    embed.add_field(name=channelListenTitle, value=Settings().getLChannels(interaction.guild.id))
    embed.add_field(name=channelStarredTitle, value=Settings().getSChannel(interaction.guild.id))
    embed.add_field(name=reactionTitle, value=Settings().getReaction(interaction.guild.id))
    embed.add_field(name=reactionRewardTitle, value=Settings().getRCost(interaction.guild.id))
    embed.add_field(name=awardTitle, value=Settings().getAward(interaction.guild.id))
    
    await interaction.response.send_message(embed=embed)


# !!! Edit commands !!!

@editGroup.command(description="Edits server member's score")
async def score(interaction: discord.Interaction, member: str, value: str) -> None:
    member = member[2:-1]
    if not memberCh(interaction.guild, member):
        await interaction.response.send_message(memberEMsg)
        return
    if not strCh(value, "1234567890-+"):
        await interaction.response.send_message(scoreValueEMsg)
        return
    Data().editScore(interaction.guild.id, member, value)
    await interaction.response.send_message(scoreEditMsg.format(member=f"<@{member}>", value=value))


# !!! Bot launch !!!

client.add_application_command(settingsGroup)
client.add_application_command(infoGroup)
client.add_application_command(editGroup)
client.run(env["TOKEN"])
