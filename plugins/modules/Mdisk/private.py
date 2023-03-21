from pyrogram import Client, filters
from config import ADMINS, SOURCE_CODE
from pyrogram.types import Message

from util import main_convertor_handler


import json
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters
from util import replace_mdisk_link, caption
from config import ADMINS, SOURCE_CODE
from pyrogram.types import Message
import re
from info import BATCH_GROUP

# Private Chat

@Client.on_message(filters.command("m") & filters.chat(BATCH_GROUP) & (
        filters.channel | filters.group) & filters.incoming & filters.forwarded)


#@Client.on_message(filters.command("m") & filters.text & filters.photo & filters.chat(BATCH_GROUP))
#async def private_link_handler(c, message):
#    if message.from_user.id not in ADMINS:
#        return await message.reply_text(f"This bot works only for ADMINS of this bot. Make your own Bot.\n\n[Source Code]({SOURCE_CODE})")
        
    try:
        txt = await message.reply('`Cooking... It will take some time if you have enabled Link Bypass`', quote=True)
        await main_convertor_handler(message, 'mdisk')

        # Updating DB stats
    except Exception as e:
        await message.reply("Error while trying to convert links %s:" % e, quote=True)
    finally:
        await txt.delete()






        if message.text:
            txt = message.text

        elif message.caption:
            txt = message.caption

    # url shortener in private chat

        if message.reply_markup:  # reply markup - button post

            reply_markup = json.loads(str(message.reply_markup))
            buttsons = []
            for i, markup in enumerate(reply_markup["inline_keyboard"]):
                buttons = []
                for j in markup:
                    text = j["text"]
                    url = j["url"]
                    url = await replace_mdisk_link(url)
                    button = InlineKeyboardButton(text, url=url)
                    buttons.append(button)
                buttsons.append(buttons)

            txt = await replace_mdisk_link(txt)

            if message.text:
                await message.reply(text=txt,
                                    reply_markup=InlineKeyboardMarkup(buttsons),
                              )
            elif message.photo:
                await message.reply_photo(caption=txt,
                                          photo=message.photo.file_id,
                                          reply_markup=InlineKeyboardMarkup(buttsons),
                                         )

            elif message.document:
                await message.reply_document(caption=txt,
                                             document=message.document.file_id,
                                             reply_markup=InlineKeyboardMarkup(buttsons),
                                          )

        elif message.text:  # for text messages
            text = message.text
            link = await replace_mdisk_link(text)
            await message.reply_text(link)

        elif message.photo:  # for media messages
            fileid = message.photo.file_id
            text = message.caption
            link = await replace_mdisk_link(text)
            await message.reply_photo(fileid, caption=link, )

        elif message.document:  # for document messages
            fileid = message.document.file_id
            text = message.caption
            link = await replace_mdisk_link(text)
            await message.reply_document(fileid, caption=link)