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

    
    

    

    


#MISC


@tree.command(name="botinfo", description="Gives you information about the bot!", guild=discord.Object(id=724138454979575818))
async def self(interaction: discord.Interaction):
    embed = discord.Embed(title="Nov is the name!", description="** **", color=3092790)
    embed.add_field(name="Developer", value="ufrz", inline=False)
    embed.add_field(name="Language", value="Python 3.10.4", inline=False)
    embed.add_field(name="Library", value="discord.py 2.0", inline=False)
    embed.add_field(name="Guild count", value=f"{len(client.guilds)}", inline=False)
    await interaction.response.send_message(embed=embed)




client.run("MTEyNTMwMjAxODc5NDMyODA2NA.Gg-tYM.py7_ybvMxectpu1_A57FfRnj9jfYQpnhg8YaPI")
