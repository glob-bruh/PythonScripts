
import os 
import subprocess
import subprocess32
import discord
from datetime import datetime
from discord.ext import commands

##################################################################################
# INFO:                                                                          #
##################################################################################
botownerid =                                                                     # This is your Discord ID. 
allowdebug = False                                                               # Enable or disable !!!debug
TOKEN = ""                                                                       # Your bot token. 
##################################################################################


adminid = list(map(int, open("adminid.txt").read().splitlines()))
print(f"""\n\n---------------------
ADMIN ID's COLLECTED:
{adminid}
---------------------""")

blacklist = open("blacklist.txt").read().splitlines()
print(f"""
----------------------------
BLACKLISTED TERMS COLLECTED:
{blacklist}
---------------------------""")

client = discord.Client()

bot = commands.Bot(command_prefix='!!!', help_command=None)

@bot.event
async def on_ready():
    print(f"""\n\n_______WERE RUNNING_______
> Started at {onlineat}
> Username is {bot.user}
> ID is {bot.user.id}
> Discord.py version is {discord.__version__}
> My prefix is !!!
> Bot owner Discord ID is {botownerid}
> There are {len(adminid)} admin(s). 
> There are {len(blacklist)} blacklisted term(s).
--------------------------""")



@bot.command(name="help")
async def help(ctx):
    await ctx.send(f"""```yaml
COMMAND LIST:
=============
help      = Shows this message.
rules     = Shows bot guidelines. 
test      = Makes the bot send a response
            message.
os        = Run commands on computer.
startup   = Makes the bot output the date
            and time it was started and 
            online.
credits   = Shows credits message. 
restart   = [Bot admin only] Restarts the
            computer bot is running on
            using 'sudo reboot'.
shutdown  = [Bot admin only] Shutdown the
            bot.
addadmin  = [Bot admin only] Escaltes a
            user to a bot admin from there
            ID. 
rmadmin   = [Bot admin only] Removes a 
            bot admin from there ID. 
addterm   = [Bot admin only] Adds a term
            to the blacklist. 
rmterm    = [Bot admin only] Removes a
            term from the blacklist. 
debug     = When enabled, displays useful
            output used for development.
=============
```""")



@bot.command(name="rules")
async def help(ctx):
    await ctx.send(f"""```yaml
RULES:
If you are seeing this, the admin has not yet made any rules. 
```""") # ADMIN, rules you want people to follow should be written here. 



@bot.command(name="test")
async def test(ctx):
    print(f"_____________\n{ctx.author} sent !!!test, sending a response.\n-------------")
    await ctx.send(f"{ctx.author.name}, the bot is working.\n{'Latency: {0}'.format(round(bot.latency, 3))} seconds.")



@bot.command(name="os")
async def os(ctx, *, command):
    for testadmin in adminid:
        if testadmin == int(ctx.author.id):
            break
    else:
        for testword in blacklist:
            if testword in command.lower():
                print(f"\n\n______BLACKLISTED COMMAND RECIEVED_____\nUSER CALLING COMMAND: {ctx.author}\nRECIEVED AT: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\nINPUT: {str(command)}\n\nOFFENDING TERM:\n{testword}\n---------------------")
                await ctx.send(f":x: The phrase `{testword}` is blacklisted. Command has not been ran.")
                return

    global output

    try:
        output = subprocess.check_output(command, shell=True, timeout=3, stderr=subprocess.PIPE).decode('UTF-8')
    except subprocess.CalledProcessError as errorcalled:
        output = f":x: An error was thrown!\n{errorcalled.stderr.decode('UTF-8')}"
        print("An error was thrown from that command!")
    except subprocess.TimeoutExpired:
        output.kill()
        await ctx.send(f":x: The command {command} took longer than 3 seconds to run. Process has been killed.")
    finally:
        print(f"\n\n_____COMMAND RECIEVED_____\nUSER CALLING COMMAND: {ctx.author}\nRECIEVED AT: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\nINPUT: {str(command)}\n\nOUTPUT:\n{output}------------------")
        if len(output) >= 2000:
            await ctx.send(f":x: Sorry, output was over 2000 characters. ")
        elif len(output) <= 0:
            await ctx.send(":thinking: No output was returned. Thats all we know...")
        else:
            await ctx.send(output)



@bot.command(name="shutdown")
async def shutdown(ctx):
    print(f"\n\n_________________\n{ctx.author} has attempted to shutdown the bot.")
    for testadmin in adminid:
        if testadmin == int(ctx.author.id):
            print(f"> {ctx.author} is bot admin. Bot will now shutdown...\n-----------------\n\n")
            await ctx.send(":white_check_mark: Bot will now shutdown...")
            await bot.close()
            return
    else:
        print(f"> {ctx.author} is NOT a bot admin. Not shutting down!\n-----------------")
        await ctx.send(":x: You are not a bot admin. The bot will not shutdown.")



@bot.command(name="restart")
async def restart(ctx):
    print(f"\n\n_________________\n{ctx.author} has attempted to restart the bot.")
    for testadmin in adminid:
        if testadmin == int(ctx.author.id):
            await ctx.send(":white_check_mark: Bot will now restart.")
            command = str("sudo reboot")
            subprocess.check_output(command, shell=True).decode('UTF-8')
            print(f"Failed to restart.")
            await ctx.send(":x: System failed to restart. See server terminal for details.")
            return
    else:
        print(f"> {ctx.author} is NOT a bot admin. Not restarting!\n-----------------")
        await ctx.send(":x: You are not a bot admin. The bot will not restart.")



