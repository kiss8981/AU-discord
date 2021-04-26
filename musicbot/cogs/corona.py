import requests
import json
import re  # 계산을 위한 특수문자 제거
import discord
from discord.ext import commands
from musicbot import LOGGER


class corona (commands.Cog) :
    def __init__ (self, bot) :
        self.bot = bot

    @commands.command(name="코로나")
    async def corona(self, ctx):
        korea = "http://api.corona-19.kr/korea?serviceKey="
        country = "http://api.corona-19.kr/korea/country?serviceKey="
        key = ""  # API 키(https://api.corona-19.kr/)

        response = requests.get(korea + key)
        text = response.text
        data = json.loads(text)

        response2 = requests.get(country + key)
        text2 = response2.text
        data2 = json.loads(text2)

        code = response.status_code
        code2 = response2.status_code

        if code == 200:
            if code2 == 200:
                embed = discord.embeds.Embed(title="코로나 국내 발생현황", description=f"{data['updateTime']}")
                embed.add_field(name="확진자(금일추가)", value=f"{data['TotalCase']}명 (+ {data2['data0_1']}명)")
                embed.add_field(name="완치자(금일추가)", value=f"{data['TotalRecovered']}명 (+ {data['TodayRecovered']}명)")
                embed.add_field(name="사망자(금일추가)", value=f"{data['TotalDeath']}명 (+ {data['TodayDeath']}명)")

                a = int(re.sub('[-=.,#/?:$}]', '', data["caseCount"]))
                b = int(re.sub('[-=.,#/?:$}]', '', data["TotalChecking"]))
                caseper = a / b * 100  # 확진율계산법: 양성/검사완료수 * 100

                embed.add_field(name='확진율', value=f"{round(caseper, 2)}%")
                embed.add_field(name='완치율', value=f"{data['recoveredPercentage']}%")
                embed.add_field(name='사망률', value=f"{data['deathPercentage']}%")
                embed.set_footer(text="audiscordbot.xyz")
                await ctx.send(embed=embed)
            else:
                print('=== [ ERROR REPORTING ] ===')
                print("\n")
                print("API 키가 입력되지 않으면 401 Unauthorized 오류가 발생할 수 있습니다. 주석에 있는 설명을 읽어주세요.")
                print("\n")
                print('API Response Code(KOREA):', data["resultCode"])
                print('API Response Message(KOREA):', data["resultMessage"])
                print("\n")
                print('API Response Code(COUNTRY):', data2["resultCode"])
                print('API Response Message(COUNTRY):', data2["resultMessage"])
                print("\n")
        else:
            print('=== [ ERROR REPORTING ] ===')
            print("\n")
            print("API 키가 입력되지 않으면 401 Unauthorized 오류가 발생할 수 있습니다. 주석에 있는 설명을 읽어주세요.")
            print("\n")
            print('API Response Code(KOREA):', data["resultCode"])
            print('API Response Message(KOREA):', data["resultMessage"])
            print("\n")
            print('API Response Code(COUNTRY):', data2["resultCode"])
            print('API Response Message(COUNTRY):', data2["resultMessage"])

def setup(bot: commands.Bot):
    bot.add_cog(corona(bot))
    LOGGER.info("corona loaded!")