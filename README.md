<p align="center">
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"></a>
    &nbsp;
    <a href="https://www.postgresql.org/"><img src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white"></a>
    &nbsp;
    <a href="https://www.docker.com/"><img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white"></a>
    &nbsp;
    <a href="https://discord.com/"><img src="https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white"></a>
    &nbsp;
    <img alt="GitHub" src="https://img.shields.io/github/license/some0person/discord-economics-bot?style=for-the-badge">
</p>

<b><p align="center" style="color:#c1a4b0">
    |
    <a href="#About">About</a>
    |
    <a href="#It's-functionality">Functionality</a>
    |
    <a href="#How-to-configure-the-bot">Configuration</a>
    |
    <a href="#How-to-use">How to use</a>
    |
    <a href="#Launching">How to start</a>
    |
</p></b>

<p align="center">
<b>~ A bit of economy to the server ~</b>
<p>



# About
DSEconomics is my first bot built with Discord API using PyCord Python library.

<p align="center">
<img src="https://user-images.githubusercontent.com/109872677/226076223-c17b88f7-7ae4-4c30-bec5-d0d64fbca5ae.png">
</p>

## It's functionality
- Reward for defined reactions received;

- Reward for placing embed of message in specific text channel;

- Mini-shop with defined items for bot currency.

*P.S: reward - special bot's currency*

<br>

## How to configure the bot

1. Add bot into your Discord server

2. Restrict commands for members to your discretion -> *recommended: ALLOW only /info and /buy commands*

3. Change bot settings using /settings commands

<br>

## How to use

- /info pricelist - shows current price list of the store and member's balance
- /info settings - shows all defined settings
- /buy - buy item from server's store
- /edit - change member's score -> **RESTRICT this command from users!**

<br>

# Launching

1. Insert bot TOKEN and aplication ID into **.env** file -> *optional: Postgres password*

2. Run `docker compose up -d`

3. Done!


