import re, glob
from musicbot.utils import mp3
import urllib.request
from os.path import getsize
import motor.motor_asyncio
from youtubesearchpython import *
import discord
from discord.ext import commands
import os
import urllib.request
from musicbot import LOGGER


dbclient = motor.motor_asyncio.AsyncIOMotorClient("mongodb://192.168.0.13:27017")
db = dbclient.aubot

class mp3convert(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="변환", aliases=["mp3변환", "노래다운", "convert"])
    async def convert(self, ctx, *, arg):
        try:
            embedVar = discord.Embed(title="MP3변환", description="변환중...", color=0x0066ff)
            embedVar.set_footer(text="audiscordbot.xyz")
            msg = await ctx.send(embed=embedVar)
            url = re.findall(r'(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+', arg)
            if url:
                if len(url) == 1:
                    validated_yt_url_1 = 'https://www.youtube.com/watch?v='
                    validated_yt_url_2 = 'https://youtu.be/'
                    if validated_yt_url_1 in url[0] or validated_yt_url_2 in url[0]:
                        mp3.songlow(url)
                        os.listdir()
                        for files in glob.glob('*.mp3'):
                            file_size = getsize(files)
                            file_size = int(file_size)
                            if file_size > 8000000:
                                embe = discord.Embed(title="MP3변환", description="7분 미만의 노래만 다운로드 가능합니다.", color=0x0066ff)
                                embe.add_field(name="긴 영상을 다운로드하시려면 고음질 MP3 변환권을 구매하셔야 합니다", value="`!상점` 을 이용해주세요")
                                embe.set_footer(text="audiscordbot.xyz")
                                await msg.edit(content="", embed=embe)
                                os.remove(files)
                            else:
                                embe = discord.Embed(title="MP3변환", description=f"{url}", color=0x0066ff)
                                embe.add_field(name="고음질 MP3 변환권을 구매하실 수 있습니다!", value="`!상점` 을 이용해주세요")
                                embe.set_footer(text="audiscordbot.xyz")
                                await msg.edit(content="", embed=embe)
                                await ctx.send(file=discord.File(files))
                                os.remove(files)
                    else:
                        await ctx.send(content="", embed=embedVar)
                else:
                    embedVar = discord.Embed(title="MP3변환", description="여러 개의 링크를 보낸 거 같습니다. 하나만 보내주세요", color=0x0066ff)
                    embedVar.set_footer(text="audiscordbot.xyz")
                    await msg.edit(content="", embed=embedVar)
            elif not url:
                videosSearch = VideosSearch(f'{arg}', limit=1)
                data1 = videosSearch.result()
                data2 = data1["result"][0]["id"]
                html = urllib.request.urlopen(f'https://www.youtube.com/results?search_query={data2}')
                video_ids = re.findall(r'watch\?v=(\S{11})', html.read().decode())
                new_url = 'https://www.youtube.com/watch?v=' + video_ids[0]
                mp3.songlow([new_url])
                os.listdir()
                for files in glob.glob('*.mp3'):
                    file_size = getsize(files)
                    file_size = int(file_size)
                    if file_size > 4500000:
                        embe = discord.Embed(title="MP3변환", description="5분 미만의 노래만 다운로드 가능합니다.", color=0x0066ff)
                        embe.add_field(name="긴 영상을 다운로드하시려면 고음질 MP3 변환권을 구매하셔야 합니다", value="`!상점` 을 이용해주세요")
                        embe.set_footer(text="audiscordbot.xyz")
                        await msg.edit(content="", embed=embe)
                        os.remove(files)
                    else:
                        embe = discord.Embed(title="MP3변환", description=f"{new_url}", color=0x0066ff)
                        embe.add_field(name="고음질 MP3 변환권을 구매하실 수 있습니다!", value="`!상점` 을 이용해주세요")
                        embe.set_footer(text="audiscordbot.xyz")
                        await msg.edit(content="", embed=embe)
                        await ctx.send(file=discord.File(files))
                        os.remove(files)
            else:
                embe = discord.Embed(title="MP3변환", description="명령어 방식이 잘못되었습니다", color=0x0066ff)
                embe.set_footer(text="audiscordbot.xyz")
                await msg.edit(content="", embed=embe)
        except commands.MissingRequiredArgument:
            embed = discord.Embed(title="MP3변환", description="!변환 <제목> or <url>", color=0xe74c3c)
            embed.set_footer(text="audiscordbot.xyz")
            await ctx.reply(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="MP3변환", description=f"{e}", color=0xe74c3c)
            embed.set_footer(text="audiscordbot.xyz")
            await ctx.reply(embed=embed)


    @commands.command(name="고음질변환", aliases=["고음질mp3변환", "고음질노래다운", "preconvert"])
    async def preconvert(self, ctx, *, arg):
        user_id = str(ctx.message.author.id)
        cursor = db.preconvert.find({"user_id": user_id})
        for document in await cursor.to_list(length=100):
            purchase = document["purchase"]
        try:
            if purchase == "true":
                embedVar = discord.Embed(title="고음질 MP3변환", description="변환중...", color=0x0066ff)
                embedVar.set_footer(text="audiscordbot.xyz")
                msg = await ctx.send(embed=embedVar)
                url = re.findall(r'(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+', arg)
                if url:
                    if len(url) == 1:
                        validated_yt_url_1 = 'https://www.youtube.com/watch?v='
                        validated_yt_url_2 = 'https://youtu.be/'
                        if validated_yt_url_1 in url[0] or validated_yt_url_2 in url[0]:
                            mp3.songhigh(url)
                            os.listdir()
                            for files in glob.glob('*.mp3'):
                                file_size = getsize(files)
                                file_size = int(file_size)
                                if file_size > 8300000:
                                    embedVar = discord.Embed(title="7분 미만의 노래만 다운로드 가능합니다", color=0x0066ff)
                                    embedVar.set_footer(text="audiscordbot.xyz")
                                    await msg.edit(content="", embed=embedVar)
                                    os.remove(files)
                                else:
                                    await ctx.send(file=discord.File(files))
                                    os.remove(files)
                        else:
                            await ctx.send(content="", embed=embedVar)
                    else:
                        embedVar = discord.Embed(title="MP3변환", description="여러 개의 링크를 보낸 거 같습니다. 하나만 보내주세요", color=0x0066ff)
                        embedVar.set_footer(text="audiscordbot.xyz")
                        await msg.edit(content="", embed=embedVar)
                elif not url:
                    videosSearch = VideosSearch(f'{arg}', limit=1)
                    data1 = videosSearch.result()
                    data2 = data1["result"][0]["id"]
                    html = urllib.request.urlopen(f'https://www.youtube.com/results?search_query={data2}')
                    video_ids = re.findall(r'watch\?v=(\S{11})', html.read().decode())
                    new_url = 'https://www.youtube.com/watch?v=' + video_ids[0]
                    mp3.songhigh([new_url])
                    os.listdir()
                    for files in glob.glob('*.mp3'):
                        file_size = getsize(files)
                        file_size = int(file_size)
                        if file_size > 8300000:
                            embe = discord.Embed(title="고음질 MP3변환", description="7분 미만의 노래만 다운로드 가능합니다.", color=0x0066ff)
                            embe.set_footer(text="audiscordbot.xyz")
                            await msg.edit(content="", embed=embe)
                            os.remove(files)
                        else:
                            embe = discord.Embed(title="고음질 MP3변환", description="변환완료...", color=0x0066ff)
                            embe.set_footer(text="audiscordbot.xyz")
                            await msg.edit(content="", embed=embe)
                            await ctx.send(new_url)
                            await ctx.send(file=discord.File(files))
                            os.remove(files)
                else:
                    embe = discord.Embed(title="MP3변환", description="명령어 방식이 잘못되었습니다", color=0x0066ff)
                    embe.set_footer(text="audiscordbot.xyz")
                    await msg.edit(content="", embed=embe)
            else:
                embe = discord.Embed(title="MP3변환", description=f"고음질 변환권 미구매 유저입니다", color=0x0066ff)
                embe.add_field(name="고음질 MP3 변환권을 구매하실 수 있습니다!", value="`!상점` 을 이용해주세요")
                embe.set_footer(text="audiscordbot.xyz")
                await ctx.send(embed=embe)
        except UnboundLocalError:
            embe = discord.Embed(title="MP3변환", description=f"고음질 변환권 미구매 유저입니다", color=0x0066ff)
            embe.add_field(name="고음질 MP3 변환권을 구매하실 수 있습니다!", value="`!상점` 을 이용해주세요")
            embe.set_footer(text="audiscordbot.xyz")
            await ctx.send(embed=embe)
        except Exception as e:
            embe = discord.Embed(title="MP3변환", description=f"ERROR", color=0x0066ff)
            embe.add_field(name="오류", value=f"{e}")
            embe.set_footer(text="audiscordbot.xyz")
            await ctx.send(embed=embe)

    @convert.error
    async def convert_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="MP3변환", description="!변환 <제목> or <url>", color=0xe74c3c)
            embed.set_footer(text="audiscordbot.xyz")
            await ctx.send(embed=embed)
        if isinstance(error, Exception):
            embed = discord.Embed(title="MP3변환", description=f"{Exception}", color=0xe74c3c)
            embed.set_footer(text="audiscordbot.xyz")
            await ctx.send(embed=embed)

    @preconvert.error
    async def preconvert_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="MP3변환", description="!고음질변환 <제목> or <url>", color=0xe74c3c)
            embed.set_footer(text="audiscordbot.xyz")
            await ctx.send(embed=embed)



def setup(bot: commands.Bot):
    bot.add_cog(mp3convert(bot))
    LOGGER.info("mp3convert loaded!")
