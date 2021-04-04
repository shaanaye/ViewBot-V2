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
async def views(ctx, link=""):

    threads = []

    def viewer():
        count = 0
        while count < 200:
            response = requests.get(link)
            count += 1
            print(response)
            print(count)

    for _ in range(50):
        t = threading.Thread(target=viewer)
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()

    await ctx.send("Added Views")




client.run("ODI3OTE1NzgzMDEwMjU0ODg4.YGh-qA.gUBmyAJGyb8u2X5taS6UCCTnN-k")
