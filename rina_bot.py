import discord
from discord.ext import commands
import requests
from discord import *
from discord.ext import tasks
from itertools import cycle
from discord import app_commands
import time
import aiohttp

intents = Intents.default()
intents.message_content = True
intents.members = True

bot = Client(intents=intents)
tree = app_commands.CommandTree(bot)

# A LIRE :
# ligne 25, player_name : pour votre pseudo
# ligne 27, api_key : votre clé d'api => /api en jeu
# ligne 82 et 87,ID discord : pour être mentionné
# ligne 90, token : le token de votre bot
# ligne 76, channel : l'id channel pour recevoir les messages


player_name = 'PSEUDO JOUEUR'
url = f'https://api.rinaorc.com/player/{player_name}'
api_key = 'VOTRE API KEY'
headers = {}
headers['API-Key'] = api_key

@bot.event
async def on_ready():
    print('Connecté')
    messageAuto.start()
    await tree.sync()


@bot.event
async def on_message(message):
    if message.author.bot:
        return

# VOIR UN PROFIL
@app_commands.command(description="Voir le profil")
async def profil(interaction : Interaction,profil:str):
    player_name = profil
    headers['API-Key'] = api_key
    url = f'https://api.rinaorc.com/player/{player_name}'
    response = requests.get(url, headers=headers)
    data = response.json()
    if response.status_code == 404:
        await interaction.response.send_message(f":negative_squared_cross_mark: **Le joueur __{profil}__ n'existe pas**")
        return
    embed = discord.Embed(title=f"Profil skyblock de {player_name}",
                          description=f"{':green_circle: En ligne' if data['player']['isOnline'] == True else 'Hors ligne :red_circle:'}",
                          color=0xf0790a)
    embed.set_author(name=f"Demandé par {interaction.user}")
    embed.add_field(name="Argents :", value=f"**{data['player']['games']['skyblock']['money']}** RC", inline=True)
    embed.add_field(name="Prestiges :", value=f"**{data['player']['games']['skyblock']['prestige']}** Prestiges", inline=True)
    embed.add_field(name="Mobs tués :", value=f"**{data['player']['games']['skyblock']['mobs']}s** Mobs tués", inline=True)
    embed.add_field(name="Temps joués :", value=f"**{data['player']['games']['skyblock']['timePlayed']}s** de jeu", inline=True)
    embed.add_field(name="Temps de fly :", value=f"**{data['player']['games']['skyblock']['flyRemaining']}s** de fly", inline=True)
    embed.add_field(name="Level d'île :", value=f"**{data['player']['games']['skyblock']['islandLevel']}** Lvls",inline=True)
    embed.set_footer(text="Bot par gregauriz (discord)")
    await interaction.response.send_message(embed=embed)
tree.add_command(profil)

# VERIFICATION REQUETE AUTOMATIQUE :
from aiohttp import ClientSession
co = None
@tasks.loop(seconds=10)
async def messageAuto():
    global co,player_name,api_key
    async with ClientSession() as session:
        channel = bot.get_channel(1111111111111111111111) # A remplacer par le channel ou les messages seront reçu
        headers['API-Key'] = api_key
        resp = await session.get(f"https://api.rinaorc.com/player/{player_name}",headers=headers)
        data = await resp.json()

        if data['player']["isOnline"] == True:
            if co == None or co == False:
                await channel.send(f"**:green_circle: Vous êtes en ligne <@ID DISCORD>**")
                co = True

        elif data['player']["isOnline"] == False:
            if co == None or co == True:
                await channel.send(f"**:red_circle: Vous êtes hors ligne <@ID DISCORD>**")
                co = False

token = "TOKEN"

bot.run(token)
