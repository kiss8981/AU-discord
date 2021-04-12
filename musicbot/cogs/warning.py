import json
from datetime import datetime
import os
import shutil
import time
import discord
from discord.utils import get
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument
from musicbot.utils.language import get_lan


class warning(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="경고", aliases=["warning"])
    @commands.has_permissions(manage_channels=True)
    async def warning(self, ctx, member: discord.Member, *, reason=None):
        guild_id = str(ctx.message.guild.id)
        if reason is None:
            reason = get_lan(ctx.author.id, 'warning_none')

        data_exist = os.path.isfile(f"data/guild_data/{guild_id}/admin.json")
        if data_exist:
            pass
        else:
            try:
                shutil.copy('data/guild_data/data.json', f'data/guild_data/{guild_id}/admin.json')
            except:
                os.mkdir(f'data/guild_data/{guild_id}/')
                shutil.copy('data/guild_data/data.json', f'data/guild_data/{guild_id}/admin.json')

        currenttime = time.strftime('%Y%m%d%H%M%S')

        with open(f'data/guild_data/{guild_id}/admin.json', 'r') as f:
            warn_data = json.load(f)

        try:
            warn_data[str(member.id)]["warn"][str(currenttime)] = f"{reason}, by {ctx.author}"
        except KeyError:
            warn_data[str(member.id)] = {}
            warn_data[str(member.id)]["warn"] = {}
            warn_data[str(member.id)]["warn"][str(currenttime)] = f"{reason}, by <@{ctx.author.id}>"

        with open(f'data/guild_data/{guild_id}/admin.json', 'w') as s:
            json.dump(warn_data, s, indent=4)

        with open(f'data/guild_data/{guild_id}/admin.json', 'r') as f:
            warn_data = json.load(f)

        count = len(warn_data[str(member.id)]["warn"])

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

        await ctx.send(get_lan(ctx.author.id, 'warning_data').format(member=member.mention, reason=reason, num=str(currenttime), count=count))

    @warning.error
    async def 경고_error(self, ctx, error):
        embed = discord.Embed(title=get_lan(ctx.author.id, 'warning'), description=get_lan(ctx.author.id, 'warning_error_2'), color=0xe74c3c)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=embed)
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(get_lan(ctx.author.id, 'member_none'))

    @commands.command(name="누적경고", aliases=["warcount", "warc", "warningcount"])
    async def warningcount(self, ctx, member: discord.Member = None):
        try:
            guild_id = str(ctx.message.guild.id)
            member = ctx.author if not member else member

            with open(f'data/guild_data/{guild_id}/admin.json', 'r') as f:
                warn_data = json.load(f)

            global cases

            try:
                cases = str(warn_data[str(member.id)]["warn"].keys())
            except KeyError:
                cases = None
            except FileNotFoundError:
                await ctx.send(get_lan(ctx.author.id, 'warning_none'))

            if cases is None:
                cases = get_lan(ctx.author.id, 'warning_case_none')

            else:
                cases = cases.lstrip('dict_keys([')
                cases = cases.rstrip('])')

            embed = discord.Embed(title=get_lan(ctx.author.id, 'warning_ac'), description=get_lan(ctx.author.id, 'warning_ac'.format(member=member)), colour=discord.Color.red())
            embed.add_field(name=get_lan(ctx.author.id, 'warning_number'), value=f'{cases}')

            await ctx.send(embed=embed)
        except:
            await ctx.send(get_lan(ctx.author.id, 'warning_case_error'))

    @warningcount.error
    async def warcount_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(get_lan(ctx.author.id, 'member_none'))

    @commands.command(name="경고정보", aliases=['warinfo', 'warninginfo', 'warin'])
    async def warninginfo(self, ctx, member: discord.Member, num):
        global case
        guild_id = str(ctx.message.guild.id)
        with open(f'data/guild_data/{guild_id}/admin.json', 'r') as f:
            warn_data = json.load(f)

        try:
            case = warn_data[str(member.id)]["warn"][str(num)]
        except KeyError:
            await ctx.send(get_lan(ctx.author.id, 'warning_case_none'))
            return

        embed = discord.Embed(title=get_lan(ctx.author.id, 'warninginfo_detail'), description=get_lan(ctx.author.id, 'warning_ac_de'.format(member=member)), colour=discord.Color.red())
        embed.add_field(name=get_lan(ctx.author.id, 'warning_number'), value=f'{num}')
        embed.add_field(name=get_lan(ctx.author.id, 'warning_detail'), value=f'{case}', inline=False)

        await ctx.send(embed=embed)

    @warninginfo.error
    async def warninginfo_error(self, ctx, error):
        embed = discord.Embed(title=get_lan(ctx.author.id, 'warning'), description=get_lan(ctx.author.id, 'warning_info_error'), colour=0x74c3c)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=embed)
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(get_lan(ctx.author.id, 'member_none'))

    @commands.command(name="경고삭제", aliases=["delwar", "wardel", "warningdel"])
    @commands.has_permissions(manage_channels=True)
    async def warningdel(self, ctx, member: discord.Member, num):
        guild_id = str(ctx.message.guild.id)

        with open(f'data/guild_data/{guild_id}/admin.json', 'r') as f:
            warn_data = json.load(f)
        count = len(warn_data[str(member.id)]["warn"])
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

        try:
            del warn_data[str(member.id)]["warn"][str(num)]
            with open(f'data/guild_data/{guild_id}/admin.json', 'w') as s:
                json.dump(warn_data, s, indent=4)
            await ctx.send(get_lan(ctx.author.id, 'wardel_msg'))
        except KeyError:
            await ctx.send(get_lan(ctx.author.id, 'warning_none'))
        except FileNotFoundError:
            await ctx.send(get_lan(ctx.author.id, 'warning_none'))
        except MissingRequiredArgument:
            await ctx.send(get_lan(ctx.author.id, 'wardel_mssarg'))

    @warningdel.error
    async def warningdel_error(self, ctx, error):
        embed = discord.Embed(title=get_lan(ctx.author.id, 'warning'), description=get_lan(ctx.author.id, 'wardel_mssarg'), color=0xe74c3c)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=embed)
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(get_lan(ctx.author.id, 'member_none'))




def setup(bot):
    bot.add_cog(warning(bot))
