from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
import yt_dlp
import asyncio
import os

API_ID = 32854686
API_HASH = "43575e3f5e3a443256f44fca714ac194"
BOT_TOKEN = "8419311415:AAEcq96mgsGvbXLQt2Bc2fQGtdO6VjmIV6k"
SESSION = "BAH1Up4Aib9A7h8b3jZtuVOClPz0fPCJude8a1ds-QlB_hLfHK73G0OWyXRHcZimQfr03DweLxvOwHBIMoPnBnfP0ngXeiVzCfcZbLn8sIvxuiwpsim7pElAHYsOLQRzxvPoF58aCxSeFlyft74qzjENRXwiIi08dOQlFB-j6KN1MPGHwc60Apd5bsyt6B_uZdtaBQJqiwP_IAAnUNQdpzsH-bnL2GJiSpP9HIEJ_VavumhXt_QCcOvVgck3XCYNBBQ1AqwzzIASaf7VVkkrVjSfy8bHzTJyorJzbYvPBeNHmphHILS4Qs5vQXdgaSAQy89undt5HN2zzePaVd8sDjZgi1NU_gAAAAIKfc6oAA"

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user = Client("user", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)
call = PyTgCalls(user)

queue = {}

# تحميل + معلومات
def download(query):
    ydl_opts = {
        "format": "bestaudio",
        "default_search": "ytsearch1",
        "outtmpl": "song.%(ext)s",
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=True)

        if "entries" in info:
            info = info["entries"][0]

        file = ydl.prepare_filename(info)
        title = info.get("title", "Unknown")

        return file, title

# أزرار
def buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⏭ تخطي", callback_data="skip"),
            InlineKeyboardButton("⏸ توقف", callback_data="pause"),
            InlineKeyboardButton("▶️ كمل", callback_data="resume"),
        ]
    ])

# 🎧 تشغيل عادي
@app.on_message(filters.text & filters.regex("^يوت"))
def send_audio(client, message):
    query = message.text.replace("يوت", "").strip()

    if not query:
        return message.reply("❌ اكتب اسم الأغنية")

    msg = message.reply("⏳ عم بحمّل...")

    try:
        file, title = download(query)

        msg.edit("🎧 تم الإرسال", reply_markup=buttons())

        message.reply_audio(
            audio=file,
            title=title,
            performer="Music Bot"
        )

        os.remove(file)

    except Exception as e:
        msg.edit(f"❌ خطأ:\n{e}")

# 🎙 تشغيل بالمكالمة
@app.on_message(filters.text & filters.regex("^(تشغيل|شغل)"))
async def play_vc(_, message):
    chat_id = message.chat.id
    query = message.text.split(None, 1)[1]

    msg = await message.reply("⏳ عم بحمّل...")

    file, title = download(query)

    if chat_id not in queue:
        queue[chat_id] = []

    queue[chat_id].append(file)

    if len(queue[chat_id]) == 1:
        await call.join_group_call(chat_id, AudioPiped(file))
        await msg.edit(f"🎙 شغال: {title}", reply_markup=buttons())
    else:
        await msg.edit("📃 انضافت للقائمة", reply_markup=buttons())

# 🎛 أزرار التحكم
@app.on_callback_query()
async def callbacks(_, query):
    chat_id = query.message.chat.id

    if query.data == "skip":
        if chat_id in queue and len(queue[chat_id]) > 1:
            old = queue[chat_id].pop(0)
            os.remove(old)
            new = queue[chat_id][0]
            await call.change_stream(chat_id, AudioPiped(new))
            await query.answer("⏭ تم التخطي")
        else:
            await query.answer("❌ ما في شي")

    elif query.data == "pause":
        await call.pause_stream(chat_id)
        await query.answer("⏸ توقف")

    elif query.data == "resume":
        await call.resume_stream(chat_id)
        await query.answer("▶️ كمل")

# ⛔ ايقاف كامل
@app.on_message(filters.command("ايقاف"))
async def stop_all(_, message):
    chat_id = message.chat.id

    if chat_id in queue:
        for f in queue[chat_id]:
            if os.path.exists(f):
                os.remove(f)
        queue[chat_id] = []

    await call.leave_group_call(chat_id)
    await message.reply("⛔ تم ايقاف كلشي")

# ⏸ توقف مؤقت
@app.on_message(filters.command("توقف"))
async def pause(_, message):
    await call.pause_stream(message.chat.id)
    await message.reply("⏸ توقف مؤقت")

# ▶️ كمل
@app.on_message(filters.command("كمل"))
async def resume(_, message):
    await call.resume_stream(message.chat.id)
    await message.reply("▶️ رجع التشغيل")

# 📜 الأوامر
@app.on_message(filters.command("الاوامر"))
def help_cmd(_, message):
    message.reply("""
📜 **أوامر البوت**

🎧 يوت + اسم الأغنية
🎙 تشغيل + اسم الأغنية

🎛 التحكم:
⏭ تخطي
⏸ توقف
▶️ كمل
⛔ ايقاف

🛡 حماية:
🔇 كتم (بالرد)
🚫 حظر (بالرد)
👢 طرد (بالرد)
""")

# 🛡 كتم
@app.on_message(filters.command("كتم") & filters.reply)
async def mute(_, message):
    user_id = message.reply_to_message.from_user.id
    await message.chat.restrict_member(user_id, ChatPermissions())
    await message.reply("🔇 تم الكتم")

# 🚫 حظر
@app.on_message(filters.command("حظر") & filters.reply)
async def ban(_, message):
    user_id = message.reply_to_message.from_user.id
    await message.chat.ban_member(user_id)
    await message.reply("🚫 تم الحظر")

# 👢 طرد
@app.on_message(filters.command("طرد") & filters.reply)
async def kick(_, message):
    user_id = message.reply_to_message.from_user.id
    await message.chat.ban_member(user_id)
    await message.chat.unban_member(user_id)
    await message.reply("👢 تم الطرد")

app.start()
user.start()
call.start()
asyncio.get_event_loop().run_forever()
