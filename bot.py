import os
import discord
from dotenv import load_dotenv
import webscraper
import helper
import random
import url_handler

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)

    print(
        f'{client.user} is connected to the following guild:\n '
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n -'.join([member.name for member in guild.members])
    print(f'Guild Members:\n- {members}')


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}, Welcome to my Headspace!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content[0:6].lower() == ".ebay ":
        complete_message = helper.parse_count(message.content)
        payload = helper.parse_string(complete_message.message)
        item_list = webscraper.produce_ebay_prices(payload)

        if str(item_list[0].time) == "0":
            toggle_time = False
        else:
            toggle_time = True

        if complete_message.num > 0:
            for index in range(complete_message.num):
                embed_content = discord.Embed(title=item_list[index].title, colour=random.randint(1, 16777200),
                                              url=url_handler.make_tiny(item_list[index].link))
                embed_content.set_image(url=item_list[index].image)
                embed_content.add_field(name="Price:", value=item_list[index].price)

                if toggle_time:
                    embed_content.add_field(name="Date Listed:", value=item_list[index].time)

                await message.channel.send(embed=embed_content)
        else:
            embed_content = discord.Embed(title=item_list[0].title, colour=random.randint(1, 16777200),
                                          url=url_handler.make_tiny(item_list[0].link))
            embed_content.set_image(url=item_list[0].image)
            embed_content.add_field(name="Price:", value=item_list[0].price)

            if toggle_time:
                embed_content.add_field(name="Date Listed:", value=item_list[0].time)

            await message.channel.send(embed=embed_content)


client.run(TOKEN)
