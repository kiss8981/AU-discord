import discord
from discord.ext import commands
import json
import urllib.request
from musicbot import LOGGER
from musicbot.utils.language import get_lan

class shortURL(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="단축주소", aliases=["shortlink", "slink", "shorturl"])
    async def shorturl(self, ctx, arg):
        client_id = "UOdkKOt8nS0r96t64l1f"  # 개발자센터에서 발급받은 Client ID 값
        client_secret = "9tOH5iXEza"  # 개발자센터에서 발급받은 Client Secret 값
        encText = urllib.parse.quote(arg)
        data = "url=" + encText
        url = "https://openapi.naver.com/v1/util/shorturl"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            shorturl = json.loads(response_body.decode('utf-8'))
            returnurl = shorturl['result']['url']
            emb = discord.embeds.Embed(title=get_lan(ctx.author.id, 'short_url'))
            emb.add_field(name=get_lan(ctx.author.id, 'short_url_defalt'), value=f"**{arg}**", inline=False)
            emb.add_field(name=get_lan(ctx.author.id, 'short_url_convert'), value=f"**{returnurl}**", inline=False)
            emb.set_thumbnail(url=f"{returnurl}.qr")
            await ctx.send(embed=emb)
        else:
            print("Error Code:" + rescode)
            emb = discord.embeds.Embed(title=get_lan(ctx.author.id, 'short_url'), description=get_lan(ctx.author.id, 'short_url_error').format(rescode=rescode))
            await ctx.send(embed=emb)


def setup(bot: commands.Bot):
    bot.add_cog(shortURL(bot))
    LOGGER.info("shortURL loaded!")