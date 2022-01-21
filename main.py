import os
import discord
import image_scraper

from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix = "!", activity = discord.Activity(type = discord.ActivityType.watching, name = 'the chat'))
slash = SlashCommand(bot, sync_commands = True)

@slash.slash(
	name = "imageURL",
	description = "Takes a URL",
	options = [
		create_option(
			name = "address",
			description = "Takes a URL",
			required = True,
			option_type = 3,
		)
	]
)

async def imageURL(ctx:SlashCommand, address):
	htmldata = image_scraper.getdata(address)
	page = image_scraper.BeautifulSoup(htmldata, 'html.parser')
	
	imageCount = 0

	for item in page.find_all('img'):
		imageCount += 1
	
	if (imageCount > 10):
		await ctx.send("The bot can only send up to 10 images.")

	elif (imageCount == 0):
		await ctx.send("There are no images in this website.")

	else:
		for item in page.find_all('img'):
			await ctx.send(item['src'])

@bot.event
async def on_ready():
	print("Ready!")	

bot.run(TOKEN)