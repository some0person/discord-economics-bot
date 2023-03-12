import discord


def channelCh(guild: discord.Guild, channelid: int) -> bool:
    if channelid.isdigit() and discord.utils.get(guild.text_channels, id=int(channelid)):
        return True
    return False


def memberCh(guild: discord.Guild, memberid: int) -> bool:
    if memberid.isdigit() and discord.utils.get(guild.members, id=int(memberid)):
        return True
    return False


def numCh(num: str) -> bool:
    if num.isdigit():
        return True
    return False


def symbolsCh(string: str) -> bool:
    return not any(map(lambda x: x in "|`';", string))


def strCh(string: str, alphabet: str) -> bool:
    return all(map(lambda x: x in alphabet, string))


async def extractMemberId(guild: discord.Guild, url: str) -> int:
    channelid, messageid = url.split('/')[-2:]
    if channelid.isdigit() and messageid.isdigit():
        channel = await guild.fetch_channel(channelid)
        if channel:
            message = await channel.fetch_message(messageid)
            if message:
                return message.author.id
    return 0