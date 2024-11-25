
# Discord OSBot

## Preface:

OSBot is a python3 Discord bot that is designed to receive and run commands sent to it by Discord users. It allows users to run any command on the remote system (or ones that the bot owner/admins specifically allow).

## Warning - read before proceeding:

This script is not for use in public servers. Allowing people on Discord to remotely control a system is **dangerous**, and can lead to serious and unexpected consequences. Make sure that you run this script in a virtual machine, and that you trust every member in the server that this bot is active in. 

If you are looking for a tool to test code/run commands with, then consider a safer alternative such as [Discord Compiler](https://headlinedev.xyz/discord-compiler).

## Setup:

This bot has been built and tested **only** on Linux systems (specifically Debian). To run this bot on your own system, follow these instructions:

1) Install Python3 to your system (you can do this through the [python website](https://www.python.org/) or your systems package manager). 
2) Download the OSBot script.
3) Go to the [Discord developer portal](https://discord.com/developers/applications) and make a new application. After you give the application an name, go to the bot tab and generate a token.
4) Open the OSBot script in a editor and paste the token on the appropriate line in the Info box.
5) [Invite the bot](https://discord.com/developers/docs/topics/oauth2#bot-authorization-flow) to a server that you **completely trust** (see the above warning for more info).
6) Through Discord, [copy your user ID](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-) and paste it into the bot owner ID line in the Info box. 
7) Create a file (in the same folder as the script) called `adminid.txt`. Put your user ID in this file. 
8) Create a file (in the same folder as the script) called `blacklist.txt`. When a user runs a command that contains a phrase from this file, it will be blocked. The only exception is if that user is a bot admin. 
9) OPTIONAL: Add some rules by editing the rules command. 
10) Run the script with Python3. The bots default prefix is `!!!`. 

You can view the available commands by running `!!!help`.

## Files:
- **adminid.txt** - List of user ID's of users that are bot admins. Bot admins can bypass the blacklist and perform actions such as system restarts and bot shutdowns. 
- **blacklist.txt** - List of phrases users commands are not allowed to contain. For example, if the phrase `sudo` is in this file, and a user attempts to run `sudo whoami`, the script will not run that users command and return a error instead. Bot admins can bypass the blacklist. 
