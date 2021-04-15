import time
import discord
from discord.ext import commands
from musicbot import LOGGER, color_code

class Ping (commands.Cog) :
    def __init__ (self, bot) :
        self.bot = bot

    @commands.command (name = 'ping', aliases = ['핑'])
    async def ping(self, ctx):
        latancy = self.bot.latency
        before = time.monotonic()
        embed=discord.Embed(title="**Ping**", description=f'ping_pong: Pong! WebSocket Ping {round(latancy * 1000)}ms\n:ping_pong: Pong! Measuring...', color=color_code)
        embed.set_footer(text="audiscordbot.xyz")
        message = await ctx.send(embed=embed)
        ping = (time.monotonic() - before) * 1000
        current_shard_latency = ctx.bot.latencies[ctx.guild.shard_id]
        latency = round(current_shard_latency[ctx.guild.shard_id + 1] * 1000)
        for guild in self.bot.guilds:
            handling_guild = len([x for x in self.bot.guilds if x.shard_id == guild.shard_id])
        shard_embed = ""
        if ctx.channel.type != discord.ChannelType.private:
            shard_embed += f"**Server Shard ID#{ctx.guild.shard_id} {latency}ms**\n"
        shard_embed += "```"
        for shard in self.bot.shards.values():
            shard_embed += f"Shard#{shard.id} {int(shard.latency * 1000)}ms, Guild {handling_guild}\n"
        shard_embed += "```\n"
        shard_embed += "http://audiscordbot.xyz/status"
        embed = discord.Embed(title="**Ping**", description=shard_embed, color=color_code)
        embed.set_footer(text="audiscordbot.xyz")
        embed.add_field(name="**Discord Ping**", value=f":ping_pong: Pong! WebSocket Ping {round(latancy * 1000)}ms\n:ping_pong: Pong! Message Ping {int(ping)}ms")
        await message.edit(embed=embed)

def setup (bot) :
    bot.add_cog (Ping (bot))
    LOGGER.info('Ping loaded!')
