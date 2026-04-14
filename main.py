from pyrogram import Client, filters
import yt_dlp
import os
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


# 🔥 اختيار Invidious instance (بديل يوتيوب مقاوم للحظر)
INVIDIOUS = "https://inv.nadeko.net"


def get_video(query):
    url = f"{INVIDIOUS}/api/v1/search?q={query}"
    r = requests.get(url).json()

    if not r:
        return None

    for item in r:
        if item.get("type") == "video":
            return "https://www.youtube.com/watch?v=" + item["videoId"]

    return None


def download_audio(url):
    ydl_opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "quiet": True,
        "outtmpl": "song.%(ext)s",
        "geo_bypass": True,
        "nocheckcertificate": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        if "entries" in info:
            info = info["entries"][0]

        return ydl.prepare_filename(info)


@app.on_message(filters.text & (filters.group | filters.private))
def music(client, message):
    if not message.text:
        return

    if message.text.startswith("يوت"):
        query = message.text.replace("يوت", "").strip()

        if not query:
            message.reply("❌ اكتب اسم الأغنية بعد يوت")
            return

        msg = message.reply("🔎 عم بدوّر بطريقة احترافية...")

        try:
            video_url = get_video(query)

            if not video_url:
                msg.edit("❌ ما لقيت الأغنية")
                return

            msg.edit("⬇️ عم بحمّل الصوت...")

            file = download_audio(video_url)

            msg.edit("🎧 عم برسل الأغنية...")

            message.reply_audio(
                audio=file,
                caption=query,
                title=query,
                performer="Pro Music Bot"
            )

            os.remove(file)

        except Exception as e:
            msg.edit(f"❌ خطأ:\n{e}")


app.run()
