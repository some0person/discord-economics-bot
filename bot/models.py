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
        dbServers = self.cur.execute("SELECT server_id FROM settings")
        if dbServers:
            dbServers = dbServers.fetchall()
            return filter(lambda x: x not in dbServers, serverlist)
        return serverlist
    
    def regServers(self, serverlist):
        for server_id in self.checkServers(serverlist):
            self.cur.execute("""INSERT INTO settings (server_id, reaction, l_channels, s_channel, r_cost, award)
                             VALUES (%s, %s, %s, %s, %s, %s)""", (server_id, ":star:", "", 0, 10, 5))
            self.connection.commit()
        return
