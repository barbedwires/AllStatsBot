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


class abot(discord.Client):
    def __init__(self):
        super().__init__(intents=INTENTS)
        self.synced = False
    
    async def on_ready(self):
        await tree.sync(guild=discord.Object(id=724138454979575818))
        self.synced = True
        print("Bot is online!")


client = abot()
tree = app_commands.CommandTree(client)


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




# stats

@tree.command(name="osu_stats", description="Gives you stats on an osu user", guild=discord.Object(id=724138454979575818))
async def self(interaction: discord.Interaction, username: str):
    baseUrl = 'https://osu.ppy.sh/api/{}?k=e7842270927e45016fef5cbe4ed44c3fe2c96440'
    url = baseUrl.format("get_user") + "&u=" + username
    r = requests.get(url)
    stats = r.json()
    seconds_played = int(stats[0]['total_seconds_played'])
    hours_played = (datetime.timedelta(seconds=seconds_played))
    embed = discord.Embed(title=f"{username}'s stats", description="** **", color=3092790)
    embed.add_field(name="PP rank", value=stats[0]['pp_rank'], inline=False)
    embed.add_field(name="Accuracy", value=stats[0]['accuracy'], inline=False)
    embed.add_field(name="Sign up Date", value=stats[0]['join_date'], inline=False)
    embed.add_field(name="Play time", value=hours_played, inline=False)


    await interaction.response.send_message(embed=embed)



@tree.command(name="r6_stats", description="Gives the stats of someones Rainbow Six Seige Profile", guild=discord.Object(id=724138454979575818))
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


@tree.command(name="r6_ranked_stats", description="Gives the ranked stats of the users Rainbow Six Seige profile", guild=discord.Object(id=724138454979575818))
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

    
    

    

    


#MISC


@tree.command(name="botinfo", description="Gives you information about the bot!", guild=discord.Object(id=724138454979575818))
async def self(interaction: discord.Interaction):
    embed = discord.Embed(title="GameStats+", description="** **", color=3092790)
    embed.add_field(name="Developer", value="ufrz", inline=False)
    embed.add_field(name="Language", value="Python 3.10.4", inline=False)
    embed.add_field(name="Library", value="discord.py 2.0", inline=False)
    embed.add_field(name="Guild count", value=f"{len(client.guilds)}", inline=False)
    await interaction.response.send_message(embed=embed)









client.run("token")
