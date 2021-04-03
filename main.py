import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import commands
import threading

client = commands.Bot(command_prefix='/')

@client.event
async def on_ready():
    print("ready")


@client.command()
async def views(ctx, link, amount_of_views):

    with requests.Session() as s:
        s.get("https://www.ebay.com/itm/2021-Hot-Wheels-RLC-Candy-Striper-Volkswagen-Drag-Bus-PINK-LOGO-4280-Low-Number/114749158274")
        session_cookies = s.cookies.get_dict()
        print(session_cookies)

    ebay_cookie = session_cookies['ebay']
    nonsession_cookie = session_cookies['nonsession']
    s_cookie = session_cookies['s']

    headers = {
        'authority': 'www.ebay.com',
        'sec-ch-ua': '^\\^Google',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.ebay.com/itm/114749158274',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': '__gads=ID=0105c692f3081c23-22605d4b85b90026:T=1617398669:S=ALNI_MZIcYDV5hGuVaM6J4291IrSamg7Aw; __uzma=7d13e260-efde-42d5-83e6-73dde7aae509; __uzmb=1617398670; __uzmc=248111033163; __uzmd=1617398670; __uzme=; npii=btguid/94791bcf1780a4b4d31b7408ffec57f56429f28f^^cguid/94791e711780ab8ea0f0ba28fee40f986429f28f^^; bm_sv=45382FF67770688A1EFE7FC946CFDC62~Xdj6KTdRUwTzV8qI6vqU1ydoPR+eyFo2R2abr3TdfyCBnMlUUqIhV4L0ZMEzOoA00p01kQjybIcsIhAi5uv2MghjsxLWqShTnWIKOAQ4GDO8ON9uRCH2euJytmun0MIPkl4ywgU/xo3Y+Q3JNl4yfA==; ns1=BAQAAAXhhh+CxAAaAANgASmJIvxBjNjl8NjAxXjE2MTczOTg2NzAyMzdeXjFeM3wyfDV8NHw3fDExXl5eNF4zXjEyXjEyXjJeMV4xXjBeMV4wXjFeNjQ0MjQ1OTA3NVhitlOTHgo1BMHZ+KhWXKJh4oNa; dp1=bu1p/QEBfX0BAX19AQA**6429f290^^bl/US6429f290^^pbf/^%^23e000e000000000000000006248bf10^^; s='+ s_cookie +'; nonsession='+ nonsession_cookie +'; ebay='+ ebay_cookie +'',
    }

    params = (
        ('hash', 'item1ab7953382:g:3-IAAOSwmcpgZbAz'),
    )

    count = 0
    response = requests.get(link, headers=headers, params=params)



client.run("ODI3OTE1NzgzMDEwMjU0ODg4.YGh-qA.gUBmyAJGyb8u2X5taS6UCCTnN-k")
