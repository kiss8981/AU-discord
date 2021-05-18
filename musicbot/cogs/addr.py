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
                maps = f"[길찾기](https://map.kakao.com/link/to/{keyword},{y},{x})"
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

    @address.error
    async def address_error(self, ctx, error):
        embe = discord.Embed(title="주소검색", description=f"오류발생", color=0x0066ff)
        embe.set_footer(text="audiscordbot.xyz")
        if isinstance(error, commands.MissingRequiredArgument):
            embe.add_field(name="MissingRequiredArgument",
                           value=f"장소를 입력해주세요\n예시: !주소검색 홍대입구")
            await ctx.send(embed=embe)
        elif isinstance(error, commands.MissingPermissions):
            embe.add_field(name="MissingPermissions", value="이 명령어를 실행할 권한이 없습니다\n"
                                                            f"필요한 권한: `{', '.join(error.missing_perms)}`")
            await ctx.send(embed=embe)
        elif isinstance(error, commands.CheckFailure):
            embe.add_field(name="CheckFailure", value="당신은 이 명령어를 사용할 수 없습니다.")
            await ctx.send(embed=embe)
        elif isinstance(error, commands.BotMissingPermissions):
            embe.add_field(name="BotMissingPermissions",
                           value=f"권한이 없습니다!")
            await ctx.send(embed=embe)
        else:
            embe.add_field(name="오류발생",
                           value=f"{error}")
            await ctx.send(embed=embe)

def setup (bot) :
    bot.add_cog (addr (bot))
    LOGGER.info('addr loaded!')