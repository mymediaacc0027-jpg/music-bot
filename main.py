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


# 🔎 بحث بسيط (بدون yt-dlp)
def search_song(query):
    url = f"https://api.deezer.com/search?q={query}"
    r = requests.get(url).json()

    if "data" in r and len(r["data"]) > 0:
        return r["data"][0]["preview"]  # 30 ثانية mp3
    return None


@app.on_message(filters.text & (filters.group | filters.private))
def music(client, message):
    if not message.text:
        return

    if message.text.startswith("يوت"):
        query = message.text.replace("يوت", "").strip()

        if not query:
            message.reply("❌ اكتب اسم الأغنية بعد يوت")
            return

        msg = message.reply("⏳ عم بدوّر على الأغنية...")

        audio_url = search_song(query)

        if not audio_url:
            msg.edit("❌ ما لقيت الأغنية")
            return

        msg.edit("🎧 عم برسل الأغنية...")

        message.reply_audio(
            audio=audio_url,
            caption=query,
            title=query,
            performer="Music Bot"
        )


app.run()
