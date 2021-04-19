import discord
from discord.ext import commands
import os
from musicbot import LOGGER
from musicbot.utils.emojigne import generate_emoji
from PIL import Image
import random
from time import sleep

class emojigenerator(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="이모지생성")
    async def emojigen(self, ctx, arg):
        if len(arg) >= 5:
            embed = discord.Embed(title="이모지생성", description="오류발생", color=0xe74c3c)
            embed.set_footer(text="audiscordbot.xyz")
            embed.add_field(name="최대치 초과", value="이모지는 최대 4글자까지 생성 가능합니다")
            await ctx.send(embed=embed)
        else:
            msg = await ctx.reply("이모지 생성중...")
            guild = ctx.guild
            rnum = random.randint(0, 1000)
            generate_emoji(arg, rnum)
            await msg.edit(content="이모지 생성중.")
            await msg.edit(content="이모지 생성중..")
            sleep(3)
            await msg.edit(content="이모지 생성중...")
            if ctx.author.guild_permissions.manage_emojis:
                await msg.edit(content="이모지 업로드중...")
                with open(f"emoji/{rnum}.png", 'rb') as fd:
                    emoji = await guild.create_custom_emoji(image=fd.read(), name=f"emoji_{rnum}")
                await msg.edit(content=f'이모지 생성을 완료했습니다! <:{rnum}:{emoji.id}>')
                os.remove(f'emoji/{rnum}.png')
            else:
                await msg.edit(content="권한이 없습니다!")

    @emojigen.error
    async def emojigen_error(self, ctx, error):
        embed = discord.Embed(title="이모지생성", description="오류발생", color=0xe74c3c)
        embed.set_footer(text="audiscordbot.xyz")
        if isinstance(error, commands.MissingRequiredArgument):
            embed.add_field(name="MissingRequiredArgument", value="!이모지생성 <원하는 단어>")
            await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(emojigenerator(bot))
    LOGGER.info("mojigenerator loaded!")