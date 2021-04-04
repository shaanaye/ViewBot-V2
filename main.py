import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import commands
import threading

client = commands.Bot(command_prefix='/')

main_class = ""
listings = []
next_listings = []
new_listings = []
ebay_username = ""
ebay_accounts = []
ebay_listing = ""
listing_image = ""

@client.event
async def on_ready():
    print("ready")

@client.command()
async def setup(ctx):
    global ebay_username
    global ebay_accounts

    first_embed = discord.Embed(title="ViewBot V2", color=0x00ffee)
    first_embed.add_field(name="Enter an eBay account to monitor", value="---------", inline=True)
    first_embed.set_footer(text="Created by shaan")
    await ctx.send(embed=first_embed)

    def wrapper(context):
        def check_msg(message):
            return context.author == message.author and context.channel == message.channel

        return check_msg

    ebay_username = await client.wait_for("message", check=wrapper(ctx))

    second_embed = discord.Embed(title="ViewBot V2", color=0x00ffee)
    second_embed.add_field(name=f"Now Monitoring {ebay_username.content}'s Account", value="---------", inline=True)
    second_embed.set_footer(text="Created by shaan")
    await ctx.send(embed=second_embed)

    ebay_accounts.append(ebay_username.content)

@client.command()
async def start(ctx):

    def initial_request():
        r = requests.get("https://www.ebay.com/sch/kicksexotic/m.html?_nkw=&_armrs=1&_ipg=&_from=")
        soup = BeautifulSoup(r.content, "html.parser")
        main_class = soup.find_all(class_="lvtitle")
        for listing in main_class:
            listings.append(listing)
        # print(main_class)
        for item in listings:
            if "New Listing".lower() in str(item).lower():
                new_listings.append(item)
                find_url()
                find_image()
                await ctx.send(new_listing_embed)

    def find_image():
        global listing_image
        r = requests.get(ebay_listing)
        soup = BeautifulSoup(r.content, 'html.parser')
        img_class = str(soup.find(id="icImg"))
        image_parse = img_class.split('src="')
        image_parse2 = image_parse[1].split('"')
        listing_image = image_parse2[0]

    def find_url():
        global ebay_listing
        parse = str(new_listings[-1])
        parse1 = parse.split('href="')
        parse2 = parse1[1].split('"')
        ebay_listing = str(parse2[0])


    new_listing_embed = discord.Embed(
        title=("New Listing Found!"),
        url = ebay_listing
    )
    new_listing_embed.add_field(name="Listing:", value="fewafgewa") #come bakc
    new_listing_embed.set_image(url=listing_image)





    threads = []

    def viewer():
        count = 0
        while count < 200:
            response = requests.get(ebay_listing)
            count += 1

    def start_threads():
        for _ in range(50):
            t = threading.Thread(target=viewer)
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()

    while True:
        initial_request()




client.run("ODI3OTE1NzgzMDEwMjU0ODg4.YGh-qA.gUBmyAJGyb8u2X5taS6UCCTnN-k")
