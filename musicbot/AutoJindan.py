import motor.motor_asyncio
import hcskr
import datetime
import discord
import asyncio

from musicbot import TOKEN, LOGGER

client = discord.Client()
dbclient = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = dbclient.test

@client.event
async def on_ready():
    LOGGER.info("자가진단 실행...")
    count_all = 0
    count_success = 0
    count_fail = 0
    cursor = db.autojindanDB.find({})
    for document in await cursor.to_list(length=5000):
        count_all += 1
        try:
            hcsdata = await hcskr.asyncTokenSelfCheck(document.get("token"))
            if hcsdata.get("error"):
                count_fail += 1
                LOGGER.error(f"{document.get('user_name')}({document.get('user_id')}): 자가진단 수행실패, {hcsdata}")  # 로깅
            else:
                count_success += 1
                LOGGER.info(f"{document.get('user_name')}({document.get('user_id')}): 자가진단 수행 성공!, {hcsdata}")  # 로깅
        except Exception as e:
            LOGGER.exception(f"자가진단 수행중 에러발생!: {e}\n")  # 로깅
            print(document)
            count_fail += 1
            continue
    LOGGER.warning(
        f"\n---------------{datetime.datetime.now()}---------------\n오늘의 자가진단 결과:\n전체 이용자 수: {count_all}\n성공: {count_success}\n실패: {count_fail}\n---------------------------------------------")  # 로깅
    await client.get_channel(int(828551043272278056)).send(
        f"```전체 이용자 수: {count_all}\n성공: {count_success}\n실패: {count_fail}```")
    await asyncio.sleep(10)
    quit()



client.run(TOKEN)