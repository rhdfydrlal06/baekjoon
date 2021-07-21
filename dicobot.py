import aiohttp
import discord
import json
from bs4 import BeautifulSoup
from discord.ext import commands

bot = commands.Bot(command_prefix='$')
discord_key = 'discord_key'
kakao_key = 'kakao_key'
server_URL = 'http://localhost:1234'

'''
이 부분은 절대 건드리시면 안 됩니다!
코루틴과 aiohttp에 대한 지식이 없는 상황에서 봇 제작을 해야 하므로,
여러분들이 사용할 수 있는 request와 최대한 흡사하게 수정하는 코드입니다...
'''
class requests_result():
    def __init__(self, st_code, contents):
        self.status_code = st_code
        self.text = contents
    
    def ok(self):
        return self.status_code == 200

class requests():
    @staticmethod
    async def get(url, headers=None, params=None, **kwargs):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                content = await response.read()
                return requests_result(response.status, content)

    @staticmethod
    async def post(url, data=None, headers=None, json=None, **kwargs):
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data, json=json) as response:
                content = await response.read()
                return requests_result(response.status, content)

    @staticmethod
    async def delete(url, data=None, headers=None, json=None, **kwargs):
        async with aiohttp.ClientSession() as session:
            async with session.delete(url, headers=headers, data=data, json=json) as response:
                content = await response.read()
                return requests_result(response.status, content)

    @staticmethod
    async def put(url, data=None, headers=None, json=None, **kwargs):
        async with aiohttp.ClientSession() as session:
            async with session.put(url, headers=headers, data=data, json=json) as response:
                content = await response.read()
                return requests_result(response.status, content)
'''
이 부분은 절대 건드리시면 안 됩니다!
코루틴과 aiohttp에 대한 지식이 없는 상황에서 봇 제작을 해야 하므로,
여러분들이 사용할 수 있는 request와 최대한 흡사하게 수정하는 코드입니다...
'''
@bot.command(name="코로나")
#BeautifulSoup을 이용하여 Crawling
async def corona(ctx, *args):
    URL = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EC%BD%94%EB%A1%9C%EB%82%98'
    #**브라우저 임을 표시하면 크롤링 안막힘**
    header = {
        'USer-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
    }
    response = await requests.get(URL)  #URL 요청
    html = response.text.decode('utf-8')    #웹 페이지 코드를 text 형태로 가져옴
    soup = BeautifulSoup(html, 'html.parser')   #찐 html 코드로 변형
    #####info_title = 감염현황 내에 있는 제목들
    #####info_num = 해당 title 내에 숫자
    titles = soup.find_all(class_="info_title", limit=4)
    numbers = soup.find_all(class_="info_num", limit=4)
    variations = soup.find_all(class_="info_variation", limit=4)

    for title, number, variation in zip(titles, numbers, variations):
        await ctx.send(f'{title.text}: {number.text} (▲{variation.text})')


@bot.command(name="검색")
#카카오 API 이용하여 Daum 검색 작업
async def search(ctx, *args):
    URL = 'https://dapi.kakao.com/v2/search/web'
    parameter = {
        'query' : ' '.join(args),
        'sort' : 'accuracy',
        'size' : 3
    }

    header = {
        'Authorization' : f'KakaoAK {kakao_key}'
    }

    response = await requests.get(URL, params=parameter, headers=header)

    if response.status_code != 200:
        print(response.text)
        await ctx.send("삐용삐용 검색 중 문제 발생 삐용삐용")
        return
    
    tmp = json.loads(response.text)
    
    for dt in tmp['documents']:
        await ctx.send(dt['title'] + ' ' + dt['contents'])


@bot.command(name="안녕!!")
async def hello(ctx):
    await ctx.send("방가워! \(@^0^@)/")
@bot.command()
async def bye(ctx):
    await ctx.send("작별인사 하지마!!! (ノ｀Д)ノ")

@bot.command(name="게시판조회")
async def board_search(ctx, *args):
    request_URL = server_URL + "/board"
    response = await requests.get(request_URL)

    if response.status_code != 200:
        print(response.text)
        await ctx.send("삐용삐용 검색 중 문제 발생 삐용삐용")
        return
    
    await ctx.send(json.loads(response.text))

@bot.command(name="게시판작성")
async def board_write(ctx, arg, *args): #비밀번호(arg), 게시글(args)
    if not args:
        await ctx.send("삐용삐용 입력이 잘못되었습니다 삐용삐용")
        return

    if len(arg) > 20:
        await ctx.send("비밀번호의 길이는 20글자를 넘을 수 없습니다.")
        return

    data = {
        'password': arg,
        'content' : ' '.join(args)
    }
    request_URL = server_URL + "/board"
    response = await requests.post(request_URL, json=data)
    if response.status_code != 200:
        print(response.text)
        await ctx.send("삐용삐용 삽입 중 문제 발생 삐용삐용")
        return

    await ctx.send(json.loads(response.text))
@bot.event
async def on_ready():
    print(f'{bot.user} 봇이 가동되었습니다!!')

bot.run(discord_key)