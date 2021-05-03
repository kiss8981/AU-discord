import discord
import motor.motor_asyncio
from discord.ext import commands
from musicbot import LOGGER

dbclient = motor.motor_asyncio.AsyncIOMotorClient("mongodb://192.168.0.13:27017")
db = dbclient.aubot


class addcoin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="등록")
    async def addcoin(self, ctx, uuid):
        user_id = str(ctx.message.author.id)
        cursor = db.payments.find({"orderId": uuid})
        cursor2 = db.AUpoint.find({"user_id": user_id})
        try:
            for document in await cursor2.to_list(length=100):
                user_id = document["user_id"]
                useramount = document["point"]
        except UnboundLocalError:
            await db.AUpoint.insert_one(
                {"user_id": user_id, "point": 0})
        for document in await cursor.to_list(length=100):
            amount = document["totalAmount"]
            useage = document["useage"]
        try:
            if useage == "true":
                embed = discord.embeds.Embed(title="AU Point", description="등록실패", color=0xFF0000)
                embed.add_field(name="정보", value=f"이미 사용된 코드입니다")
                embed.set_footer(text="shop.audiscordbot.xyz")
                await ctx.send(embed=embed)
            elif useage == "false":
                try:
                    await db.AUpoint.update_many(
                        {"user_id": user_id}, {"$set": {"point": int(useramount) + int(amount)}})
                    await db.payments.update_many({"orderId": uuid}, {"$set": {"useage": "true"}})
                    cursor2 = db.AUpoint.find({"user_id": user_id})
                    for document in await cursor2.to_list(length=100):
                        useramount = document["point"]
                    embed = discord.embeds.Embed(title="AU Point", description="등록완료", color=0x88FF00)
                    embed.add_field(name="현제 보유중인 코인", value=f"{useramount}AU")
                    embed.set_footer(text="shop.audiscordbot.xyz")
                    await ctx.send(embed=embed)
                except UnboundLocalError:
                    await db.AUpoint.insert_one(
                        {"user_id": user_id, "point": 0})
                    embed = discord.embeds.Embed(title="AU Point", description="등록완료", color=0x88FF00)
                    embed.add_field(name="DB등록완료", value=f"다시 입력해주세요!")
                    embed.set_footer(text="shop.audiscordbot.xyz")
                    await ctx.send(embed=embed)
        except UnboundLocalError:
            embed = discord.embeds.Embed(title="AU Point", description="등록실패", color=0xFF0000)
            embed.add_field(name="에러", value=f"찾을수 없는 코드입니다")
            embed.set_footer(text="shop.audiscordbot.xyz")
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.embeds.Embed(title="AU Point", description="등록실패", color=0xFF0000)
            embed.add_field(name="에러", value=f"{e}")
            embed.set_footer(text="shop.audiscordbot.xyz")
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(addcoin(bot))
    LOGGER.info('Owners Loaded!')