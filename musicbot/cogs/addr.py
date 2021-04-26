import discord
import requests
from discord.ext import commands
from musicbot import LOGGER, color_code, commandInt, OWNERS, EXTENSIONS


class addr (commands.Cog) :
    def __init__ (self, bot) :
        self.bot = bot


    @commands.command(name="주소검색")
    async def address(self, ctx, *, keyword: str = None):
        if keyword == None:
            return await ctx.send("장소를 입력해주세요\n예시: !주소검색 홍대입구")
        else:
            try:
                url = f'https://dapi.kakao.com/v2/local/search/keyword.json?query={keyword}'
                headers = {"Authorization": "KakaoAK <RestAPIkey>"}
                name = requests.get(url, headers=headers).json()['documents'][0]['place_name']
                address = requests.get(url, headers=headers).json()['documents'][0]['address_name']
                phone = requests.get(url, headers=headers).json()['documents'][0]['phone']
                road_address = requests.get(url, headers=headers).json()['documents'][0]['road_address_name']
                category = requests.get(url, headers=headers).json()['documents'][0]['category_group_name']
                x = requests.get(url, headers=headers).json()['documents'][0]['x']
                y = requests.get(url, headers=headers).json()['documents'][0]['y']
                keyword = keyword.replace(" ", "%20")
                maps = f"[링크](https://map.kakao.com/link/map/{keyword},{y},{x})"
                if phone == "":
                    phone = "없음"
                if address == "":
                    address = "없음"
                if road_address == "":
                    road_address = "없음"
                if category == "":
                    category = "없음"
                embed = discord.Embed(title=f"{name} 검색결과")
                embed.add_field(name="이름", value=name, inline=False)
                embed.add_field(name="주소", value=address)
                embed.add_field(name="도로명주소", value=road_address)
                embed.add_field(name="전화번호", value=phone, inline=False)
                embed.add_field(name="종류", value=category)
                embed.add_field(name="지도", value=maps, inline=False)
                await ctx.send(embed=embed)
            except IndexError:
                await ctx.send(f"찾을수 없는 장소입니다!")
            except Exception as e:
                await ctx.send(f"오류가 발생했어요 \n{e}")

def setup (bot) :
    bot.add_cog (addr (bot))
    LOGGER.info('addr loaded!')