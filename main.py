import discord
import requests
import datetime 
import json
from bs4 import BeautifulSoup
from discord import app_commands
from discord.ext import commands 

PREFIX = ";"

INTENTS = discord.Intents.all()

client = commands.Bot(intents=INTENTS, command_prefix=PREFIX)
client.remove_command('help')



async def on_ready(self):
    print("Bot is online!")


async def on_guild_join(self):
    await client.tree.sync()
    print("Commands have been synced for the new server")








def statsplit(x):
    split1 = str(x).split("<")[-2]
    split2 = split1.split(" ")[-1]
    split3 = split2.split(">")[-1]

    return split3

def mmrsplit(x):
    split1 = str(x).split(">")[-2]
    split2 = split1.split("<")[-2]

    return split2 

def imgsplit(x):
    split1 = str(x).split("=")[-1]
    split2 = split1.split(">")[-2]
    split3 = split2.replace('"', '')
    split4 = split3.rstrip('/')

    return split4




# help commands


@client.command()
async def sync(ctx):
    print("sync command")
    if ctx.author.id == 325837218222440460:
        await client.tree.sync()
        await ctx.send(f"Synced commands to the the servers!")
    else:
        await ctx.send('You must be the owner to use this command!')

@client.tree.command(name="help", description="Displays the list of commands that are currently available")
async def self(interaction:discord.Interaction):
    embed = discord.Embed(title="Command list", description="** **", color=3092790)

    embed.add_field(name="/games_supported", value="Displays the games that GameStats+ can be used for")
    embed.add_field(name="/help_valorant", value="Displays the current commands for valorant")
    embed.add_field(name="/help_osu", value="Displays the current commands for osu!")
    embed.add_field(name="/help_r6", value="Displays the current commands for Rainbow Six Siege")
    embed.add_field(name="/help_apex", value="Displays the current commands for apex legends")
    embed.add_field(name="/help_csgo", value="Displays the current commands for csgo")
    embed.add_field(name="/help_misc", value="Displays the misc commands for GameStats+")


    await interaction.response.send_message(embed=embed)



@client.tree.command(name="help_valorant", description="Displays the current commands for valorant")
async def self(interaction:discord.Interaction):
    embed = discord.Embed(title="Current Valorant commands", description="** **", color=discord.Color.red())

    embed.add_field(name="/valorant_stats", value="Displays the current ranked stats for the user")

    await interaction.response.send_message(embed=embed)


@client.tree.command(name="help_r6", description="Displays the current commands for Rainbow Six Siege")
async def self(interaction:discord.Interaction):
    embed = discord.Embed(title="List of commands for Rainbow Six Siege", description="** **",)

    embed.add_field(name="/r6_stats", value="Displays the lifetime stats for the user")
    embed.add_field(name="/r6_ranked_stats", value="Displays the ranked stats for the user")

    await interaction.response.send_message(embed=embed)


@client.tree.command(name="help_osu", description="Displays the current commands for osu!")
async def self(interaction:discord.Interaction):
    embed = discord.Embed(title="Current osu! commands", description="** **", color=discord.Color.pink())

    embed.add_field(name="/osu_stats", value="Displays the stats for  the user")

    await interaction.response.send_message(embed=embed)


@client.tree.command(name="help_csgo", description="Displays the current commands for csgo")
async def self(interaction:discord.Interaction):
    embed = discord.Embed(title="Current csgo commands", description="** **", color=discord.Color.orange())

    embed.add_field(name="/counter_strike_stats", value="Displays the csgo stats for the user")

    await interaction.response.send_message(embed=embed)


@client.tree.command(name="help_apex", description="Displays the current commands for apex legends")
async def self(interaction:discord.Interaction):
    embed = discord.Embed(title="Current csgo commands", description="** **", color=discord.Color.red())

    embed.add_field(name="/apex_legend_stats", value="Displays the apex legend stats for the user")

    await interaction.response.send_message(embed=embed)


@client.tree.command(name="games_supported", description="List of games that are currently supported.")
async def self(interaction:discord.Interaction):
    await interaction.response.send_message("Games currently supported: osu!, R6, Valorant, Apex Legends, and CS:GO")


# stats




# OSU!

