import lightbulb
import os
import image_scraper

from dotenv import load_dotenv
from utils import get_filesize_mb

load_dotenv()

bot = lightbulb.BotApp(token = os.getenv('DISCORD_TOKEN'))

total_message_size_limit = 100
file_count_limit = 10	

@bot.command
@lightbulb.option("url", "URL to scrape images from")
@lightbulb.command("scrape-images", "Scrapes all images from any given website", ephemeral = True, auto_defer = True)
@lightbulb.implements(lightbulb.SlashCommand)
async def scrapeImages(ctx):
	
	if guild := ctx.get_guild():
		server_boosts = guild.premium_subscription_count
	else:
		server_boosts = 0

	if not (target := ctx.get_channel()):
		target = ctx.author

	file_size_limit = get_file_size_limit_by_boosts(server_boosts)

	file_count = 0
	total_file_count = 0
	total_message_size = 0
	total_size = 0

	too_large_files = []

	aggregated_files_to_send = []

	for image_path in image_scraper.download_images(ctx.options.url, total_size_limit = int(os.getenv('DISK_LIMIT_MB'))):
		if (file_size := get_filesize_mb(image_path)) > file_size_limit:
			too_large_files.append(file_size)
			continue

		if (total_message_size + file_size > total_message_size_limit) or (file_count + 1 > file_count_limit):
			await send_images(target, aggregated_files_to_send)
			aggregated_files_to_send = []
			file_count = 0
			total_message_size = 0

		aggregated_files_to_send.append(image_path)
		file_count += 1
		total_file_count += 1
		total_message_size += file_size
		total_size += file_size

	await send_images(target, aggregated_files_to_send)

	await target.send(f"Scraped **{total_file_count + len(too_large_files)}** files with total size of **{(total_size + sum(too_large_files)):.2f} MB**. **{len(too_large_files)}** of which were too large to send.")

	await ctx.respond("Done!")

async def send_images(target, image_paths):
	await target.send(attachments = image_paths)

def get_file_size_limit_by_boosts(boost_count):
	if 0 <= boost_count < 7:
		size_limit = 8
	elif 7 <= boost_count < 14:
		size_limit = 50
	elif 14 <= boost_count:
		size_limit = 100

	return size_limit


bot.run()
