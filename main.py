import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import commands
import threading
import time

client = commands.Bot(command_prefix='.')

main_class = ""
listings = []
next_listings = []
new_listings = []
ebay_username = ""
ebay_accounts = []
ebay_listing = ""
listing_image = ""
sent_webhooks = []
webhook = False

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
    global ebay_listing
    global listing_image
    global webhook

    print("starting")

    new_listing_embed = discord.Embed(
        title=("New Listing Found!"),
        url = ebay_listing
    )
    new_listing_embed.add_field(name="Adding Views!", value="------------------")
    new_listing_embed.set_image(url=listing_image)

    def initial_request():
        global sent_webhooks
        global webhook
        r = requests.get("https://www.ebay.com/sch/kicksexotic/m.html?_nkw=&_armrs=1&_ipg=&_from=")
        print("sent request")
        soup = BeautifulSoup(r.content, "html.parser")
        main_class = soup.find_all(class_="lvtitle")
        for listing in main_class:
            listings.append(listing)
        for item in listings:
            if "New Listing".lower() in str(item).lower():
                new_listings.append(item)
                print(str(new_listings) + "[NEW LISTINGS]")
                sent_webhooks.append(new_listings[-1])
                for previous_listing in sent_webhooks:
                    print(str(previous_listing))
                    if str(previous_listing).lower() == str(new_listings[0]).lower():
                        print("listings are the same")
                        break
                    else:
                        print("listings are different")
                        find_url()
                        print("found url")
                        find_image()
                        print("found image")
                        new_listings.pop(-1)
                        print(new_listings)
                        print("starting threads")
                        start_threads()
                        webhook = True
            else:
                print("No new listings")


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

    threads = []

    def viewer():
        count = 0
        while count < 5:
            response = requests.get(ebay_listing)
            count += 1

    def start_threads():
        for _ in range(2):
            t = threading.Thread(target=viewer)
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()

    while True:
        initial_request()
        if webhook:
            print("webhook")
            await ctx.send(embed=new_listing_embed)
            time.sleep(5)
            webhook = False
        time.sleep(20)



client.run("ODI3OTE1NzgzMDEwMjU0ODg4.YGh-qA.gUBmyAJGyb8u2X5taS6UCCTnN-k")
