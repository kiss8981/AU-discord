import discord
from discord.ext import commands
import requests
from urllib.parse import quote
import re  # Regex for youtube link
import warnings
from musicbot import LOGGER

def remove_tag(content):
   cleanr =re.compile('<.*?>')
   cleantext = re.sub(cleanr, '', content)
   return cleantext


class lostArk(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="로스트아크", aliases=["로아전적", "로아", "lostark"])
    async def lolstats(self, ctx, *, arg):
        APIsearch = 'http://localhost:8080/crawler/userdata?name='
        playerNickname = arg
        # Open URL
        URL = requests.get(APIsearch + playerNickname)
        data = URL.json()

        ability = []

        embed = discord.Embed(title=f"{playerNickname}님의 전적", description="", color=0x5CD1E5)
        try:
            embed.add_field(name="클래스", value=data['msg']['characterClass'], inline=False)
        except:
            pass
        try:
            embed.add_field(name="아이템 레벨", value=data['msg']['itemLevel'] + ' 레벨')
        except:
            pass
        try:
            embed.add_field(name="원정대 레벨", value=data['msg']['expeditionLevel'] + ' 레벨')
        except:
            pass
        try:
            embed.add_field(name="전투 레벨", value=data['msg']['battleLevel'] + ' 레벨')
        except:
            pass
        try:
            embed.add_field(name="머리", value=remove_tag(data['msg']['item']['hat']['Element_000']['value']))
        except:
            pass
        try:
            embed.add_field(name="견갑", value=remove_tag(data['msg']['item']['pauldrons']['Element_000']['value']))
        except:
            pass
        try:
            embed.add_field(name="상의", value=remove_tag(data['msg']['item']['top']['Element_000']['value']))
        except:
            pass
        try:
            embed.add_field(name="하의", value=remove_tag(data['msg']['item']['pants']['Element_000']['value']))
        except:
            pass
        try:
            embed.add_field(name="장갑", value=remove_tag(data['msg']['item']['gloves']['Element_000']['value']))
        except:
            pass
        try:
            embed.add_field(name="무기", value=remove_tag(data['msg']['item']['weapon']['Element_000']['value']))
        except:
            pass
        try:
            embed.set_thumbnail(url=f'{data["msg"]["characterImg"]}')
        except:
            pass
        try:
            for i in range(len(data['msg']['ability'])):
                ability.append(data['msg']['ability'][i]['name'])
            embed.add_field(name="각인", value=('\n').join(ability), inline=False)
        except:
            if data['msg'] == '유저를 찾을 수 없거나 아무 아이템도 장착되어 있지 않습니다':
                embed.add_field(name='정보가 없습니다', value='유저를 찾을 수 없거나 아무 아이템도 장착되어 있지 않습니다')
            else:
                embed.add_field(name="각인", value='적용된 각인 효과가 없습니다', inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(lostArk(bot))
    LOGGER.info("lostArk loaded!")