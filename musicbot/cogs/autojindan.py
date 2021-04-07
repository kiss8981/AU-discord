import hcskr
import discord
import logging
import datetime
from discord.ext import commands
from musicbot import LOGGER
from pymongo import MongoClient
import asyncio
import motor.motor_asyncio



dbclient = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = dbclient.TEST


class autojindan(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="자가진단설정",usage=f"[이름] [생년월일6자] [지역] [학교종류] [학교] [비밀번호]")
    @commands.dm_only()
    async def autojindanset(self, ctx, name:str, birthday:str, area:str, pos:str, schoolname:str, password:str):
        user_id = str(ctx.author.id)
        user_name = str(ctx.author)
        hcskr_result = await hcskr.asyncGenerateToken(name, birthday, area, schoolname, pos, password)
        if hcskr_result['error']:
            LOGGER.info(f"{ctx.author} 자가진단 설정에 실패하였습니다. {hcskr_result['message']}")
            embed = discord.embeds.Embed(title=f"자가진단 등록 오류", description=f"```{hcskr_result['message']}```")
            return await ctx.reply(embed=embed)
        token = hcskr_result['token']
        await db.autojindanDB.insert_one({"user_name": user_name, "user_id": user_id, "token": token})
        embed = discord.embeds.Embed(title=f"자가진단 등록 성공", description=f"매일 아침 7시경에 자동으로 자가 진단이 수행됩니다!\n자가진단 기록은 [여기](http://discord.gg/cs3EGVf3Qd)에서 확인가능합니다", author=ctx.author)
        await ctx.reply(embed=embed)
        LOGGER.info(f"{ctx.author}자가진단 정보를 성공적으로 등록하였습니다!.")

    @autojindanset.error
    async def autojindanset_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.embeds.Embed(title="자동 자가진단", description="`!자가진단설정 [이름] [생년월일6자] [지역] [학교종류] [학교] [비밀번호]`")
            embed.add_field(name="지원하는 모든 지역", value="+ 서울, 서울시, 서울교육청, 서울시교육청, 서울특별시\n+ 부산, 부산광역시, 부산시, 부산교육청, 부산광역시교육청\n+ 대구, 대구광역시, 대구시, 대구교육청, 대구광역시교육청\n+ 인천, 인천광역시, 인천시, 인천교육청, 인천광역시교육청\n+ 광주, 광주광역시, 광주시, 광주교육청, 광주광역시교육청\n+ 대전, 대전광역시, 대전시, 대전교육청, 대전광역시교육청\n+ 울산, 울산광역시, 울산시, 울산교육청, 울산광역시교육청\n+ 세종, 세종특별시, 세종시, 세종교육청, 세종특별자치시, 세종특별자치시교육청\n+ 경기, 경기도, 경기교육청, 경기도교육청\n+ 강원, 강원도, 강원교육청, 강원도교육청\n+ 충북, 충청북도, 충북교육청, 충청북도교육청\n+ 충남, 충청남도, 충남교육청, 충청남도교육청\n+ 전북, 전라북도, 전북교육청, 전라북도교육청\n+ 전남, 전라남도, 전남교육청, 전라남도교육청\n+ 경북, 경상북도, 경북교육청, 경상북도교육청\n+ 경남, 경상남도, 경남교육청, 경상남도교육청\n+ 제주, 제주도, 제주특별자치시, 제주교육청, 제주도교육청, 제주특별자치시교육청, 제주특별자치도", inline=False)
            embed.add_field(name="지원하는 모든 학교종류", value="+ 유치원, 유, 유치\n+ 초등학교, 초, 초등\n+ 중학교, 중, 중등\n+ 고등학교, 고, 고등\n+ 특수학교, 특, 특수, 특별", inline=False)
            await ctx.send(embed=embed)
        if isinstance(error, commands.PrivateMessageOnly):
            embed = discord.embeds.Embed(title="자동 자가진단", description="`!자가진단설정` 명령어는 DM채널에서만 사용가능합니다")
            await ctx.send(embed=embed)




def setup(bot: commands.Bot):
    bot.add_cog(autojindan(bot))
    LOGGER.info("autojindan loaded!")