from .hcs import asyncSelfCheck, asyncUserLogin, asyncTokenSelfCheck, asyncGenerateToken, selfcheck, userlogin, tokenselfcheck, generatetoken, versioninfo
import aiohttp
import os
import sys
import asyncio
async def UpdateCheck():
    try:
        async with aiohttp.ClientSession() as session:
            # get school organization code using given school code
            async with session.get("https://raw.githubusercontent.com/331leo/hcskr_python/main/VERSIONINFO") as response:
                VERSIONINFO = await response.text()
        VERSIONINFO=VERSIONINFO.split("#")
        if VERSIONINFO[1] == "M" and VERSIONINFO[0] > versioninfo:
            os.system(f"{sys.executable} -m pip install --upgrade hcskr")
            print("필수 모듈 업데이트가 있습니다. 자동으로 업데이트 하였습니다. 정상적인 작동을 위해 프로그램을 재실행 해주세요")
    except:
        pass
asyncio.get_event_loop().run_until_complete(UpdateCheck())