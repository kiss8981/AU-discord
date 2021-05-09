import discord
import motor.motor_asyncio
from discord.ext import commands
from musicbot import LOGGER, color_code
from musicbot.utils import confirm

dbclient = motor.motor_asyncio.AsyncIOMotorClient("mongodb://192.168.0.13:27017")
db = dbclient.aubot


class shop(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='상점')
    async def shop(self, ctx, *, arg: str = None):
        if not arg == None:
            arg = arg.upper()
        try:
            if arg == "고음질변환":
                user_id = str(ctx.message.author.id)
                cursor1 = db.preconvert.find({"user_id": user_id})
                cursor2 = db.AUpoint.find({"user_id": user_id})
                for document in await cursor2.to_list(length=100):
                    useramount = document["point"]
                embed = discord.Embed(title="구매", description="MP3 고음질 변환권을 구매하시겠습니까? \n 500AU가 차감됩니다")
                embed.add_field(name="현재 보유 중인 포인트", value=f"{useramount}AU")
                msg = await ctx.send(embed=embed)
                res = await confirm.confirm(self.bot, ctx, msg)
                if res == True:
                    for document in await cursor1.to_list(length=100):
                        userpurchase = document["purchase"]
                    try:
                        if userpurchase == "false":
                            if useramount >= 500:
                                await db.AUpoint.update_many(
                                    {"user_id": user_id}, {"$set": {"point": int(useramount) - 500}})
                                await db.preconvert.insert_one(
                                    {"user_id": user_id, "purchase": "true"})
                                embed = discord.Embed(title="구매", description="구매가 완료되었습니다! \n `!고음질변환` 명령어를 사용하실수 있습니다")
                                return await msg.edit(embed=embed)
                            else:
                                embed = discord.Embed(title="구매", description="포인트가 부족합니다")
                                embed.add_field(name="현재 보유 중인 포인트", value=f"{useramount}AU")
                                return await msg.edit(embed=embed)
                        if userpurchase == "true":
                            embed = discord.Embed(title="구매", description="이미 구매하신 아이템입니다")
                            embed.add_field(name="현재 보유 중인 포인트", value=f"{useramount}AU")
                            return await msg.edit(embed=embed)
                    except UnboundLocalError:
                        if useramount >= 500:
                            await db.AUpoint.update_many(
                                {"user_id": user_id}, {"$set": {"point": int(useramount) - 500}})
                            await db.preconvert.insert_one(
                                {"user_id": user_id, "purchase": "true"})
                            embed = discord.Embed(title="구매", description="구매가 완료되었습니다! \n `!고음질변환` 명령어를 사용하실수 있습니다")
                            return await msg.edit(embed=embed)
                        else:
                            await db.preconvert.insert_one(
                                {"user_id": user_id, "purchase": "false"})
                            embed = discord.Embed(title="구매", description="포인트가 부족합니다")
                            embed.add_field(name="현재 보유 중인 포인트", value=f"{useramount}AU")
                            return await msg.edit(embed=embed)
                    except Exception as e:
                        embed = discord.Embed(title="상점", description="ERROR", color=color_code)
                        embed.set_footer(text="shop.audiscordbot.xyz")
                        embed.add_field(name="오류발생", value=f"{e}")
                        await ctx.send(embed=embed)
                if res == False:
                    embed = discord.Embed(title="구매", description="구매가 취소 되었습니다")
                    embed.add_field(name="현재 보유 중인 포인트", value=f"{useramount}AU")
                    return await msg.edit(embed=embed)
            if arg == "이모지생성":
                user_id = str(ctx.message.author.id)
                cursor1 = db.emojigen.find({"user_id": user_id})
                cursor2 = db.AUpoint.find({"user_id": user_id})
                for document in await cursor2.to_list(length=100):
                    useramount = document["point"]
                embed = discord.Embed(title="구매", description="이모지생성권 구매하시겠습니까? \n 5000AU가 차감됩니다")
                embed.add_field(name="현재 보유 중인 포인트", value=f"{useramount}AU")
                msg = await ctx.send(embed=embed)
                res = await confirm.confirm(self.bot, ctx, msg)
                if res == True:
                    for document in await cursor1.to_list(length=100):
                        userpurchase = document["purchase"]
                    try:
                        if userpurchase == "false":
                            if useramount >= 5000:
                                await db.AUpoint.update_many(
                                    {"user_id": user_id}, {"$set": {"point": int(useramount) - 5000}})
                                await db.emojigen.insert_one(
                                    {"user_id": user_id, "purchase": "true"})
                                embed = discord.Embed(title="구매", description="구매가 완료되었습니다! \n `!이모지생성` 명령어를 사용하실수 있습니다")
                                return await msg.edit(embed=embed)
                            else:
                                embed = discord.Embed(title="구매", description="포인트가 부족합니다")
                                embed.add_field(name="현재 보유 중인 포인트", value=f"{useramount}AU")
                                return await msg.edit(embed=embed)
                        if userpurchase == "true":
                            embed = discord.Embed(title="구매", description="이미 구매하신 아이템입니다")
                            embed.add_field(name="현재 보유 중인 포인트", value=f"{useramount}AU")
                            return await msg.edit(embed=embed)
                    except UnboundLocalError:
                        if useramount >= 500:
                            await db.AUpoint.update_many(
                                {"user_id": user_id}, {"$set": {"point": int(useramount) - 5000}})
                            await db.emojigen.insert_one(
                                {"user_id": user_id, "purchase": "true"})
                            embed = discord.Embed(title="구매", description="구매가 완료되었습니다! \n `!이모지생성` 명령어를 사용하실수 있습니다")
                            return await msg.edit(embed=embed)
                        else:
                            await db.emojigen.insert_one(
                                {"user_id": user_id, "purchase": "false"})
                            embed = discord.Embed(title="구매", description="포인트가 부족합니다")
                            embed.add_field(name="현재 보유 중인 포인트", value=f"{useramount}AU")
                            return await msg.edit(embed=embed)
                    except Exception as e:
                        embed = discord.Embed(title="상점", description="ERROR", color=color_code)
                        embed.set_footer(text="shop.audiscordbot.xyz")
                        embed.add_field(name="오류발생", value=f"{e}")
                        await ctx.send(embed=embed)
                if res == False:
                    embed = discord.Embed(title="구매", description="구매가 취소 되었습니다")
                    embed.add_field(name="현재 보유 중인 포인트", value=f"{useramount}AU")
                    return await msg.edit(embed=embed)
            else:
                embed = discord.Embed(title="상점", description="아래에 있는 명령어들을 이용해 상점을 이용해보세요!", color=color_code)
                embed.set_footer(text="shop.audiscordbot.xyz")
                embed.add_field(name="`!상점 고음질변환`", value=">>> MP3 고음질 변환권을 구매합니다", inline=False)
                embed.add_field(name="`!상점 이모지생성`", value=">>> 이모지생성권을 구매합니다", inline=False)
                embed.add_field(name="현재 보유 중인 포인트", value=f"{useramount}AU")
                await ctx.send(embed=embed)
        except UnboundLocalError:
            embed = discord.Embed(title="상점", description="아래에 있는 명령어들을 이용해 상점을 이용해보세요!", color=color_code)
            embed.set_footer(text="shop.audiscordbot.xyz")
            embed.add_field(name="`!상점 고음질변환`", value=">>> MP3 고음질 변환권을 구매합니다", inline=False)
            embed.add_field(name="`!상점 이모지생성`", value=">>> 이모지생성권을 구매합니다", inline=False)
            embed.add_field(name="현재 보유 중인 포인트", value=f"0AU", inline=False)
            embed.add_field(name="포인트가 없어 구매가 불가능합니다", value=f"https://shop.audiscordbot.xyz 에서 포인트를 구매해주세요!", inline=False)
            embed.set_footer(text="shop.audiscordbot.xyz")
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="상점", description="ERROR", color=color_code)
            embed.set_footer(text="shop.audiscordbot.xyz")
            embed.add_field(name="오류발생", value=f"{e}")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(shop(bot))
    LOGGER.info('shop Loaded!')