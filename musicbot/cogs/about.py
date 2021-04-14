import discord
from discord.ext import commands

from musicbot.utils.language import get_lan
from musicbot import LOGGER, color_code

class About (commands.Cog) :
    def __init__ (self, bot) :
        self.bot = bot

    @commands.command (aliases = ['봇', '개발자', '봇정보', '봇관련', '관련', '정보'])
    async def about (self, ctx) :
        player_server_count=0
        for i in self.bot.guilds:
            player = self.bot.lavalink.player_manager.get(int(i.id))
            try:
                if player.is_connected:
                    player_server_count+=1
            except Exception:
                pass
        current_shard_latency = ctx.bot.latencies[ctx.guild.shard_id]
        latency = round(current_shard_latency[1] * 1000)
        for guild in self.bot.guilds:
            handling_guild = len([x for x in self.bot.guilds if x.shard_id == guild.shard_id])
        embed=discord.Embed(title=get_lan(ctx.author.id, "about_bot_info"), description=(f"""Shard #{ctx.guild.shard_id} : Ping {latency}ms, Guild {handling_guild}"""), color=color_code)
        embed.add_field(name=get_lan(ctx.author.id, "about_guild_count"), value=len(self.bot.guilds), inline=True)
        embed.add_field(name=get_lan(ctx.author.id, "about_members_count"), value=len(self.bot.users), inline=True)
        embed.add_field(name=get_lan(ctx.author.id, "about_number_of_music_playback_servers"), value=player_server_count, inline=True)
        embed.set_footer(text="audiscordbot.xyz")
        await ctx.send(embed=embed)

def setup (bot) :
    bot.add_cog (About (bot))
    LOGGER.info('About loaded!')