@bot.command(name="addadmin")
async def addadmin(ctx, userid):
    print(f"\n\n---------------------\n{ctx.author} has tried to make ID {userid} a bot admin.")
    global adminid
    for testadmin in adminid:
        if testadmin == int(ctx.author.id):
            print(f">{ctx.author} is a bot admin. Escalating user.")
            with open('adminid.txt','a') as adminstowrite:
                adminstowrite.write("\n" + userid)
                adminid.append(int(userid))
                print(f"New admin list:\n{adminid}\n---------------------")
                await ctx.send(f":white_check_mark: {ctx.author.name} has made <@!{userid}> a bot administrator.")
                return
    else:
        print(f"> {ctx.author} is not a bot admin. Request to escalate user denied.\n---------------------")
        await ctx.send(":x: You need to already be an bot admin to use this command.")



@bot.command(name="rmadmin")
async def rmadmin(ctx, userid):
    print(f"\n\n---------------------\n{ctx.author} has tried to remove ID {userid} as bot admin.")
    global adminid
    for testadmin in adminid:
        if testadmin == int(ctx.author.id):
            if int(userid) == int(botownerid):
                print("This person is hosting the bot. De-escalating has been canceled.")
                await ctx.send(":x: You cant remove the bot owner as a admin.")
            else:
                print(f">{ctx.author} is a bot admin! De-escalating user.")
                with open("adminid.txt", "r") as updatefile:
                    textfilelines = updatefile.readlines()
                with open("adminid.txt", "w") as updatefile:
                    for line in textfilelines:
                        if line.strip("\n") != userid:
                            updatefile.write(line.strip("\n"))
                adminid.remove(int(userid))
                await ctx.send(f":white_check_mark: {ctx.author.name} has removed <@!{userid}> as a bot administrator.")
            print(f"New admin list:\n{adminid}\n---------------------")
            return
    else:
        print(f"> {ctx.author} is not a bot admin. Request to de-escalate user denied.\n---------------------")
        await ctx.send(":x: You need to already be an bot admin to use this command.")


@bot.command(name="addterm")
async def addterm(ctx, blockedterm):
    print(f"\n\n---------------------\n{ctx.author} has tried to blacklist the term {blockedterm}.")
    global adminid
    for testadmin in adminid:
        if testadmin == int(ctx.author.id):
            print(f">{ctx.author} is a bot admin. {blockedterm} has been added to the blacklist.")
            with open('blacklist.txt','a') as termtowrite:
                termtowrite.write("\n" + blockedterm)
                blacklist.append(blockedterm)
                print(f"New blacklist list:\n{blacklist}\n---------------------")
                await ctx.send(f":white_check_mark: {ctx.author.name} has blacklisted the term {blockedterm}.")
                return
    else:
        print(f"> {ctx.author.name} is not a bot admin. Term has not been blacklisted.\n---------------------")
        await ctx.send(":x: You need to already be an bot admin to use this command.")    



@bot.command(name="rmterm")
async def rmterm(ctx, blockedterm):
    print(f"\n\n---------------------\n{ctx.author} has tried to remove the term {blockedterm}\nfrom the blacklist!")
    global adminid
    for testadmin in adminid:
        if testadmin == int(ctx.author.id):
            print(f">{ctx.author} is a bot admin. {blockedterm} will be removed from the blacklist.")
            with open("blacklist.txt", "r") as updatefile:
                textfilelines = updatefile.readlines()
            with open("blacklist.txt", "w") as updatefile:
                for line in textfilelines:
                    if line.strip() != blockedterm:
                        updatefile.write(line)
            blacklist.remove(blockedterm)
            await ctx.send(f":white_check_mark: {ctx.author.name} has removed the term {blockedterm} from the blacklist.")
        print(f"New blacklist list:\n{blacklist}\n---------------------")
        return
    else:
        print(f"> {ctx.author.name} is not a bot admin. Term has not been blacklisted.\n---------------------")
        await ctx.send(":x: You need to be a bot admin to use this command.")    
        
        

@bot.command(name="debug")
async def debug(ctx):
    print(f"\n----------------\n{ctx.author} has sent the d3BuG command.")
    if allowdebug == True:
        await ctx.send(f"""```yaml
[] DEBUG []
===========
VARS:
adminid = {adminid} (count: {len(adminid)})
blacklist = {blacklist} (count: {len(blacklist)})
botownerid = {botownerid}
bot = {bot}
onlineat = {onlineat}

FILES:
adminid = {list(map(int, open("adminid.txt").read().splitlines()))}
blacklist = {open("blacklist.txt").read().splitlines()}

DISCORD.PY:
bot.user = {bot.user}
ctx = {ctx}
ctx.author = {ctx.author} -> {ctx.author.id}
client = {client}
version = {str(discord.__version__)}```""")
        print("----------------")
    else:
        print("Debug command has been disabled, so deny response was sent.\n----------------")
        await ctx.send(":x: Debug command has been disabled by bot owner.")

@bot.command(name="startup")
async def startup(ctx):
    print(f"\n\n_________________\n{ctx.author} has requested online date and time.\n-----------------")
    await ctx.send(f":clock1: Bot went online at `{onlineat}`.")

@bot.command(name="credits")
async def credits(ctx):
    print(f"\n\n-----------------\n{ctx.author} requested the credits message.\n-----------------")
    await ctx.send(f"`Built by Glob_Bruh in 2020.`")

onlineat = str(datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
bot.run(TOKEN)
