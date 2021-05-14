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
        latency = round(current_shard_latency[ctx.guild.shard_id + 1] * 1000)
        for guild in self.bot.guilds:
            handling_guild = len([x for x in self.bot.guilds if x.shard_id == guild.shard_id])
        shard_embed = ""
        if ctx.channel.type != discord.ChannelType.private:
            shard_embed += f"**서버의 Shard ID#{ctx.guild.shard_id} {latency}ms**\n"
        shard_embed += "```"
        for shard in self.bot.shards.values():
            shard_embed += f"Shard#{shard.id} {int(shard.latency * 1000)}ms, Guild {handling_guild}\n"
        shard_embed += "```\n"
        shard_embed += "http://audiscordbot.xyz/status"





        embed=discord.Embed(title=get_lan(ctx.author.id, "about_bot_info"), description=(shard_embed), color=color_code)
        embed.add_field(name=get_lan(ctx.author.id, "about_guild_count"), value=len(self.bot.guilds), inline=True)
        embed.add_field(name=get_lan(ctx.author.id, "about_members_count"), value=len(self.bot.users), inline=True)
        embed.add_field(name=get_lan(ctx.author.id, "about_number_of_music_playback_servers"), value=player_server_count, inline=True)
        embed.add_field(name="**사용된 오픈소스**",
                        value="[`롤 전적 오픈소스`](https://github.com/J-hoplin1/League-Of-Legend-Search-Bot)"
                              "\n[`노래봇 오픈소스`](https://github.com/NewPremium/Toaru-kagaku-no-music-bot)"
                              "\n[`자가진단 오픈소스`](https://github.com/331leo/hcskr_python)"
                              "\n[`경고 오픈소스`](https://github.com/Team-EG/j-bot-old)")
        embed.set_footer(text="audiscordbot.xyz")
        await ctx.send(embed=embed)

    @commands.command(aliases=["shard_status"])
    async def shards(self, ctx):
        """
        Check the status of every shard the bot is hosting.
        """
        text = ""
        if ctx.channel.type != discord.ChannelType.private:
            text += f"`이 서버의 Shard ID: {ctx.guild.shard_id}`\n"
        text += "```"
        for shard in self.bot.shards.values():
            text += f"Shard#{shard.id}: {int(shard.latency * 1000)}ms\n"
        text += "```"

        embed = discord.Embed(title="pong",
                              description=text
                              )
        await ctx.send(embed=embed)


    @shards.error
    async def shards_error(self, ctx, error):
        embe = discord.Embed(title="Shard", description=f"오류발생", color=0x0066ff)
        embe.set_footer(text="audiscordbot.xyz")
        if isinstance(error, commands.MissingPermissions):
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
    bot.add_cog (About (bot))
    LOGGER.info('About loaded!')
