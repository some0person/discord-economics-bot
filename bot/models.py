import psycopg2
from os import environ as env


class Settings:
    def __init__(self):
        self.connection = psycopg2.connect(host=env["HOSTNAME"],
                                           user=env["POSTGRES_USER"],
                                           password=env["POSTGRES_PASSWORD"],
                                           dbname=env["POSTGRES_DB"])
        
        self.cur = self.connection.cursor()

    def checkServers(self, serverlist):
        self.cur.execute("SELECT server_id FROM settings")
        dbServers = self.cur.fetchall()
        if dbServers:
            return filter(lambda x: (x, ) not in dbServers, serverlist)
        return serverlist
    
    def regServers(self, serverlist):
        for serverid in self.checkServers(serverlist):
            self.cur.execute("""INSERT INTO settings (server_id, reaction, l_channels, s_channel, r_cost, award)
                             VALUES (%s, %s, %s, %s, %s, %s)""", (serverid, ":star:", "", 0, 10, 5))
            self.connection.commit()

    def addLChannel(self, serverid, channelid):
        self.cur.execute(f"SELECT l_channels FROM settings WHERE server_id='{serverid}'")
        lchannels = ';'.join(filter(lambda x: x, set(self.cur.fetchone()[0].split(';') + [str(channelid)])))
        self.cur.execute(f"UPDATE settings SET l_channels='{lchannels}' WHERE server_id='{serverid}'")
        self.connection.commit()

    def delLChannel(self, serverid, channelid):
        self.cur.execute(f"SELECT l_channels FROM settings WHERE server_id='{serverid}'")
        lchannels = ';'.join(filter(lambda x: x != str(channelid), self.cur.fetchone()[0].split(';')))
        self.cur.execute(f"UPDATE settings SET l_channels='{lchannels}' WHERE server_id='{serverid}'")
        self.connection.commit()

    def getLChannels(self, serverid):
        self.cur.execute(f"SELECT l_channels FROM settings WHERE server_id='{serverid}'")
        channels = self.cur.fetchone()[0]
        if channels:
            return " | ".join(map(lambda x: f"<#{x}>", channels.split(';')))
        return "None"

    def setSChannel(self, serverid, channelid):
        self.cur.execute(f"UPDATE settings SET s_channel='{channelid}' WHERE server_id='{serverid}'")
        self.connection.commit()
    
    def delSChannel(self, serverid):
        self.cur.execute(f"UPDATE settings SET s_channel='0' WHERE server_id='{serverid}'")
        self.connection.commit()
    
    def getSChannel(self, serverid):
        self.cur.execute(f"SELECT s_channel FROM settings WHERE server_id='{serverid}'")
        channel = self.cur.fetchone()[0]
        if channel:
            return f"<#{channel}>"
        return "None"

    def setRCost(self, serverid, cost):
        self.cur.execute(f"UPDATE settings SET r_cost='{cost}' WHERE server_id='{serverid}'")
        self.connection.commit()
    
    def getRCost(self, serverid):
        self.cur.execute(f"SELECT r_cost FROM settings WHERE server_id='{serverid}'")
        return self.cur.fetchone()[0]

    def setAward(self, serverid, award):
        self.cur.execute(f"UPDATE settings SET award='{award}' WHERE server_id='{serverid}'")
        self.connection.commit()
    
    def getAward(self, serverid):
        self.cur.execute(f"SELECT award FROM settings WHERE server_id='{serverid}'")
        return self.cur.fetchone()[0]
    