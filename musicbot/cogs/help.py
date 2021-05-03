import discord
from discord.ext import commands

from musicbot.utils.language import get_lan
from musicbot import LOGGER, color_code, commandInt, OWNERS, EXTENSIONS


class Help (commands.Cog) :
    def __init__ (self, bot) :
        self.bot = bot

    @commands.command (name = 'help', aliases = ['도움', '도움말', '명령어', '헬프'])
    async def help (self, ctx, *, arg : str  = None) :
        if not arg == None:
            arg = arg.upper()
        if arg == "GENERAL" or arg == "일반":
            embed=discord.Embed(title=get_lan(ctx.author.id, "help_general"), description="", color=color_code)
            embed.set_footer(text="audiscordbot.xyz")

            if "about" in EXTENSIONS:
                embed.add_field(name=get_lan(ctx.author.id, "help_general_about_command").format(commandInt=commandInt),      value=get_lan(ctx.author.id, "help_general_about_info"), inline=True)

            if "other" in EXTENSIONS:
                embed.add_field(name=get_lan(ctx.author.id, "help_general_invite_command").format(commandInt=commandInt),     value=get_lan(ctx.author.id, "help_general_invite_info"), inline=True)
                embed.add_field(name=get_lan(ctx.author.id, "help_general_java_command").format(commandInt=commandInt),       value=get_lan(ctx.author.id, "help_general_java_info"), inline=True)
                embed.add_field(name=get_lan(ctx.author.id, "help_general_softver_command").format(commandInt=commandInt),    value=get_lan(ctx.author.id, "help_general_softver_info"), inline=True)

            if "ping" in EXTENSIONS:
                embed.add_field(name=get_lan(ctx.author.id, "help_general_ping_command").format(commandInt=commandInt),       value=get_lan(ctx.author.id, "help_general_ping_info"), inline=True)

            if "translation" in EXTENSIONS:
                embed.add_field(name=get_lan(ctx.author.id, "help_general_translation_command").format(commandInt=commandInt),value=get_lan(ctx.author.id, "help_general_translation_info"), inline=True)

            if "set_language" in EXTENSIONS:
                embed.add_field(name=f"`{commandInt}language`", value="Sends a list of available language packs.", inline=True)
                embed.add_field(name=f"`{commandInt}language` [*language pack*]", value="Apply the language pack.", inline=True)

            await ctx.send(embed=embed)

        elif arg == "SHOP" or arg == "상점":
            embed = discord.Embed(title="상점 명령어", description="", color=color_code)
            embed.add_field(name="`!상점`", value=">>> 상점 관련 명령어들을 보내드려요!", inline=False)
            embed.add_field(name="`!등록` <주문번호>", value=">>> 상점에서 구매한 포인트를 추가해줍니다",
                            inline=False)
            embed.add_field(name="`!보유`", value=">>> 보유하신 포인트를 알려줘요!",
                            inline=False)
            embed.add_field(name="`!상점 고음질변환`", value=">>> 고음질변환 아이템을 구매할수있어요!", inline=False)
            embed.set_footer(text="shop.audiscordbot.xyz")
            await ctx.send(embed=embed)

        elif arg == "SCHOOL" or arg == "학교":
            if "school" in EXTENSIONS:
                embed = discord.Embed(title=get_lan(ctx.author.id, "help_school"),
                                      description=get_lan(ctx.author.id, "help_school_description"), color=color_code)
                embed.set_footer(text="audiscordbot.xyz")
                embed.add_field(name=get_lan(ctx.author.id, "help_school__command").format(commandInt=commandInt),
                                value=get_lan(ctx.author.id, "help_school_info_command").format(commandInt=commandInt),
                                inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_school_meal_command").format(commandInt=commandInt),
                                value=get_lan(ctx.author.id, "help_school_info_meal").format(commandInt=commandInt),
                                inline=False)
                await ctx.send(embed=embed)

        elif arg == "UTILS" or arg == "유틸":
            embed = discord.Embed(title=get_lan(ctx.author.id, "help_utils"),
                                  description=get_lan(ctx.author.id, "help_utils_description"), color=color_code)
            embed.set_footer(text="audiscordbot.xyz")
            embed.add_field(name="`!고음질변환` <URL> or <영상제목>", value=">>> 고음질 변환 아이템을 구매한 유저가 사용할 수 있는 명령어입니다",
                            inline=False)
            embed.add_field(name=get_lan(ctx.author.id, "help_utils_convert_command").format(commandInt=commandInt),
                            value=get_lan(ctx.author.id, "help_utils_convert_info").format(commandInt=commandInt),
                            inline=False)
            embed.add_field(name=get_lan(ctx.author.id, "help_utils_shorturl_command").format(commandInt=commandInt),
                            value=get_lan(ctx.author.id, "help_utils_shorturl_info").format(commandInt=commandInt),
                            inline=False)
            embed.add_field(name=get_lan(ctx.author.id, "help_utils_randomteam_command").format(commandInt=commandInt),
                            value=get_lan(ctx.author.id, "help_utils_randomteam_info").format(commandInt=commandInt),
                            inline=False)
            embed.add_field(name=get_lan(ctx.author.id, "help_utils_randomteamvoice_command").format(commandInt=commandInt),
                            value=get_lan(ctx.author.id, "help_utils_randomteamvoice_info").format(commandInt=commandInt),
                            inline=False)
            embed.add_field(name=get_lan(ctx.author.id, "help_utils_profile_command").format(commandInt=commandInt),
                            value=get_lan(ctx.author.id, "help_utils_profile_info").format(commandInt=commandInt),
                            inline=False)
            embed.add_field(name="`!이모지생성` <들어갈 글자>", value=">>> 내용을 이용하여 최대 4글자 이모지를 만듭니다",
                            inline=False)
            embed.add_field(name=get_lan(ctx.author.id, "help_general_melon_command").format(commandInt=commandInt),
                            value=get_lan(ctx.author.id, "help_general_melon_info").format(commandInt=commandInt),
                            inline=False)
            embed.add_field(name=get_lan(ctx.author.id, "help_general_billboard_command").format(commandInt=commandInt),
                            value=get_lan(ctx.author.id, "help_general_billboard_info").format(commandInt=commandInt),
                            inline=False)
            await ctx.send(embed=embed)

        elif arg == "WARNING" or arg == "경고":
            embed = discord.Embed(title=get_lan(ctx.author.id, "help_warning"),
                                  description=get_lan(ctx.author.id, "help_warning_description"), color=color_code)
            embed.set_footer(text="audiscordbot.xyz")
            embed.add_field(name=get_lan(ctx.author.id, "help_warning_command").format(commandInt=commandInt),
                            value=get_lan(ctx.author.id, "help_warning_info").format(commandInt=commandInt),
                            inline=False)
            embed.add_field(name=get_lan(ctx.author.id, "help_warning_del_command").format(commandInt=commandInt),
                            value=get_lan(ctx.author.id, "help_warning_del_info").format(commandInt=commandInt),
                            inline=False)
            embed.add_field(name=get_lan(ctx.author.id, "help_warning_count_command").format(commandInt=commandInt),
                            value=get_lan(ctx.author.id, "help_warning_count_info").format(commandInt=commandInt),
                            inline=False)
            embed.add_field(name=get_lan(ctx.author.id, "help_warning_info_command").format(commandInt=commandInt),
                            value=get_lan(ctx.author.id, "help_warning_info_info").format(commandInt=commandInt),
                            inline=False)
            await ctx.send(embed=embed)

        elif arg == "STATS" or arg == "전적":
            embed = discord.Embed(title=get_lan(ctx.author.id, "help_stats"),
                                  description=get_lan(ctx.author.id, "help_stats_description"), color=color_code)
            embed.set_footer(text="audiscordbot.xyz")
            embed.add_field(name=get_lan(ctx.author.id, "help_lolstats_command").format(commandInt=commandInt),
                            value=get_lan(ctx.author.id, "help_lolstats_info").format(commandInt=commandInt),
                            inline=False)
            await ctx.send(embed=embed)

        elif arg == "MUSIC" or arg == "음악":
            if "music" in EXTENSIONS:
                embed=discord.Embed(title=get_lan(ctx.author.id, "help_music"), description=get_lan(ctx.author.id, "help_music_description"), color=color_code)
                embed.set_footer(text="audiscordbot.xyz")
                embed.add_field(name=get_lan(ctx.author.id, "help_music_connect_command").format(commandInt=commandInt),   value=get_lan(ctx.author.id, "help_music_connect_info").format(commandInt=commandInt), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_music_play_command").format(commandInt=commandInt),      value=get_lan(ctx.author.id, "help_music_play_info").format(commandInt=commandInt), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_music_stop_command").format(commandInt=commandInt),      value=get_lan(ctx.author.id, "help_music_stop_info").format(commandInt=commandInt), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_music_skip_command").format(commandInt=commandInt),      value=get_lan(ctx.author.id, "help_music_skip_info").format(commandInt=commandInt), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_music_vol_command").format(commandInt=commandInt),       value=get_lan(ctx.author.id, "help_music_vol_info").format(commandInt=commandInt), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_music_now_command").format(commandInt=commandInt),       value=get_lan(ctx.author.id, "help_music_now_info").format(commandInt=commandInt), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_music_q_command").format(commandInt=commandInt),         value=get_lan(ctx.author.id, "help_music_q_info").format(commandInt=commandInt), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_music_pause_command").format(commandInt=commandInt),     value=get_lan(ctx.author.id, "help_music_stop_info").format(commandInt=commandInt), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_music_shuffle_command").format(commandInt=commandInt),   value=get_lan(ctx.author.id, "help_music_shuffle_info").format(commandInt=commandInt), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_music_repeat_command").format(commandInt=commandInt),    value=get_lan(ctx.author.id, "help_music_repeat_info").format(commandInt=commandInt), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_music_seek_command").format(commandInt=commandInt),      value=get_lan(ctx.author.id, "help_music_seek_info").format(commandInt=commandInt), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_music_remove_command").format(commandInt=commandInt),    value=get_lan(ctx.author.id, "help_music_remove_info").format(commandInt=commandInt), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_music_find_command").format(commandInt=commandInt),      value=get_lan(ctx.author.id, "help_music_find_info").format(commandInt=commandInt), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_play_chart_melonplay_command").format(commandInt=commandInt),      value=get_lan(ctx.author.id, "help_play_chart_melonplay_info").format(commandInt=commandInt), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_play_chart_billboardplay_command").format(commandInt=commandInt),  value=get_lan(ctx.author.id, "help_play_chart_billboardplay_info").format(commandInt=commandInt), inline=False)
                await ctx.send(embed=embed)
        elif arg == "DEV" or arg == "개발" or arg == "개발자":
            if ctx.author.id in OWNERS:
                embed=discord.Embed(title=get_lan(ctx.author.id, "help_dev"), description=get_lan(ctx.author.id, "help_dev_description"), color=color_code)
                embed.set_footer(text="audiscordbot.xyz")
                embed.add_field(name=get_lan(ctx.author.id, "help_dev_serverlist_command").format(commandInt=commandInt),   value=get_lan(ctx.author.id, "help_dev_serverlist_info"), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_dev_modules_command").format(commandInt=commandInt),      value=get_lan(ctx.author.id, "help_dev_modules_command"), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_dev_load_command").format(commandInt=commandInt),         value=get_lan(ctx.author.id, "help_dev_load_command"), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_dev_unload_command").format(commandInt=commandInt),       value=get_lan(ctx.author.id, "help_dev_unload_command"), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_dev_reload_command").format(commandInt=commandInt),       value=get_lan(ctx.author.id, "help_dev_reload_command"), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_dev_serverinfo_command").format(commandInt=commandInt),   value=get_lan(ctx.author.id, "help_dev_serverinfo_command"), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_dev_broadcast_command").format(commandInt=commandInt),    value=get_lan(ctx.author.id, "help_dev_broadcast_command"), inline=False)
                await ctx.send(embed=embed)

        else:
            embed=discord.Embed(title=get_lan(ctx.author.id, "help"), description=get_lan(ctx.author.id, "help_info").format(bot_name=self.bot.user.name), color=color_code)
            embed.set_footer(text="audiscordbot.xyz")
            embed.add_field(name=get_lan(ctx.author.id, "help_general_command").format(commandInt=commandInt), value=get_lan(ctx.author.id, "help_general_command_info"), inline=False)

            embed.add_field(name="`!도움 상점`", value=">>> 상점 관련 명령어들을 보내드려요!", inline=False)

            if "music" in EXTENSIONS:
                embed.add_field(name=get_lan(ctx.author.id, "help_music_command").format(commandInt=commandInt), value=get_lan(ctx.author.id, "help_music_command_info"), inline=False)


            if "school" in EXTENSIONS:
                embed.add_field(name=get_lan(ctx.author.id, "help_school_command").format(commandInt=commandInt), value=get_lan(ctx.author.id, "help_school_command_info"), inline=False)

            if "short_URL" in EXTENSIONS:
                embed.add_field(name=get_lan(ctx.author.id, "help_utils_command").format(commandInt=commandInt), value=get_lan(ctx.author.id, "help_utils_command_info"), inline=False)

            if "warning" in EXTENSIONS:
                embed.add_field(name=get_lan(ctx.author.id, "help_warning_command_").format(commandInt=commandInt), value=get_lan(ctx.author.id, "help_warning_command_info"), inline=False)

            if "lol-stats" in EXTENSIONS:
                embed.add_field(name=get_lan(ctx.author.id, "help_stats_command").format(commandInt=commandInt), value=get_lan(ctx.author.id, "help_stats_command_info"), inline=False)

            if ctx.author.id in OWNERS:
                embed.add_field(name=get_lan(ctx.author.id, "help_dev_command").format(commandInt=commandInt), value=get_lan(ctx.author.id, "help_dev_command_info"), inline=False)
            await ctx.send(embed=embed)

def setup (bot) :
    bot.add_cog (Help (bot))
    LOGGER.info('Help loaded!')
