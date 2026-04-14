from pyrogram import Client, filters
import yt_dlp
import os

API_ID = 32854686
API_HASH = "43575e3f5e3a443256f44fca714ac194"
BOT_TOKEN = "8419311415:AAEcq96mgsGvbXLQt2Bc2fQGtdO6VjmIV6k"

app = Client(
    "music_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


# 🎧 تحميل الصوت من يوتيوب
def download_audio(query):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "song.%(ext)s",
        "noplaylist": True,
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=True)
        file_path = ydl.prepare_filename(info["entries"][0])

    return file_path


# 🎵 أمر التشغيل
@app.on_message(filters.text & filters.group)
@app.on_message(filters.text & filters.private)
def music(client, message):
    text = message.text.lower()

    if text.startswith("يوت"):
        query = message.text.replace("يوت", "").strip()

        if not query:
            message.reply("❌ اكتب اسم الأغنية بعد يوت")
            return

        msg = message.reply("⏳ عم بحمّل الأغنية...")

        try:
            file = download_audio(query)

            msg.edit("🎧 تم التحميل، عم أرسل الملف...")

            message.reply_audio(file, caption=query)

            os.remove(file)

        except Exception as e:
            msg.edit(f"❌ صار خطأ: {e}")


app.run()
