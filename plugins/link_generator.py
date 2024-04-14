import requests
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import ADMINS
from helper_func import encode, get_message_id

ADCORTO_API_KEY = "16d71a6393ca4b6b85d9acb343a80ca9a5bc12f3"  # Replace with your ADCorto API key

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('batch'))
async def batch(client: Client, message: Message):
    while True:
        try:
            first_message = await client.ask(text="Forward the First Message from DB Channel (with Quotes)..\n\nor Send the DB Channel Post Link", chat_id=message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        f_msg_id = await get_message_id(client, first_message)
        if f_msg_id:
            break
        else:
            await first_message.reply("❌ Error\n\nthis Forwarded Post is not from my DB Channel or this Link is taken from DB Channel", quote=True)
            continue

    while True:
        try:
            second_message = await client.ask(text="Forward the Last Message from DB Channel (with Quotes)..\nor Send the DB Channel Post link", chat_id=message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        s_msg_id = await get_message_id(client, second_message)
        if s_msg_id:
            break
        else:
            await second_message.reply("❌ Error\n\nthis Forwarded Post is not from my DB Channel or this Link is taken from DB Channel", quote=True)
            continue

    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)

    long_link = f"https://t.me/{client.username}?start={base64_string}"

    adcorto_api_url = "https://adcorto.com/api"
    payload = {
        "api": ADCORTO_API_KEY,
        "url": long_link,
        "alias": "CustomAlias"
    }
    response = requests.get(adcorto_api_url, params=payload)
    if response.status_code == 200:
        json_response = response.json()
        if json_response.get("status") == "success":
            short_link = json_response.get("shortenedUrl")
        else:
            short_link = "Error occurred while shortening the link"
    else:
        short_link = "Error occurred while connecting to ADCorto API"

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={short_link}')]])
    await second_message.reply_text(f"<b>Here is your link</b>\n\n{short_link}", quote=True, reply_markup=reply_markup)