@client.tree.command(name="osu_stats", description="Gives you stats on an osu user")
async def self(interaction: discord.Interaction, username: str):
    baseUrl = 'https://osu.ppy.sh/api/{}?k=e7842270927e45016fef5cbe4ed44c3fe2c96440'
    url = baseUrl.format("get_user") + "&u=" + username
    r = requests.get(url)
    stats = r.json()
    seconds_played = int(stats[0]['total_seconds_played'])
    hours_played = (datetime.timedelta(seconds=seconds_played))
    embed = discord.Embed(title=f"{username}'s stats", description="** **", color=discord.Color.pink())
    embed.add_field(name="PP rank", value=stats[0]['pp_rank'], inline=False)
    embed.add_field(name="Accuracy", value=stats[0]['accuracy'], inline=False)
    embed.add_field(name="Sign up Date", value=stats[0]['join_date'], inline=False)
    embed.add_field(name="Play time", value=hours_played, inline=False)


    await interaction.response.send_message(embed=embed)

# RAINBOW SIX

@client.tree.command(name="r6_stats", description="Gives the stats of someones Rainbow Six Seige Profile")
async def self(interaction: discord.Interaction, platform: str, username: str):
    r = requests.get(f"https://r6.tracker.network/profile/{platform}/{username}")
    userPage = BeautifulSoup(r.text, 'html.parser')
    kd = userPage.find('div', {'data-stat': 'PVPKDRatio'})
    kdd = statsplit(kd)
    wr = userPage.find('div', {'data-stat': 'PVPWLRatio'})
    wrr = statsplit(wr)
    kills = userPage.find('div', {'data-stat': 'PVPKills'})
    killls = statsplit(kills)
    wins = userPage.find('div', {'data-stat': 'PVPMatchesWon'})
    winss = statsplit(wins)
    timePlayed = userPage.find('div', {'data-stat': 'PVPTimePlayed'})
    timePlayedd = statsplit(timePlayed)

    embed = discord.Embed(title=f"{username}'s all time stats", description="** **", color=3092790)
    embed.add_field(name="KD", value=kdd)
    embed.add_field(name="Win Rate", value=wrr, inline=False)
    embed.add_field(name="Kills", value=killls)
    embed.add_field(name="Wins", value=winss, inline=False)
    embed.add_field(name="Time Played", value=timePlayedd)

    await interaction.response.send_message(embed=embed)

@client.tree.command(name="r6_ranked_stats", description="Gives the ranked stats of the users Rainbow Six Seige profile")
async def self(interaction: discord.Interaction, platform: str, username: str):
    r = requests.get(f"https://r6.tracker.network/profile/{platform}/{username}")
    userPage = BeautifulSoup(r.text, 'html.parser')
    mmr = userPage.find('div', {'style': 'font-family: Rajdhani; font-size: 3rem;'})
    best_mmr = mmrsplit(mmr)

    mmr_pic = userPage.find('image', {'width': '56'})
    picture = imgsplit(mmr_pic)

    rankedKD = userPage.find('div', {'data-stat': 'RankedKDRatio'})
    kd = statsplit(rankedKD)

    rankedWins = userPage.find('div', {'data-stat': 'RankedWins'})
    wins = statsplit(rankedWins)

    rankedWinRate = userPage.find('div', {'data-stat': 'RankedWLRatio'})
    win_rate = statsplit(rankedWinRate)

    embed = discord.Embed(title=f"{username}'s ranked stats", description="** **", color=3092790)
    embed.add_field(name="Current season MMR", value=best_mmr, inline=False)
    embed.add_field(name="All Time Ranked KD", value=kd, inline=False)
    embed.add_field(name="All Time Ranked Wins", value=wins, inline=False)
    embed.add_field(name="All Time Ranked Win Rate", value=win_rate, inline=False)
    embed.set_thumbnail(url=picture)

    await interaction.response.send_message(embed=embed)

# valorant 

