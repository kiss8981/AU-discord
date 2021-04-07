import discord
from discord.ext import commands
from musicbot.utils.language import get_lan
from musicbot import LOGGER


class profile(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="프로필")
    async def profile(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        embed = discord.Embed(title=get_lan(ctx.author.id, "profile"), description= f"{member}{get_lan(ctx.author.id, 'profile-nim')}")
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(profile(bot))
    LOGGER.info("profile loaded!")