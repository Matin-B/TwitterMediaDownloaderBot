import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode
from aiogram.utils.emoji import emojize

import config
from downlaoder import download_tweet

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler()
async def send_download_link(message: types.Message):
    """
    This handler will be called when user sends any text message
    """
    message_text = message.text
    download_response = download_tweet(message_text)
    if download_response == "Not Found":
        await message.reply("Tweet Not Found")
    else:
        tweet_text = download_response['text']
        tweet_author_username = download_response['tweet_author_username']
        tweet_author_name = download_response['tweet_author_name']
        tweet_date = download_response['tweet_date']
        link = download_response['link']
        media_status = download_response['media']

        if media_status is True:
            pass
        else:
            await message.reply(
                # https://www.webfx.com/tools/emoji-cheat-sheet/#
                emojize(f'{tweet_text}\n\n:link: [{tweet_author_name} '\
                        f'(@{tweet_author_username})](https://twitter.com/{tweet_author_username})'\
                        '\n\n:robot: @TwitterMediaDownloaderBot'),
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True
            )

"""
    if len(download_response) != 1:
        # Create media group
        media = types.MediaGroup()

        for item in download_response:
            media.attach_photo(item['url'])
        await message.reply_media_group(
            media=media
        )
    else:
        for item in download_response:
            if item['type'] == 'video':
                await message.reply("This is a video")
            elif item['type'] == 'photo':
                await message.reply_photo(item['url'])
            elif item['type'] == 'animated_gif':
                await message.reply_animation(item['url'])
"""

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
