import asyncio
from base64 import b64decode, b64encode
import aiohttp
from .mapping import schoolinfo
import sys
import base64
import inspect
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
import jwt #This module is "PyJWT" https://pypi.org/project/PyJWT/

versioninfo = "1.9.2"

pubkey = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA81dCnCKt0NVH7j5Oh2+SGgEU0aqi5u6sYXemouJWXOlZO3jqDsHYM1qfEjVvCOmeoMNFXYSXdNhflU7mjWP8jWUmkYIQ8o3FGqMzsMTNxr+bAp0cULWu9eYmycjJwWIxxB7vUwvpEUNicgW7v5nCwmF5HS33Hmn7yDzcfjfBs99K5xJEppHG0qc+q3YXxxPpwZNIRFn0Wtxt0Muh1U8avvWyw03uQ/wMBnzhwUC8T4G5NclLEWzOQExbQ4oDlZBv8BM/WxxuOyu0I8bDUDdutJOfREYRZBlazFHvRKNNQQD2qDfjRz484uFs7b5nykjaMB9k/EJAuHjJzGs9MMMWtQIDAQAB=="
def encrypt(n):
    rsa_public_key = b64decode(pubkey)
    pub_key = RSA.importKey(rsa_public_key)

    cipher = Cipher_pkcs1_v1_5.new(pub_key)
    msg = n.encode('utf-8')

    default_encrypt_length = 245
    length = default_encrypt_length
    msg_list = [msg[i:i + length] for i in list(range(0, len(msg), length))]
    encrypt_msg_list = []
    for msg_str in msg_list:
        cipher_text = base64.b64encode(cipher.encrypt(message=msg_str))
        encrypt_msg_list.append(cipher_text)
    return encrypt_msg_list[0].decode("utf-8")


def selfcheck(name, birth, area, schoolname, level, password, customloginname=None, loop=asyncio.get_event_loop()):
    return loop.run_until_complete(asyncSelfCheck(name, birth, area, schoolname, level, password, customloginname))
def userlogin(name, birth, area, schoolname, level, password, loop=asyncio.get_event_loop()):
    return loop.run_until_complete(asyncUserLogin(name,birth,area,schoolname,level,password))
def generatetoken(name, birth, area, schoolname, level, password, loop=asyncio.get_event_loop()):
    return loop.run_until_complete(asyncGenerateToken(name, birth, area, schoolname, level, password))
def tokenselfcheck(token, loop=asyncio.get_event_loop()):
    return loop.run_until_complete(asyncTokenSelfCheck(token))

async def asyncSelfCheck(name, birth, area, schoolname, level, password, customloginname=None):
    if customloginname == None:
        customloginname = name
    login_result = await asyncUserLogin(name, birth, area, schoolname, level, password)
    if login_result["error"]:
        return login_result
    token = login_result['token']
    info = login_result['info']
    schoolcode = login_result['schoolcode']
    async with aiohttp.ClientSession() as session:
        # Hcs getUserInfo Request
        endpoint = f"https://{info['schoolurl']}hcs.eduro.go.kr/v2/getUserInfo"
        headers = {"Content-Type": "application/json", "Authorization": token}
        data = {"orgCode":schoolcode}
        async with session.post(endpoint, json=data, headers=headers) as response:
            try:
                res = await response.json()
                token = res['token']
            except:
                return {"error": True, "code": "UNKNOWN", "message": "getUserInfo: 알 수 없는 에러 발생."}
        # Servey Register
        endpoint = f"https://{info['schoolurl']}hcs.eduro.go.kr/registerServey"
        headers = {"Content-Type": "application/json", "Authorization": token}
        surveydata = {"rspns01": "1", "rspns02": "1", "rspns00": "Y",
                        "upperToken": token, "upperUserNameEncpt": customloginname}

        async with session.post(endpoint, json=surveydata, headers=headers) as response:
            res = await response.json()
            try:
                return {
                    "error": False,
                    "code": "SUCCESS",
                    "message": "성공적으로 자가진단을 수행하였습니다.",
                    "regtime": res["registerDtm"],
                }
            except:
                return {"error": True, "code": "UNKNOWN", "message": "알 수 없는 에러 발생."}


