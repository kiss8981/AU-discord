import discord
from discord.ext import commands
import os
from musicbot import LOGGER
from musicbot.utils.emojigne import generate_emoji
from PIL import Image
import motor.motor_asyncio
import random
from time import sleep

dbclient = motor.motor_asyncio.AsyncIOMotorClient("mongodb://192.168.0.13:27017")
db = dbclient.aubot

class emojigenerator(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="이모지생성")
    async def emojigen(self, ctx, arg, fontcolor: str = None, fonttype: str = None):
        user_id = str(ctx.message.author.id)
        cursor = db.emojigen.find({"user_id": user_id})
        for document in await cursor.to_list(length=100):
            purchase = document["purchase"]
        try:
            if purchase == "true":
                if len(arg) >= 5:
                    embed = discord.Embed(title="이모지생성", description="오류발생", color=0xe74c3c)
                    embed.set_footer(text="audiscordbot.xyz")
                    embed.add_field(name="최대치 초과", value="이모지는 최대 4글자까지 생성 가능합니다")
                    await ctx.send(embed=embed)
                else:
                    msg = await ctx.reply("이모지 생성중...")
                    guild = ctx.guild
                    rnum = random.randint(0, 1000)
                    generate_emoji(arg, rnum, fonttype, fontcolor)
                    sleep(3)
                    if ctx.author.guild_permissions.manage_emojis:
                        await msg.edit(content="이모지 업로드중...")
                        with open(f"emoji/{rnum}.png", 'rb') as fd:
                            emoji = await guild.create_custom_emoji(image=fd.read(), name=f"emoji_{rnum}")
                        await msg.edit(content=f'이모지 생성을 완료했습니다! <:{rnum}:{emoji.id}>')
                        os.remove(f'emoji/{rnum}.png')
                    else:
                        await msg.edit(content="권한이 없습니다!")
            else:
                embe = discord.Embed(title="MP3변환", description=f"고음질 변환권 미구매 유저입니다", color=0x0066ff)
                embe.add_field(name="고음질 MP3 변환권을 구매하실 수 있습니다!", value="`!상점` 을 이용해주세요")
                embe.set_footer(text="audiscordbot.xyz")
                await ctx.send(embed=embe)
        except UnboundLocalError:
            embe = discord.Embed(title="이모지생성", description=f"이모지생성권 미구매 유저입니다", color=0x0066ff)
            embe.add_field(name="이모지생성권을 구매하실 수 있습니다!", value="`!상점` 을 이용해주세요")
            embe.set_footer(text="audiscordbot.xyz")
            await ctx.send(embed=embe)
        except Exception as e:
            embe = discord.Embed(title="이모지생성", description=f"오류발생", color=0x0066ff)
            embe.add_field(name="오류", value=f"{e}")
            embe.set_footer(text="audiscordbot.xyz")
            await ctx.send(embed=embe)

    @emojigen.error
    async def emojigen_error(self, ctx, error):
        embe = discord.Embed(title="이모지생성", description=f"오류발생", color=0x0066ff)
        embe.set_footer(text="audiscordbot.xyz")
        if isinstance(error, commands.MissingRequiredArgument):
            embe.add_field(name="MissingRequiredArgument",
                           value=f"`!이모지생성` <들어갈 글자> <글시체> <색상>\n 상세한 명령어는 `!명령어 이모지` 에서 확인해주세요")
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








def setup(bot):
    bot.add_cog(emojigenerator(bot))
    LOGGER.info("mojigenerator loaded!")