from pyrogram import Client, filters
import requests

API_ID = 32854686
API_HASH = "43575e3f5e3a443256f44fca714ac194"
BOT_TOKEN = "8419311415:AAEcq96mgsGvbXLQt2Bc2fQGtdO6VjmIV6k"

app = Client(
    "music_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


# 🎧 API جاهز (بديل يوتيوب)
def get_song(query):
    url = f"https://api.vevioz.com/api/button/mp3/{query}"
    return url


@app.on_message(filters.text & (filters.group | filters.private))
def music(client, message):
    if message.text.startswith("يوت"):
        query = message.text.replace("يوت", "").strip()

        if not query:
            return message.reply("❌ اكتب اسم الأغنية")

        msg = message.reply("🔎 عم دور...")

        try:
            audio_url = get_song(query)

            msg.edit("🎧 عم برسل الأغنية...")

            message.reply_audio(
                audio=audio_url,
                title=query,
                performer="Music Bot"
            )

        except Exception as e:
            msg.edit(f"❌ خطأ:\n{e}")


app.run()