async def asyncUserLogin(name, birth, area, schoolname, level, password):
    name = encrypt(name)  # Encrypt Name
    birth = encrypt(birth)  # Encrypt Birth
    password = encrypt(password) # Encrypt Password
    try:
        info = schoolinfo(area, level)  # Get schoolInfo from Hcs API
    except:
        return {"error": True, "code": "FORMET", "message": "지역명이나 학교급을 잘못 입력하였습니다."}
    url = f"https://hcs.eduro.go.kr/v2/searchSchool?lctnScCode={info['schoolcode']}&schulCrseScCode={info['schoollevel']}&orgName={schoolname}&loginType=school"

    # REST Client open
    async with aiohttp.ClientSession() as session:
        # Get Request to given Url
        async with session.get(url) as response:
            school_infos = await response.json()

            if len(school_infos["schulList"]) > 5:
                return {
                    "error": True,
                    "code": "NOSCHOOL",
                    "message": "너무 많은 학교가 검색되었습니다. 지역, 학교급을 제대로 입력하고 학교 이름을 보다 상세하게 적어주세요.",
                }

            try:
                schoolcode = school_infos["schulList"][0]["orgCode"]
            except:
                return {
                    "error": True,
                    "code": "NOSCHOOL",
                    "message": "검색 가능한 학교가 없습니다. 지역, 학교급을 제대로 입력하였는지 확인해주세요.",
                }

        # Trying Login Session for get auth token

        data = {"orgCode": schoolcode, "name": name, "birthday": birth, "loginType": "school", "stdntPNo": None}
        endpoint = f"https://{info['schoolurl']}hcs.eduro.go.kr/v2/findUser"

        async with session.post(endpoint, json=data) as response:
            res = await response.json()
            try:
                token = res["token"]
            except:
                return {
                    "error": True,
                    "code": "NOSTUDENT",
                    "message": "학교는 검색하였으나, 입력한 정보의 학생을 찾을 수 없습니다.",
                }

        # Hcs Password vaildtion
        headers = {"Content-Type": "application/json", "Authorization": token}
        data = {"password":password,"deviceUuid":""}
        endpoint = f"https://{info['schoolurl']}hcs.eduro.go.kr/v2/validatePassword"

        async with session.post(endpoint, json=data,headers=headers) as response:

            try:
                res = await response.json()
                try:
                    if res['isError']:
                        return {
                            "error": True,
                            "code": "PASSWORD",
                            "message": "학생정보는 검색하였으나, 비밀번호가 틀립니다.",
                            }
                except:
                    token = res
            except:
                return {"error": True, "code": "UNKNOWN", "message": "validatePassword: 알 수 없는 에러 발생."}
        try:
            caller_name = str(sys._getframe(1).f_code.co_name)
        except:
            caller_name = None
        if caller_name == "asyncSelfCheck":
            return {"error": False, "code": "SUCCESS", "message": "유저 로그인 성공!", "token": token, "info": info, "schoolcode":schoolcode}
        return {"error": False, "code": "SUCCESS", "message": "유저 로그인 성공!"}

async def asyncGenerateToken(name, birth, area, schoolname, level, password):
    login_result = await asyncUserLogin(name, birth, area, schoolname, level, password)
    if login_result['error']:
        return login_result
    data = {"name": str(name), "birth": str(birth), "area": str(area), "schoolname": str(schoolname), "level": str(level), "password": str(password)}
    jwt_token = jwt.encode(data, pubkey, algorithm="HS256")
    if isinstance(jwt_token, str):
        jwt_token = jwt_token.encode("utf8")
    token = b64encode(jwt_token).decode("utf8")
    return {"error": False, "code": "SUCCESS", "message": "자가진단 토큰 발급 성공!", "token": token}
    
async def asyncTokenSelfCheck(token):
    try:
        data = jwt.decode(b64decode(token), pubkey, algorithms="HS256")
    except Exception as e:
        return {"error": True, "code": "WRONGTOKEN", "message": "올바르지 않은 토큰입니다."}
    return await asyncSelfCheck(data['name'], data['birth'], data['area'], data['schoolname'], data['level'], data['password'])
