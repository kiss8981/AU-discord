from discord.ext import commands
import random

from musicbot.utils.language import get_lan
from musicbot import LOGGER, BOT_NAME_TAG_VER, color_code


class randomteam(commands.Cog):

    def __init__(self, bot):
        self.client = bot

    @commands.command(name = '팀섞', aliases = ['randomteam'])
    async def rantomteamtext(self, ctx, *, x):
        players = [y.strip() for y in x.split(' ')]
        random.shuffle(players)
        y = len(players) / 2
        team1 = ', '.join(players[:int(y)])
        team2 = ', '.join(players[int(y):])
        msg = f"```1팀:\n{team1}\n\n2팀:\n{team2}```"
        await ctx.send(msg)

    @commands.command(name = '팀섞음성', aliases = ['randomvoice'])
    async def randomteamvoice(self, ctx):
        try:
            user_voice = ctx.message.author.voice.channel.id
            channel = self.client.get_channel(user_voice)
            members = channel.members
            membername = []
            for member in members:
                membername.append(member.name)
            membername = ' '.join(membername)
            players = [y.strip() for y in membername.split(' ')]
            random.shuffle(players)
            y = len(players) / 2
            team1 = ', '.join(players[:int(y)])
            team2 = ', '.join(players[int(y):])
            msg = f"```1팀:\n{team1}\n\n2팀:\n{team2}```"
            await ctx.send(msg)
        except AttributeError:
            await ctx.send("음성채널에 입장 해주세요")


def setup(bot):
    bot.add_cog(randomteam(bot))
    LOGGER.info("randomteam loadded")
