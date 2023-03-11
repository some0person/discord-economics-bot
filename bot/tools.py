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


def extractMemberId(guild: discord.Guild, url: str) -> int:
    memberid = url.split('/')[-1]
    if memberid.isdigit() and guild.get_member(int(memberid)):
        return int(memberid)
    return 0