import urllib
import requests
import json
import time
import discord
from discord.ext import commands
from musicbot import LOGGER



class school(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command(name="급식")
    async def school_lunch(self, ctx, arg, date=None):
        if date is None:
            date = time.strftime('%d', time.localtime(time.time()))
            if date == "01":
                date = 1
            if date == "02":
                date = 2
            if date == "03":
                date = 3
            if date == "04":
                date = 4
            if date == "05":
                date = 5
            if date == "06":
                date = 6
            if date == "07":
                date = 7
            if date == "08":
                date = 8
            if date == "09":
                date = 9
        embed = discord.Embed(title=f"{arg} 급식")
        embed.add_field(name=f"{date}일 급식", value=f"{date}일 급식을 찾는중입니다...")
        embed.set_footer(text="audiscordbot.xyz")
        msg = await ctx.send(embed=embed)
        
        url = f'https://schoolmenukr.ml/code/api?q={arg}'

        data = requests.get(url).json()
        school_code = data['school_infos'][0]['code']
        school_name = data['school_infos'][0]['name']

        meal_url = f'https://schoolmenukr.ml/api/middle/{school_code}?date={date}'

        data = requests.get(meal_url).json()
        menu = data['menu'][0]['lunch']
        try:
            for i in range(0, len(menu)):
                menuall = '\n'.join(menu[:i+1])
            embed = discord.Embed(title=f"{school_name} 급식")
            embed.add_field(name=f"{date}일 급식", value=f"{menuall}\n")
            embed.set_footer(text="audiscordbot.xyz")
            await msg.edit(content="", embed=embed)
        except UnboundLocalError:
            embed = discord.Embed(title=f"{school_name} 급식")
            embed.add_field(name=f"{date}일 급식", value=f"`{date}`일은 급식이 없습니다!")
            embed.set_footer(text="audiscordbot.xyz")
            await msg.edit(content="", embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(school(bot))
    LOGGER.info("school loaded!")