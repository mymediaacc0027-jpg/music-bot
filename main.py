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


def download_audio(query):
    ydl_opts = {
        "format": "bestaudio[ext=m4a]/bestaudio/best",
        "noplaylist": True,
        "quiet": True,
        "default_search": "ytsearch1",
        "outtmpl": "song.%(ext)s",
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=True)

        if "entries" in info:
            info = info["entries"][0]

        return ydl.prepare_filename(info)


@app.on_message(filters.text & (filters.group | filters.private))
def music(client, message):
    if message.text.startswith("يوت"):
        query = message.text.replace("يوت", "").strip()

        if not query:
            return message.reply("❌ اكتب اسم الأغنية")

        msg = message.reply("⏳ عم بحمّل...")

        try:
            file = download_audio(query)

            msg.edit("🎧 عم برسل كـ مشغل صوت...")

            message.reply_audio(
                audio=file,
                title=query,
                performer="Music Bot"
            )

            if os.path.exists(file):
                os.remove(file)

        except Exception as e:
            msg.edit(f"❌ خطأ:\n{e}")


app.run()