@client.tree.command(name="valorant_stats", description="Retreive the comp stats for the user")
async def self(interaction: discord.Interaction, username:str, riot_id:str):
    if " " in username:
        username = username.replace(' ', '%20')

    r = requests.get(f"https://tracker.gg/valorant/profile/riot/{username}%23{riot_id}/overview")

    userPage = BeautifulSoup(r.text, 'html.parser')
    mmr = userPage.find('span', {'class': 'stat__value'})
    print(mmr)
    best_mmr = mmr.text
    print(best_mmr)

    test = userPage.find_all('span', {'class': 'value'})

    winRate = test[6]

    rr = requests.get(f'https://tracker.gg/valorant/profile/riot/{username}%23{riot_id}/agents')
    agentPage = BeautifulSoup(rr.text, 'html.parser')
    agentLocate = agentPage.find_all('div', {'class': 'value'})
    most_played_character = str(agentLocate[0].text)

    agentPicture = agentPage.find_all('img', {'data-v-0c313880': ''})
    print(agentPicture[4])
    picture = agentPicture[4]
    new_pic = str(picture).replace('<img data-v-0c313880="" src=', '')
    real_pic = new_pic.replace('"', '')
    legend_picture = real_pic.replace('/>', '')


    
    if most_played_character == "Skye":
        colorr = discord.Color.green()
    elif most_played_character == "Killjoy":
        colorr = discord.Color.yellow()
    elif most_played_character == "Cypher":
        colorr = discord.Color.from_rgb(255, 255, 255)
    elif most_played_character == "Sova":
        colorr = discord.Color.blue()
    elif most_played_character == "Astra":
        colorr = discord.Color.purple()
    elif most_played_character == "BrimStone":
        colorr = discord.Color.dark_orange()
    elif most_played_character == "Raze":
        colorr = discord.Color.orange()
    elif most_played_character == "Viper":
        colorr = discord.Color.green()
    elif most_played_character == "Breach":
        colorr = discord.Color.orange()
    elif most_played_character == "Omen":
        colorr = discord.Color.purple()
    elif most_played_character == "Reyna":
        colorr = discord.Color.pink()
    elif most_played_character == "Jett":
        colorr = discord.Color.blue()
    elif most_played_character == "Phoenix":
        colorr = discord.Color.orange()
    elif most_played_character == "KAY/O":
        colorr = discord.Color.purple()
    elif most_played_character == "Gekko":
        colorr = discord.Color.green()
    elif most_played_character == "Harbor":
        colorr = discord.Color.dark_blue()
    elif most_played_character == "Deadlock":
        colorr = discord.Color.from_rgb(255, 255, 255)
    elif most_played_character == "Chamber":
        colorr = discord.Color.gold()
    elif most_played_character == "Sage":
        colorr = discord.Color.green()




    embed = discord.Embed(title=f"Valorant Stats for {username.replace('%20', ' ')}#{riot_id} for the current episode", description="** **", color=colorr)
    embed.add_field(name="Current RR", value=best_mmr)
    embed.add_field(name="Comp Win Rate", value=winRate.text)
    embed.add_field(name="Comp Wins", value=test[7].text)
    embed.add_field(name="Comp Kills", value=test[10].text)
    embed.add_field(name="Most played Comp Legend", value=most_played_character)
    embed.set_thumbnail(url=legend_picture)



    await interaction.response.send_message(embed=embed)

    
# CS:GO

@client.tree.command(name="counter_strike_stats", description="gets the csgo stats for the user")
async def self(interaction:discord.Interaction, steamid:str):
    r = requests.get(f"https://tracker.gg/csgo/profile/steam/{steamid}/overview")
    userPage = BeautifulSoup(r.text, 'html.parser')
    classes = userPage.find_all('span', {'class': 'value'})

    username = userPage.find('span', {'class': 'trn-ign__username'})



    embed = discord.Embed(title=f"{username.text}'s stats", description="** **", color=discord.Color.orange())
    embed.add_field(name="KD", value=classes[0].text)
    embed.add_field(name="Win Rate", value=classes[2].text)
    embed.add_field(name="Kills", value=classes[4].text)

    await interaction.response.send_message(embed=embed)



# APEX LEGENDS


@client.tree.command(name="apex_legends_stats", description="Gives stats for the user")
async def self(interaction:discord.Interaction, username:str):
    r = requests.get(f"https://apex.tracker.gg/apex/profile/origin/{username}/overview")
    userPage = BeautifulSoup(r.text, 'html.parser')

    classes = userPage.find_all('span', {'class': 'value'})

    mmr = userPage.find('span', {'class': 'mmr'})
    level = classes[0].text
    kills = classes[1].text

    lgnd_name = userPage.find_all('div', {'class': 'legend__name'})
    most_played_character = str(lgnd_name[0].text)

    character_pic = userPage.find_all('img', {'class': 'legend__portrait'})
    org = str(character_pic[0])
    new_org = org.split("=")[-2]
    neww_org = new_org.replace('style', '')
    character_picture = neww_org.replace('"', '')




    embed = discord.Embed(title=f"Stats for {username}", description="** **", color=discord.Color.red())
    embed.add_field(name="MMR", value=mmr.text)
    embed.add_field(name="Level", value=level)
    embed.add_field(name="Kills", value=kills)
    embed.add_field(name="Most played character", value=most_played_character)
    embed.set_thumbnail(url=character_picture)

    await interaction.response.send_message(embed=embed)




# 


ufrz made this :)


client.run("")
    
