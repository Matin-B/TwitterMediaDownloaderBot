import logging
import config
from aiogram import Bot, Dispatcher, executor, types
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
    message_text = message.text
    download_response = download_tweet(message_text)
    if download_response == "Media Not Found":
        await message.reply("Media Not Found")
    elif download_response == "Not Found":
        await message.reply("Tweet Not Found")
    else:
        for item in download_response:
            if item['type'] == 'video':
                await message.reply("This is a video")
            elif item['type'] == 'photo':
                await message.reply_photo(item['url'])
            elif item['type'] == 'animated_gif':
                await message.reply_animation(item['url'])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
