import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import commands
from dhooks import Webhook, Embed
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
count = 0
listing_name = ""
price = ""



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

    user = await client.wait_for("message", check=wrapper(ctx))
    ebay_username = user.content
    second_embed = discord.Embed(title="ViewBot V2", color=0x00ffee)
    second_embed.add_field(name=f"Now Monitoring {user.content}'s Account", value="---------", inline=True)
    second_embed.set_footer(text="Created by shaan")
    await ctx.send(embed=second_embed)

    ebay_accounts.append(user.content)


@client.command()
async def start(ctx):
    global ebay_listing
    global listing_image
    global sent_webhooks
    global count
    global listing_name
    global price
    global ebay_username
    print("starting")

    def initial_request():
        global sent_webhooks
        global webhook
        global listings
        global listing_image
        global ebay_listing
        global new_listings
        global ebay_username
        r = requests.get("https://www.ebay.com/sch/"+str(ebay_username)+"/m.html?_nkw=&_armrs=1&_ipg=&_from=")
        print("sent request")
        soup = BeautifulSoup(r.content, "html.parser")
        main_class = soup.find_all(class_="lvtitle")
        for listing in main_class:
            listings.append(listing)
        main_class.clear()
        print(str(listings) + "ALL LISTINGS")
        for item in listings:
            if "New Listing".lower() in str(item).lower():
                new_listings.append(item)
            else:
                pass
        listings.clear()
        print(new_listings)

        for new_listing in new_listings:
            if new_listing in sent_webhooks:
                print("Listings Has Already Been Sent")
            else:
                parse = str(new_listing)
                parse1 = parse.split('href="')
                parse2 = parse1[1].split('"')
                ebay_listing = str(parse2[0])
                start_threads()
                sent_webhooks.append(new_listing)
                print("Added views to " + ebay_listing)
                print(new_listings)
                time.sleep(4)
                webhook = True
        new_listings.clear()
        print(str(new_listings) + "[NEW LISTINGS]")
        print(str(sent_webhooks) + "[SENT WEBHOOKS]")


    def find_image():
        global listing_image
        r = requests.get(ebay_listing)
        soup = BeautifulSoup(r.content, 'html.parser')
        img_class = str(soup.find(id="icImg"))
        image_parse = img_class.split('src="')
        image_parse2 = image_parse[1].split('"')
        listing_image = image_parse2[0]

    def find_url(sent_listing):
        global ebay_listing
        parse = str(sent_listing)
        parse1 = parse.split('href="')
        parse2 = parse1[1].split('"')
        ebay_listing = str(parse2[0])

    def listing_information():
        global ebay_listing
        global listing_name
        global price
        r = requests.get(ebay_listing)
        soup = BeautifulSoup(r.content, "html.parser")
        listing_name1 = soup.find(id="itemTitle")
        listing_name2 = str(listing_name1).split("</span>")
        listing_name3 = str(listing_name2[1]).split("</h1>")
        listing_name = listing_name3[0]
        price1 = soup.find(id="prcIsum")
        price2 = str(price1).split('content="')
        price3 = str(price2[1]).split('" id')
        price = str(price3[0])


    threads = []

    def viewer():
        count = 0
        while count < 300:
            response = requests.get(ebay_listing)
            count += 1

    def start_threads():
        for _ in range(20):
            t = threading.Thread(target=viewer)
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()


    while True:
        initial_sent_webhook_length = len(sent_webhooks)
        initial_request()
        if count == 0:
            for sent_listing in sent_webhooks:
                find_url(sent_listing)
                find_image()
                listing_information()
                new_listing_embed = Embed(
                    description=f'[**New Listing Found!**]({ebay_listing})',
                    color=0x00FF00,
                )
                new_listing_embed.add_field(name="Added Views to:", value=f"{listing_name}", inline=False)
                new_listing_embed.add_field(name="User:", value=f'{ebay_username}', inline=True)
                new_listing_embed.add_field(name="Price:", value=f'{price}', inline=True)
                new_listing_embed.set_image(url=listing_image)
                new_listing_embed.set_footer(text="Created by shaan")
                await ctx.send(embed=new_listing_embed)
            count += 1
        else:
            prior_sent_webhook_length = len(sent_webhooks)
            if prior_sent_webhook_length > initial_sent_webhook_length:
                find_url(sent_webhooks[-1])
                find_image()
                listing_information()
                new_listing_embed = Embed(
                    description=f'[**New Listing Found!**]({ebay_listing})',
                    color=0x00FF00
                )
                new_listing_embed.add_field(name="Added Views to:", value=f"{listing_name}", inline=False)
                new_listing_embed.add_field(name="User:", value=f'{ebay_username}', inline=True)
                new_listing_embed.add_field(name="Price:", value=f'{price}', inline=True)
                new_listing_embed.set_image(url=listing_image)
                new_listing_embed.set_footer(text="Created by shaan")
                await ctx.send(embed=new_listing_embed)
            else:
                pass

        time.sleep(60)

client.run("ODI3OTE1NzgzMDEwMjU0ODg4.YGh-qA.gUBmyAJGyb8u2X5taS6UCCTnN-k")
