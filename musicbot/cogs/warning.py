from datetime import datetime
import shutil
import time
import discord
from discord.utils import get
from discord.ext import commands
from musicbot.utils.language import get_lan
import motor.motor_asyncio

dbclient = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = dbclient.test


class warning(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="경고", aliases=["warning"])
    @commands.has_permissions(manage_channels=True)
    async def warning(self, ctx, member: discord.Member, *, reason=None):
        guild_id = str(ctx.message.guild.id)
        if reason is None:
            reason = get_lan(ctx.author.id, 'warning_none')

        currenttime = time.strftime('%Y%m%d%H%M%S')
        await db.warning.insert_one(
            {"guild_id": guild_id, "user_id": str(member.id), "reason": f"{reason}, by {ctx.author}",
             "time": currenttime})

        cursor = db.warning.find({"guild_id": guild_id, "user_id": str(member.id)})
        count = 0
        for document in await cursor.to_list(length=100):
            count += 1

        try:
            if count == 1:
                role = get(ctx.guild.roles, name=get_lan(ctx.author.id, 'warning_num_1'))
                await member.add_roles(role)
            if count == 2:
                role = get(ctx.guild.roles, name=get_lan(ctx.author.id, 'warning_num_2'))
                await member.add_roles(role)
            if count == 3:
                role = get(ctx.guild.roles, name=get_lan(ctx.author.id, 'warning_num_3'))
                await member.add_roles(role)
            if count == 4:
                role = get(ctx.guild.roles, name=get_lan(ctx.author.id, 'warning_num_4'))
                await member.add_roles(role)
            if count == 5:
                role = get(ctx.guild.roles, name=get_lan(ctx.author.id, 'warning_num_5'))
                await member.add_roles(role)
            if count == 6:
                role = get(ctx.guild.roles, name=get_lan(ctx.author.id, 'warning_num_6'))
                await member.add_roles(role)
            if count == 7:
                role = get(ctx.guild.roles, name=get_lan(ctx.author.id, 'warning_num_7'))
                await member.add_roles(role)
            if count == 8:
                role = get(ctx.guild.roles, name=get_lan(ctx.author.id, 'warning_num_8'))
                await member.add_roles(role)
            if count == 9:
                role = get(ctx.guild.roles, name=get_lan(ctx.author.id, 'warning_num_9'))
                await member.add_roles(role)
            if count == 10:
                role = get(ctx.guild.roles, name=get_lan(ctx.author.id, 'warning_num_10'))
                await member.add_roles(role)
        except:
            await ctx.send(get_lan(ctx.author.id, 'warning_error'))

        await ctx.send(
            get_lan(ctx.author.id, 'warning_data').format(member=member.mention, reason=reason, num=str(currenttime),
                                                          count=count))

    @warning.error
    async def 경고_error(self, ctx, error):
        embed = discord.Embed(title=get_lan(ctx.author.id, 'warning'),
                              description=get_lan(ctx.author.id, 'warning_error_2'), color=0xe74c3c)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=embed)
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(get_lan(ctx.author.id, 'member_none'))

    @commands.command(name="누적경고", aliases=["warcount", "warc", "warningcount"])
    async def warningcount(self, ctx, member: discord.Member = None):
        guild_id = str(ctx.message.guild.id)
        member = ctx.author if not member else member
        cases = []
        cursor = db.warning.find({"guild_id": guild_id, "user_id": str(member.id)})
        for document in await cursor.to_list(length=100):
            cases.append(document["time"])
        embed = discord.Embed(title=get_lan(ctx.author.id, 'warning_ac'),
                              description=get_lan(ctx.author.id, 'warning_ac'.format(member=member)),
                              colour=discord.Color.red())
        embed.add_field(name=get_lan(ctx.author.id, 'warning_number'), value=f'{cases}')

        await ctx.send(embed=embed)

    @warningcount.error
    async def warcount_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(get_lan(ctx.author.id, 'member_none'))

    @commands.command(name="경고정보", aliases=['warinfo', 'warninginfo', 'warin'])
    async def warninginfo(self, ctx, member: discord.Member, num):
        guild_id = str(ctx.message.guild.id)
        cursor = db.warning.find({"guild_id": guild_id, "user_id": str(member.id), "time": num})
        for document in await cursor.to_list(length=100):
            case = document["reason"]

        embed = discord.Embed(title=get_lan(ctx.author.id, 'warninginfo_detail'), description=f"{member.mention}",
                              colour=discord.Color.red())
        embed.add_field(name=get_lan(ctx.author.id, 'warning_number'), value=f'{num}')
        embed.add_field(name=get_lan(ctx.author.id, 'warning_detail'), value=f'{case}', inline=False)

        await ctx.send(embed=embed)

    @warninginfo.error
    async def warninginfo_error(self, ctx, error):
        embed = discord.Embed(title=get_lan(ctx.author.id, 'warning'),
                              description=get_lan(ctx.author.id, 'warning_info_error'), colour=0x74c3c)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=embed)
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(get_lan(ctx.author.id, 'member_none'))

    @commands.command(name="경고삭제", aliases=["delwar", "wardel", "warningdel"])
    @commands.has_permissions(manage_channels=True)
    async def warningdel(self, ctx, member: discord.Member, num):
        guild_id = str(ctx.message.guild.id)
        cursor = db.warning.find({"guild_id": guild_id, "user_id": str(member.id)})
        count = 0
        for doc in await cursor.to_list(length=100):
            count += 1
        try:
            if count == 1:
                role = get(ctx.guild.roles, name=get_lan(ctx.author.id, 'warning_num_1'))
                await member.remove_roles(role)
            if count == 2:
                role = get(ctx.guild.roles, name=get_lan(ctx.author.id, 'warning_num_2'))
                await member.remove_roles(role)
            if count == 3:
                role = get(ctx.guild.roles, name=get_lan(ctx.author.id, 'warning_num_3'))
                await member.remove_roles(role)
            if count == 4:
                role = get(ctx.guild.roles, name=get_lan(ctx.author.id, 'warning_num_4'))
                await member.remove_roles(role)
            if count == 5:
                role = get(ctx.guild.roles, name=get_lan(ctx.author.id, 'warning_num_5'))
                await member.remove_roles(role)
            if count == 6:
                role = get(ctx.guild.roles, name=get_lan(ctx.author.id, 'warning_num_6'))
                await member.remove_roles(role)
            if count == 7:
                role = get(ctx.guild.roles, name=get_lan(ctx.author.id, 'warning_num_7'))
                await member.remove_roles(role)
            if count == 8:
                role = get(ctx.guild.roles, name=get_lan(ctx.author.id, 'warning_num_8'))
                await member.remove_roles(role)
            if count == 9:
                role = get(ctx.guild.roles, name=get_lan(ctx.author.id, 'warning_num_9'))
                await member.remove_roles(role)
            if count == 10:
                role = get(ctx.guild.roles, name=get_lan(ctx.author.id, 'warning_num_10'))
                await member.remove_roles(role)
        except:
            pass

        cursor = db.warning.find({"guild_id": guild_id, "user_id": str(member.id), "time": num})
        count = 0
        for doc in await cursor.to_list(length=100):
            count += 1

        if count == 1:
            await db.warning.delete_one({"guild_id": guild_id, "user_id": str(member.id), "time": num})
            await ctx.send(get_lan(ctx.author.id, 'wardel_msg'))
        elif count == 0:
            await ctx.send(get_lan(ctx.author.id, 'warning_none'))

    @warningdel.error
    async def warningdel_error(self, ctx, error):
        embed = discord.Embed(title=get_lan(ctx.author.id, 'warning'),
                              description=get_lan(ctx.author.id, 'wardel_mssarg'), color=0xe74c3c)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=embed)
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(get_lan(ctx.author.id, 'member_none'))


def setup(bot):
    bot.add_cog(warning(bot))
