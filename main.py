import lightbulb
import os

from dotenv import load_dotenv

load_dotenv()

bot = lightbulb.BotApp(token = os.getenv('DISCORD_TOKEN'))

test_guild_ids = [int(server_id) for server_id in os.getenv('TEST_SERVER_IDS').split(",")]

total_media_size_limit = 100

@bot.command
@lightbulb.option("url", "URL to scrape images from")
@lightbulb.command("scrape-images", "Scrapes all images from any given website", guilds = test_guild_ids, ephemeral = True, auto_defer = True)
@lightbulb.implements(lightbulb.SlashCommand)
async def scrapeImages(ctx):
	
	if guild := ctx.get_guild():
		server_boosts = guild.premium_subscription_count
	else:
		server_boosts = 0

	await ctx.respond("Pong!")

bot.run()

def get_file_size_limit_by_boosts(boost_count):
	if 0 <= boost_count < 7:
		size_limit = 8
	elif 7 <= boost_count < 14:
		size_limit = 50
	elif 14 <= boost_count:
		size_limit = 100

	return size_limit