import nextcord 
from nextcord import Interaction
from nextcord.ext import commands
import logging
import time
import random
from datetime import datetime
from threading import Timer
DICE="⚀⚁⚂⚃⚄⚅"


def UPDATE_QOTD():
    print("UPDATING QOTD")
    with open("DATA/SUBMITTED_QOTD.txt","r+") as data:
        QUOTES=data.readlines()
        if len(QUOTES)>0:Data=QUOTES[random.randint(0,len(QUOTES)-1)]
        else:Data="nincs quote"
        data.close()
    with open("DATA/SUBMITTED_QOTD.txt","w+") as data:
        data.writelines("")
        data.close()
    with open("DATA/QOTD.txt","w") as write:
        write.writelines(Data)


def SE():
    WIN=0
    dice=""
    for _ in range(2):
        w=random.randint(0,len(DICE)-1)
        dice+=(DICE[w]+" ")
        if w==1:
            if WIN==0:
                WIN=1
            else:
                WIN=12
    return dice,WIN

def QUOTE():
    with open("DATA/QOTD.txt","r+") as data:
        return data.readline()

def QOTD_SUBMIT(quote):
    with open("DATA/SUBMITTED_QOTD.txt","r+") as data:
        data.write(data.read()+quote+"\n")
        data.close()

def GetUserCoinsFromUUID(id:int):
    with open("DATA/BAL.txt","r+") as data:
        coin = 0
        success=False
        lines=data.readlines()
        for i in range(len(lines)):
            if lines[i].startswith(str(id)+";"):
                coin=int(str(lines[i]).split(';')[1])
                success=True
        if not success:
            data.write("\n"+str(id)+";0")
    return coin

logging.basicConfig(filename="LOG.log", filemode="w", format="%(name)s → %(levelname)s: %(message)s")
bot=commands.Bot(command_prefix="!")

class colors():
    primary = nextcord.Color.from_rgb(88, 101, 242)
    secondary = nextcord.Color.from_rgb(104, 81, 196)

@bot.slash_command(name="log")
async def log(interaction:Interaction):
    log = open("LOG.log","r+")
    logtxt=log.read()
    msg=await interaction.response.send_message("```autohotkey\n"+logtxt+"```")
    log.close()
    time.sleep(3)
    await msg.delete()

@bot.slash_command(name="balance",description="ennyi pénzed van")
async def coins(interaction:Interaction):
    msg=""
    coin = GetUserCoinsFromUUID(interaction.user.id)
    n = 3
    coin_split = [str(coin)[index : index + n] for index in range(0, len(str(coin)), n)]
    final=""
    for i in range(len(coin_split)): final = final+coin_split[i]+"," if i<len(coin_split)-1 else final+coin_split[i]
    embed=nextcord.Embed(color=colors.primary,title="<:KNYDcoin:1175144945078779934> "+final)
    embed.set_author(name="KNYD coin Egyenleg:")
    embed.set_thumbnail(url=interaction.user.avatar)
    msg = await interaction.response.send_message(msg,embed=embed,ephemeral=True)

@bot.slash_command(name="snake-eyes")
async def snake_eyes(interaction:Interaction):
    game=SE()
    await interaction.response.send_message("# "+game[0])
    COINS=GetUserCoinsFromUUID(interaction.user.id)
    
@bot.slash_command(name="quote-of-the-day")
async def quote_of_the_day(interaction:Interaction):
    await interaction.response.send_message("> "+QUOTE())

@bot.slash_command(name="submit-quote")
async def submit_quote(interaction:Interaction,quote:str):
    QOTD_SUBMIT(quote)
    await interaction.response.send_message("elküldve!",ephemeral=True)

@bot.slash_command(name="update-quote")
async def update_quote(interaction:Interaction):
    UPDATE_QOTD()
    await interaction.response.send_message("quote frissítve!",ephemeral=True)

x=datetime.today()
y=x.replace(day=x.day+1, hour=6, minute=0, second=0, microsecond=0)
delta_t=y-x
secs=delta_t.seconds+1
t = Timer(secs, UPDATE_QOTD)
t.start()
bot.run("key")
