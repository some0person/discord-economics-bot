import psycopg2
from os import environ as env


class Settings:
    def __init__(self) -> None:
        self.con = psycopg2.connect(host=env["HOSTNAME"],
                                    user=env["POSTGRES_USER"],
                                    password=env["POSTGRES_PASSWORD"],
                                    dbname=env["POSTGRES_DB"])
        self.cur = self.con.cursor()
    
    def checkServers(self, serverlist: list[int]):
        self.cur.execute("SELECT server_id FROM settings")
        dbServers = self.cur.fetchall()
        if dbServers:
            return filter(lambda x: (x, ) not in dbServers, serverlist)
        return serverlist
    
    def regServers(self, serverlist: list[int]) -> None:
        for serverid in self.checkServers(serverlist):
            self.cur.execute("""INSERT INTO settings (server_id, reaction, l_channels, s_channel, r_cost, award)
                             VALUES (%s, %s, %s, %s, %s, %s)""", (serverid, ":star:", "", 0, 10, 5))
            self.con.commit()

    
    def addLChannel(self, serverid: str, channelid: str) -> None:
        self.cur.execute(f"SELECT l_channels FROM settings WHERE server_id='{serverid}'")
        lchannels = ';'.join(filter(lambda x: x, set(self.cur.fetchone()[0].split(';') + [str(channelid)])))
        self.cur.execute(f"UPDATE settings SET l_channels='{lchannels}' WHERE server_id='{serverid}'")
        self.con.commit()

    def delLChannel(self, serverid: str, channelid: str) -> None:
        self.cur.execute(f"SELECT l_channels FROM settings WHERE server_id='{serverid}'")
        lchannels = ';'.join(filter(lambda x: x != str(channelid), self.cur.fetchone()[0].split(';')))
        self.cur.execute(f"UPDATE settings SET l_channels='{lchannels}' WHERE server_id='{serverid}'")
        self.con.commit()

    def setSChannel(self, serverid: str, channelid: str) -> None:
        self.cur.execute(f"UPDATE settings SET s_channel='{channelid}' WHERE server_id='{serverid}'")
        self.con.commit()
    
    def delSChannel(self, serverid: str) -> None:
        self.cur.execute(f"UPDATE settings SET s_channel='0' WHERE server_id='{serverid}'")
        self.con.commit()
    
    def setRCost(self, serverid: str, cost: str) -> None:
        self.cur.execute(f"UPDATE settings SET r_cost='{cost}' WHERE server_id='{serverid}'")
        self.con.commit()
    
    def setAward(self, serverid: str, award: str) -> None:
        self.cur.execute(f"UPDATE settings SET award='{award}' WHERE server_id='{serverid}'")
        self.con.commit()
    
    def setReaction(self, serverid: str, reaction: str) -> None:
        self.cur.execute(f"UPDATE settings SET reaction='{reaction}' WHERE server_id='{serverid}'")
        self.con.commit()


    def getLChannels(self, serverid: str) -> str:
        self.cur.execute(f"SELECT l_channels FROM settings WHERE server_id='{serverid}'")
        channels = self.cur.fetchone()[0]
        if channels:
            return " | ".join(map(lambda x: f"<#{x}>", channels.split(';')))
        return "None"

    def getSChannel(self, serverid: str) -> str:
        self.cur.execute(f"SELECT s_channel FROM settings WHERE server_id='{serverid}'")
        channel = self.cur.fetchone()[0]
        if channel:
            return f"<#{channel}>"
        return "None"

    def getReaction(self, serverid: str) -> str:
        self.cur.execute(f"SELECT reaction FROM settings WHERE server_id='{serverid}'")
        return self.cur.fetchone()[0]

    def getRCost(self, serverid: str) -> int:
        self.cur.execute(f"SELECT r_cost FROM settings WHERE server_id='{serverid}'")
        return self.cur.fetchone()[0]

    def getAward(self, serverid: str) -> int:
        self.cur.execute(f"SELECT award FROM settings WHERE server_id='{serverid}'")
        return self.cur.fetchone()[0]

    
class Data:
    def __init__(self) -> None:
        self.con = psycopg2.connect(host=env["HOSTNAME"],
                                    user=env["POSTGRES_USER"],
                                    password=env["POSTGRES_PASSWORD"],
                                    dbname=env["POSTGRES_DB"])
        self.cur = self.con.cursor()
    
    def addEntry(self, serverid: str, memberid: str):
        self.cur.execute("INSERT INTO data (server_id, member_id, score) VALUES (%s, %s, %s)", (serverid, memberid, 0))
        self.con.commit()
    
    def checkEntry(self, serverid: str, memberid: str) -> None:
        self.cur.execute(f"SELECT server_id,member_id FROM data WHERE server_id='{serverid}' AND member_id='{memberid}'")
        if not self.cur.fetchone():
            self.addEntry(serverid, memberid)
    
    def editScore(self, serverid: str, memberid: str, value: str) -> None:
        self.checkEntry(serverid, memberid)
        self.cur.execute(f"SELECT score FROM data WHERE server_id='{serverid}' AND member_id='{memberid}'")
        self.cur.execute(f"UPDATE data SET score={self.cur.fetchone()[0] + int(value)} WHERE server_id='{serverid}' AND member_id='{memberid}'")
        self.con.commit()
    
    def getScore(self, serverid:int, memberid: int) -> int:
        self.cur.execute(f"SELECT score FROM data WHERE server_id='{serverid}' AND member_id='{memberid}'")
        score = self.cur.fetchone()[0]
        if score:
            return score
        return 0


class PriceList:
    def __init__(self) -> None:
        self.con = psycopg2.connect(host=env["HOSTNAME"],
                                    user=env["POSTGRES_USER"],
                                    password=env["POSTGRES_PASSWORD"],
                                    dbname=env["POSTGRES_DB"])
        self.cur = self.con.cursor()
    
    def addPrice(self, serverid: int, title: str, price: str, description: str) -> None:
        self.cur.execute(f"SELECT MAX(item_id) FROM pricelist WHERE server_id='{serverid}'")
        itemid = self.cur.fetchone()[0]
        if itemid:
            itemid += 1
        else:
            itemid = 1
        self.cur.execute("INSERT INTO pricelist (item_id, server_id, title, price, description) \
                         VALUES (%s, %s, %s, %s, %s)", (itemid, serverid, title, price, description))
        self.con.commit()
    
    def delPrice(self, serverid: int, index: str) -> None:
        self.cur.execute(f"SELECT item_id,title,price,description FROM pricelist WHERE server_id='{serverid}'")
        pricelist = map(lambda y: y[1:], filter(lambda x: x[0] != int(index), self.cur.fetchall()))
        self.cur.execute(f"DELETE FROM pricelist WHERE server_id='{serverid}'")
        [self.addPrice(serverid, item[0], item[1], item[2]) for item in pricelist]
        self.con.commit()
    
    def getPrice(self, serverid: int) -> list[tuple]:
        self.cur.execute(f"SELECT item_id,title,price,description FROM pricelist WHERE server_id='{serverid}'")
        pricelist = self.cur.fetchall()
        if pricelist:
            return pricelist
        return [("", "None", '', "The list is empty",)]
