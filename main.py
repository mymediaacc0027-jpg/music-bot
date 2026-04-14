from pyrogram import Client, filters
import yt_dlp

API_ID = 32854686
API_HASH = "43575e3f5e3a443256f44fca714ac194"
BOT_TOKEN = "8419311415:AAEcq96mgsGvbXLQt2Bc2fQGtdO6VjmIV6k"

app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


def download_audio(query):
    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": "%(title)s.%(ext)s",
"format": "bestaudio/best",
"postprocessors": [{
    "key": "FFmpegExtractAudio",
    "preferredcodec": "mp3",
    "preferredquality": "192",
}],
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch:{query}"])


@app.on_message(filters.text & filters.private)
@app.on_message(filters.text & filters.group)
def music(client, message):
    if message.text.startswith("يوت"):
        query = message.text.replace("يوت", "").strip()
        msg = message.reply("⏳ ثانيه أشوفلك...")

        download_audio(query)

        msg.edit("🎧 ثانيه و تبقى معاك...")

        import os
import os

files = [f for f in os.listdir() if f.endswith(".mp3")]

if not files:
    message.reply("❌ ما قدرت ألقى الملف، حاول مرة تانية")
    return

file = max(files, key=os.path.getctime)
message.reply_audio(file, caption=query)


app.run()
