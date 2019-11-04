import discord
from discord.ext import commands
import revsearch
# import dubstosubs
from config import DISCORD_TOKEN
from config import DISCORD_WELCOME
import musumecollection
# import re
import functions

bot = commands.Bot(command_prefix='?')

# TODO: Create standard embed template for messages
# TODO: Move functions into seperate python file
# TODO: Add command prefix to config


@bot.event
async def on_ready():
    print("%s is now online" % bot.user.name)
    await bot.change_presence(game=discord.Game(name="^help"))


@bot.event
async def on_member_join(member):
    channel = member.server.get_channel(DISCORD_WELCOME)
    # await bot.send_message(channel, "Hello"
    embed = discord.Embed(title="Welcome!", description="Come on and slam", 
                          color=musumecollection.PADORU_COLOUR)
    embed.set_thumbnail(url=musumecollection.PADORU_ICON)
    embed.set_image(url=musumecollection.PADORU_WELCOME)
    await bot.send_message(channel, embed=embed)


@bot.event
async def on_message(message):
    if message.content.startswith("^help"):
        embed = discord.Embed(title="Commands",
                              description=f"Here are some commands. Umu!",
                              color=musumecollection.PADORU_COLOUR)
        embed.set_thumbnail(url=musumecollection.PADORU_ICON)
        embed.add_field(name="^help", value="Available commands")
        embed.add_field(name="^coinflip", value="Flip a coin")
        embed.add_field(name="^source", value="SauceNao search")
        await bot.send_message(message.channel, embed=embed)
    # SauceNao functionality
    # Usage: start a message with ^source and upload an image
    # (in the same message)
    if message.content.startswith("^source"):
        # TODO: Add bot typing
        await bot.send_typing(message.channel)
        try:
            if message.attachments:
                attachmentDict = message.attachments[0]
                sauce_list = revsearch.get_sauce_nao(attachmentDict["url"])
                if sauce_list["found"]:
                    similarity = sauce_list["similarity"]
                    thumbnail = sauce_list["thumbnail"]
                    embed = discord.Embed(title="Saber Search",
                                          description=f"I'm {similarity}% sure"
                                          " it is this. Umu!",
                                          color=musumecollection.PADORU_COLOUR)
                    embed.set_image(url=thumbnail)
                    embed.set_thumbnail(url=musumecollection.PADORU_ICON)
                    embed.add_field(name="Title", value=sauce_list["title"])
                    embed.add_field(name="Artist", value=sauce_list["name"])
                    embed.add_field(name="ID", value=sauce_list["id"])
                    embed.add_field(name="URL", value=sauce_list["url"])
                    await bot.send_message(message.channel, embed=embed)
                else:
                    embed = discord.Embed(title="Saber Search",
                                          description="Khh-- I can't find it",
                                          color=musumecollection.PADORU_COLOUR)
                    embed.set_thumbnail(url=musumecollection.PADORU_ICON)
                    await bot.send_message(message.channel, embed=embed)
            else:
                embed = discord.Embed(title="Saber Search", description="You"
                                      " didn't even upload anything.",
                                      color=musumecollection.PADORU_COLOUR)
                embed.set_thumbnail(url=musumecollection.PADORU_ICON)
                await bot.send_message(message.channel, embed=embed)
        # At the moment it's doing a catch all for invalid filetypes,
        # Later I need to find a way to find whether they have specicially
        # Uploaded images, currenty content-type via requests does 90% of the
        # Work, however it falsely flags .jpg-large files as applications.
        # TODO: Find a way to identify images
        except Exception as e:
            print(e)
            embed = discord.Embed(title="Saber Search",
                                  description="Guh I don't like that, "
                                  "did you upload an image?",
                                  color=musumecollection.PADORU_COLOUR)
            embed.set_thumbnail(url=musumecollection.PADORU_ICON)
            await bot.send_message(message.channel, embed=embed)
    # Translate
    # Type ^translate <from lang> to <to lang> "<text to translate>"
    # TODO look into getting a bing translate API key
    # if message.content.startswith("^translate"):
        # try:
            # TODO: Clean up regex for translation
            # PATTERN = re.compile(r'''((?:[^ "']|"[^"]*"|'[^']*')+)''')
            # msg = PATTERN.split(message.content)
            # if msg[3] != "to":
            # result = dubstosubs.do_translate(msg[9], msg[7], msg[3])
            # else:
            # result = dubstosubs.do_translate(msg[7], msg[5])
            # await bot.send_message(message.channel, result)
        # TODO: Have the bot handle poorly worded translation requests better
        # except Exception as e:
            # print(e)
    # Coin flip
    if message.content.startswith("^coinflip"):
        await bot.send_typing(message.channel)
        result = functions.coin_flip()
        embed = discord.Embed(title="Coin Flip", description=result,
                              color=musumecollection.PADORU_COLOUR)
        if result == "Heads":
            embed.set_image(url=musumecollection.PADORU_HEADS)
        else:
            embed.set_image(url=musumecollection.PADORU_TAILS)
        embed.set_thumbnail(url=musumecollection.PADORU_ICON)
        await bot.send_message(message.channel, embed=embed)


# TODO: Add Jisho support
# TODO: Add Sticker support
# TODO: Add MAL search
# TODO: Add @everyone response
# TODO: Member cards
# TODO: Add server info
# TODO: Add server ping
# TODO: Lyrics search
# TODO: Add Donate button
# TODO: add waifu insult
# TODO: Add help command


bot.run(DISCORD_TOKEN)
