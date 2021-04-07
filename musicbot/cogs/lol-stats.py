import discord
from discord.ext import commands
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import quote
import re  # Regex for youtube link
import warnings
from musicbot import LOGGER

tierScore = {
    'default': 0,
    'iron': 1,
    'bronze': 2,
    'silver': 3,
    'gold': 4,
    'platinum': 5,
    'diamond': 6,
    'master': 7,
    'grandmaster': 8,
    'challenger': 9
}


def tierCompare(solorank, flexrank):
    if tierScore[solorank] > tierScore[flexrank]:
        return 0
    elif tierScore[solorank] < tierScore[flexrank]:
        return 1
    else:
        return 2


def deleteTags(htmls):
    for a in range(len(htmls)):
        htmls[a] = re.sub('<.+?>', '', str(htmls[a]), 0).strip()
    return htmls


warnings.filterwarnings(action='ignore')


class lol_stats(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="롤전적", aliases=["전적롤", "전적_롤", "lolstats"])
    async def lolstats(self, ctx, *, arg):
        opggsummonersearch = 'https://www.op.gg/summoner/userName='
        playerNickname = arg
        # Open URL
        checkURLBool = urlopen(opggsummonersearch + quote(playerNickname))
        bs = BeautifulSoup(checkURLBool, 'html.parser')

        # 자유랭크 언랭은 뒤에 '?image=q_auto&v=1'표현이없다

        # Patch Note 20200503에서
        # Medal = bs.find('div', {'class': 'ContentWrap tabItems'}) 이렇게 바꾸었었습니다.
        # PC의 설정된 환경 혹은 OS플랫폼에 따라서 ContentWrap tabItems의 띄어쓰기가 인식이

        Medal = bs.find('div', {'class': 'SideContent'})
        RankMedal = Medal.findAll('img', {'src': re.compile(
            '\/\/[a-z]*\-[A-Za-z]*\.[A-Za-z]*\.[A-Za-z]*\/[A-Za-z]*\/[A-Za-z]*\/[a-z0-9_]*\.png')})
        # Variable RankMedal's index 0 : Solo Rank
        # Variable RankMedal's index 1 : Flexible 5v5 rank

        # for mostUsedChampion
        mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
        mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})

        # 솔랭, 자랭 둘다 배치가 안되어있는경우 -> 사용된 챔피언 자체가 없다. 즉 모스트 챔피언 메뉴를 넣을 필요가 없다.

        # Scrape Summoner's Rank information
        # [Solorank,Solorank Tier]
        solorank_Types_and_Tier_Info = deleteTags(bs.findAll('div', {'class': {'RankType', 'TierRank'}}))
        # [Solorank LeaguePoint, Solorank W, Solorank L, Solorank Winratio]
        solorank_Point_and_winratio = deleteTags(
            bs.findAll('span', {'class': {'LeaguePoints', 'wins', 'losses', 'winratio'}}))
        # [Flex 5:5 Rank,Flexrank Tier,Flextier leaguepoint + W/L,Flextier win ratio]
        flexrank_Types_and_Tier_Info = deleteTags(bs.findAll('div', {
            'class': {'sub-tier__rank-type', 'sub-tier__rank-tier', 'sub-tier__league-point',
                      'sub-tier__gray-text'}}))
        # ['Flextier W/L]
        flexrank_Point_and_winratio = deleteTags(bs.findAll('span', {'class': {'sub-tier__gray-text'}}))

        # embed.set_imag()는 하나만 들어갈수 있다.

        # 솔랭, 자랭 둘다 배치 안되어있는 경우 -> 모스트 챔피언 출력 X
        if len(solorank_Point_and_winratio) == 0 and len(flexrank_Point_and_winratio) == 0:
            embed = discord.Embed(title="소환사 전적검색", description="", color=0x5CD1E5)
            embed.add_field(name="솔로랭크 : 언랭크", value="언랭크", inline=False)
            embed.add_field(name="자유랭크 : 언랭크", value="언랭크", inline=False)
            embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
            await ctx.send(playerNickname + "님의 전적", embed=embed)

        # 솔로랭크 기록이 없는경우
        elif len(solorank_Point_and_winratio) == 0:

            # most Used Champion Information : Champion Name, KDA, Win Rate
            mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
            mostUsedChampion = mostUsedChampion.a.text.strip()
            mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})
            mostUsedChampionKDA = mostUsedChampionKDA.text.split(':')[0]
            mostUsedChampionWinRate = bs.find('div', {'class': "Played"})
            mostUsedChampionWinRate = mostUsedChampionWinRate.div.text.strip()

            FlexRankTier = flexrank_Types_and_Tier_Info[0] + ' : ' + flexrank_Types_and_Tier_Info[1]
            FlexRankPointAndWinRatio = flexrank_Types_and_Tier_Info[2] + " /" + \
                                       flexrank_Types_and_Tier_Info[-1]
            embed = discord.Embed(title="소환사 전적검색", description="", color=0x5CD1E5)
            embed.add_field(name="솔로랭크 : 언랭크", value="언랭크", inline=False)
            embed.add_field(name=FlexRankTier, value=FlexRankPointAndWinRatio, inline=False)
            embed.add_field(name="모스트 챔피언 : " + mostUsedChampion,
                            value="KDA : " + mostUsedChampionKDA + " / " + " 승률 : " + mostUsedChampionWinRate,
                            inline=False)
            embed.set_thumbnail(url='https:' + RankMedal[1]['src'])
            await ctx.send(playerNickname + "님의 전적", embed=embed)

        # 자유랭크 기록이 없는경우
        elif len(flexrank_Point_and_winratio) == 0:

            # most Used Champion Information : Champion Name, KDA, Win Rate
            mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
            mostUsedChampion = mostUsedChampion.a.text.strip()
            mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})
            mostUsedChampionKDA = mostUsedChampionKDA.text.split(':')[0]
            mostUsedChampionWinRate = bs.find('div', {'class': "Played"})
            mostUsedChampionWinRate = mostUsedChampionWinRate.div.text.strip()

            SoloRankTier = solorank_Types_and_Tier_Info[0] + ' : ' + solorank_Types_and_Tier_Info[1]
            SoloRankPointAndWinRatio = solorank_Point_and_winratio[0] + "/ " + solorank_Point_and_winratio[
                1] + " " + solorank_Point_and_winratio[2] + " /" + solorank_Point_and_winratio[3]
            embed = discord.Embed(title="소환사 전적검색", description="", color=0x5CD1E5)
            embed.add_field(name=SoloRankTier, value=SoloRankPointAndWinRatio, inline=False)
            embed.add_field(name="자유랭크 : 언랭크", value="언랭크", inline=False)
            embed.add_field(name="모스트 챔피언 : " + mostUsedChampion,
                            value="KDA : " + mostUsedChampionKDA + " / " + "승률 : " + mostUsedChampionWinRate,
                            inline=False)
            embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
            await ctx.send(playerNickname + "님의 전적", embed=embed)
        # 두가지 유형의 랭크 모두 완료된사람
        else:
            # 더 높은 티어를 thumbnail에 안착
            solorankmedal = RankMedal[0]['src'].split('/')[-1].split('?')[0].split('.')[0].split('_')
            flexrankmedal = RankMedal[1]['src'].split('/')[-1].split('?')[0].split('.')[0].split('_')

            # Make State
            SoloRankTier = solorank_Types_and_Tier_Info[0] + ' : ' + solorank_Types_and_Tier_Info[1]
            SoloRankPointAndWinRatio = solorank_Point_and_winratio[0] + "/ " + solorank_Point_and_winratio[
                1] + " " + solorank_Point_and_winratio[2] + " /" + solorank_Point_and_winratio[3]
            FlexRankTier = flexrank_Types_and_Tier_Info[0] + ' : ' + flexrank_Types_and_Tier_Info[1]
            FlexRankPointAndWinRatio = flexrank_Types_and_Tier_Info[2] + " /" + \
                                       flexrank_Types_and_Tier_Info[-1]

            # most Used Champion Information : Champion Name, KDA, Win Rate
            mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
            mostUsedChampion = mostUsedChampion.a.text.strip()
            mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})
            mostUsedChampionKDA = mostUsedChampionKDA.text.split(':')[0]
            mostUsedChampionWinRate = bs.find('div', {'class': "Played"})
            mostUsedChampionWinRate = mostUsedChampionWinRate.div.text.strip()

            cmpTier = tierCompare(solorankmedal[0], flexrankmedal[0])
            if SoloRankTier == "Ranked Solo : Challenger":
                SoloRankTier = "솔로랭크 : 첼린저"
            if SoloRankTier == "Ranked Solo : Grandmaster":
                SoloRankTier = "솔로랭크 : 그랜드마스터"
            if SoloRankTier == "Ranked Solo : Master":
                SoloRankTier = "솔로랭크 : 마스터"
            if SoloRankTier == "Ranked Solo : Diamond 1":
                SoloRankTier = "솔로랭크 : 다이아 1"
            if SoloRankTier == "Ranked Solo : Diamond 2":
                SoloRankTier = "솔로랭크 : 다이아 2"
            if SoloRankTier == "Ranked Solo : Diamond 3":
                SoloRankTier = "솔로랭크 : 다이아 3"
            if SoloRankTier == "Ranked Solo : Diamond 4":
                SoloRankTier = "솔로랭크 : 다이아 4"
            if SoloRankTier == "Ranked Solo : Platinum 1":
                SoloRankTier = "솔로랭크 : 플래티넘 1"
            if SoloRankTier == "Ranked Solo : Platinum 2":
                SoloRankTier = "솔로랭크 : 플래티넘 2"
            if SoloRankTier == "Ranked Solo : Platinum 3":
                SoloRankTier = "솔로랭크 : 플래티넘 3"
            if SoloRankTier == "Ranked Solo : Platinum 4":
                SoloRankTier = "솔로랭크 : 플래티넘 4"
            if SoloRankTier == "Ranked Solo : Gold 1":
                SoloRankTier = "솔로랭크 : 골드 1"
            if SoloRankTier == "Ranked Solo : Gold 2":
                SoloRankTier = "솔로랭크 : 골드 2"
            if SoloRankTier == "Ranked Solo : Gold 3":
                SoloRankTier = "솔로랭크 : 골드 3"
            if SoloRankTier == "Ranked Solo : Gold 4":
                SoloRankTier = "솔로랭크 : 골드 4"
            if SoloRankTier == "Ranked Solo : Silver 1":
                SoloRankTier = "솔로랭크 : 실버 1"
            if SoloRankTier == "Ranked Solo : Silver 2":
                SoloRankTier = "솔로랭크 : 실버 2"
            if SoloRankTier == "Ranked Solo : Silver 3":
                SoloRankTier = "솔로랭크 : 실버 3"
            if SoloRankTier == "Ranked Solo : Silver 4":
                SoloRankTier = "솔로랭크 : 실버 4"
            if SoloRankTier == "Ranked Solo : Bronze 1":
                SoloRankTier = "솔로랭크 : 브론즈 1"
            if SoloRankTier == "Ranked Solo : Bronze 2":
                SoloRankTier = "솔로랭크 : 브론즈 2"
            if SoloRankTier == "Ranked Solo : Bronze 3":
                SoloRankTier = "솔로랭크 : 브론즈 3"
            if SoloRankTier == "Ranked Solo : Bronze 4":
                SoloRankTier = "솔로랭크 : 브론즈 4"
            if SoloRankTier == "Ranked Solo : Iron 1":
                SoloRankTier = "솔로랭크 : 아이언 1"
            if SoloRankTier == "Ranked Solo : Iron 2":
                SoloRankTier = "솔로랭크 : 아이언 2"
            if SoloRankTier == "Ranked Solo : Iron 3":
                SoloRankTier = "솔로랭크 : 아이언 3"
            if SoloRankTier == "Ranked Solo : Iron 4":
                SoloRankTier = "솔로랭크 : 아이언 4"
            if FlexRankTier == "Flex 5:5 Rank : Challenger":
                FlexRankTier = "자유랭크 : 첼린저"
            if FlexRankTier == "Flex 5:5 Rank : Grandmaster":
                FlexRankTier = "자유랭크 : 그랜드마스터"
            if FlexRankTier == "Flex 5:5 Rank : Master":
                FlexRankTier = "자유랭크 : 마스터"
            if FlexRankTier == "Flex 5:5 Rank : Diamond 1":
                FlexRankTier = "자유랭크 : 다이아 1"
            if FlexRankTier == "Flex 5:5 Rank : Diamond 2":
                FlexRankTier = "자유랭크 : 다이아 2"
            if FlexRankTier == "Flex 5:5 Rank : Diamond 3":
                FlexRankTier = "자유랭크 : 다이아 3"
            if FlexRankTier == "Flex 5:5 Rank : Diamond 4":
                FlexRankTier = "자유랭크 : 다이아 4"
            if FlexRankTier == "Flex 5:5 Rank : Platinum 1":
                FlexRankTier = "자유랭크 : 플래티넘 1"
            if FlexRankTier == "Flex 5:5 Rank : Platinum 2":
                FlexRankTier = "자유랭크 : 플래티넘 2"
            if FlexRankTier == "Flex 5:5 Rank : Platinum 3":
                FlexRankTier = "자유랭크 : 플래티넘 3"
            if FlexRankTier == "Flex 5:5 Rank : Platinum 4":
                FlexRankTier = "자유랭크 : 플래티넘 4"
            if FlexRankTier == "Flex 5:5 Rank : Gold 1":
                FlexRankTier = "자유랭크 : 골드 1"
            if FlexRankTier == "Flex 5:5 Rank : Gold 2":
                FlexRankTier = "자유랭크 : 골드 2"
            if FlexRankTier == "Flex 5:5 Rank : Gold 3":
                FlexRankTier = "자유랭크 : 골드 3"
            if FlexRankTier == "Flex 5:5 Rank : Gold 4":
                FlexRankTier = "자유랭크 : 골드 4"
            if FlexRankTier == "Flex 5:5 Rank : Silver 1":
                FlexRankTier = "자유랭크 : 실버 1"
            if FlexRankTier == "Flex 5:5 Rank : Silver 2":
                FlexRankTier = "자유랭크 : 실버 2"
            if FlexRankTier == "Flex 5:5 Rank : Silver 3":
                FlexRankTier = "자유랭크 : 실버 3"
            if FlexRankTier == "Flex 5:5 Rank : Silver 4":
                FlexRankTier = "자유랭크 : 실버 4"
            if FlexRankTier == "Flex 5:5 Rank : Bronze 1":
                FlexRankTier = "자유랭크 : 브론즈 1"
            if FlexRankTier == "Flex 5:5 Rank : Bronze 2":
                FlexRankTier = "자유랭크 : 브론즈 2"
            if FlexRankTier == "Flex 5:5 Rank : Bronze 3":
                FlexRankTier = "자유랭크 : 브론즈 3"
            if FlexRankTier == "Flex 5:5 Rank : Bronze 4":
                FlexRankTier = "자유랭크 : 브론즈 4"
            if FlexRankTier == "Flex 5:5 Rank : Iron 1":
                FlexRankTier = "자유랭크 : 아이언 1"
            if FlexRankTier == "Flex 5:5 Rank : Iron 2":
                FlexRankTier = "자유랭크 : 아이언 2"
            if FlexRankTier == "Flex 5:5 Rank : Iron 3":
                FlexRankTier = "자유랭크 : 아이언 3"
            if FlexRankTier == "Flex 5:5 Rank : Iron 4":
                FlexRankTier = "자유랭크 : 아이언 4"
            embed = discord.Embed(title="소환사 전적검색", description="", color=0x5CD1E5)
            embed.add_field(name=SoloRankTier, value=SoloRankPointAndWinRatio, inline=False)
            embed.add_field(name=FlexRankTier, value=FlexRankPointAndWinRatio, inline=False)
            embed.add_field(name="모스트 챔피언 : " + mostUsedChampion,
                            value="KDA : " + mostUsedChampionKDA + " / " + " 승률 : " + mostUsedChampionWinRate,
                            inline=False)
            if cmpTier == 0:
                embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
            elif cmpTier == 1:
                embed.set_thumbnail(url='https:' + RankMedal[1]['src'])
            else:
                if solorankmedal[1] > flexrankmedal[1]:
                    embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                elif solorankmedal[1] < flexrankmedal[1]:
                    embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                else:
                    embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
            await ctx.send(playerNickname + "님의 전적", embed=embed)

    @lolstats.error
    async def lolstats_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            embed = discord.Embed(title="롤 전적", description="닉네임을 입력해주세요", color=0xe74c3c)
            await ctx.send(embed=embed)
        elif AttributeError(error):
            embed = discord.Embed(title="존재하지 않는 소환사", description="", color=0x5CD1E5)
            embed.add_field(name="해당 닉네임의 소환사가 존재하지 않습니다.", value="소환사 이름을 확인해주세요", inline=False)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="롤 전적", description="닉네임을 입력해주세요", color=0xe74c3c)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(lol_stats(bot))
    LOGGER.info("lol-stat loaded!")