from telebot import TeleBot
from telebot.types import Message

from shazam import recognize

bot = TeleBot("TOKEN", parse_mode='HTML')


@bot.message_handler(commands=['start'])
def reaction_to_start(message: Message):
    chat_id = message.chat.id
    full_name = message.from_user.full_name
    bot.send_message(chat_id,
                     f"<b>Assalomu alaykum {full_name}!</b>\n\n<i>"
                     f"Men sizga musiqalarni topishga yordam berishim mumkin. Menga ovozli xabar,"
                     f" yumaloq video, musiqa yoki video yuboring. Men sizga musiqasini topib beraman 😊️</i>")


@bot.message_handler(content_types=['voice', 'audio', 'video_note', 'video'])
def reaction_to_media(message: Message):
    chat_id = message.chat.id

    loading_msg = bot.send_message(chat_id, "🔎 <i>Qidirilmoqda...</i>")

    result = recognize(bot, message)
    bot.delete_message(chat_id, loading_msg.message_id)

    if not result or "track" not in result:
        bot.send_message(chat_id, "😔 <b>Afsuski musiqa topilmadi.</b>")

    track = result["track"]
    title = track.get("title", "Noma'lum")
    artist = track.get("subtitle", "Noma'lum")

    text = (f"✅ <b>Musiqa topildi.</b>\n\n"
            f"• <b>Nomi:</b> {title}\n"
            f"• <b>Qo'shiqchi:</b> {artist}")

    bot.send_message(chat_id, text)


if __name__ == '__main__':
    print("✅ Bot ishga tushurildi.")
    bot.infinity_polling()
