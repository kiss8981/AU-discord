import re, glob
from musicbot.utils import mp3
import urllib.request
from os.path import getsize
from youtubesearchpython import *
import discord
from discord.ext import commands
import os
import urllib.request
from musicbot import LOGGER


class mp3convert(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="변환", aliases=["mp3변환", "노래다운", "convert"])
    async def convert(self, ctx, *, arg):
        embedVar = discord.Embed(title="MP3변환", description="변환중...", color=0x0066ff)
        await ctx.send(embed=embedVar)
        url = re.findall(r'(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+', arg)
        if url:
            if len(url) == 1:
                validated_yt_url_1 = 'https://www.youtube.com/watch?v='
                validated_yt_url_2 = 'https://youtu.be/'
                if validated_yt_url_1 in url[0] or validated_yt_url_2 in url[0]:
                    mp3.song(url)
                    os.listdir()
                    for files in glob.glob('*.mp3'):
                        file_size = getsize(files)
                        file_size = int(file_size)
                        if file_size > 8000000:
                            embedVar = discord.Embed(title="7분 미만의 노래만 다운로드 가능합니다", color=0x0066ff)
                            await ctx.send(embed=embedVar)
                            os.remove(files)
                        else:
                            await ctx.send(file=discord.File(files))
                            os.remove(files)
                else:
                    await ctx.send(embed=embedVar)
            else:
                embedVar = discord.Embed(title="MP3변환", description="여러 개의 링크를 보낸 거 같습니다. 하나만 보내주세요", color=0x0066ff)
                await ctx.send(embed=embedVar)
        elif not url:
            videosSearch = VideosSearch(f'{arg}', limit=1)
            data1 = videosSearch.result()
            data2 = data1["result"][0]["id"]
            html = urllib.request.urlopen(f'https://www.youtube.com/results?search_query={data2}')
            video_ids = re.findall(r'watch\?v=(\S{11})', html.read().decode())
            new_url = 'https://www.youtube.com/watch?v=' + video_ids[0]
            mp3.song([new_url])
            os.listdir()
            for files in glob.glob('*.mp3'):
                file_size = getsize(files)
                file_size = int(file_size)
                if file_size > 8000000:
                    embe = discord.Embed(title="MP3변환", description="7분 미만의 노래만 다운로드 가능합니다.", color=0x0066ff)
                    await ctx.send(embed=embe)
                    os.remove(files)
                else:
                    embe = discord.Embed(title="MP3변환", description="변환완료...", color=0x0066ff)
                    await ctx.send(embed=embe)
                    await ctx.send(new_url)
                    await ctx.send(file=discord.File(files))
                    os.remove(files)
        else:
            embe = discord.Embed(title="MP3변환", description="명령어 방식이 잘못되었습니다", color=0x0066ff)
            await ctx.send(embed=embe)

    @convert.error
    async def convert_error(self, ctx, error):
        embed = discord.Embed(title="MP3변환", description="!변환 <제목> or <url>", color=0xe74c3c)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(mp3convert(bot))
    LOGGER.info("mp3convert loaded!")
