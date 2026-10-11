import os
import logging
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ==================== 1. የእርስዎ መረጃዎች ====================
BOT_TOKEN = "8817368607:AAGk_w1nesJrexoeoTXVruoaHjgHwPYamhU"
ADMIN_CHAT_ID = 6887411607
CHANNEL_ID = -1004432663384

# የሚዲያ ፎልደር ስም
MEDIA_DIR = "media"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ==================== 2. የመጀመሪያ መልእክት (/start) ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "📊 **BHM — ሳይንሳዊ የቁመት ማሳደጊያ ፕሮግራም**\n\n"
        "ይህ ፕሮግራም ለማንኛውም ሰው ክፍት አይደለም።\n\n"
        "ለእርሶ ተስማሚ መሆኑን ለማረጋገጥ ጀምር የሚለውን ይጫኑ 👇"
    )
    keyboard = [[InlineKeyboardButton("ጀምር 🚀", callback_data="step_1")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    start_photo = os.path.join(MEDIA_DIR, "start.jpg")
    chat_id = update.effective_chat.id

    if os.path.exists(start_photo):
        with open(start_photo, "rb") as photo:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=welcome_text,
                reply_markup=reply_markup,
                parse_mode="Markdown",
            )
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text=welcome_text,
            reply_markup=reply_markup,
            parse_mode="Markdown",
        )


# ==================== 3. የጥያቄዎች እና የምርጫዎች ሂደት ====================
async def handle_user_survey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    chat_id = update.effective_chat.id

    # ደረጃ 1: የእድሜ ምርጫ
    if data == "step_1":
        text = "1/7 — የእድሜ ክልልዎ የየትኛው ውስጥ ነው?"
        keyboard = [
            [InlineKeyboardButton("ከ14 ዓመት በታች", callback_data="age_under14")],
            [InlineKeyboardButton("15 - 25", callback_data="age_15_25")],
            [InlineKeyboardButton("25 - 35", callback_data="age_25_35")],
            [InlineKeyboardButton("ከ35 ዓመት በላይ", callback_data="age_over35")],
        ]
        await context.bot.send_message(
            chat_id=chat_id, text=text, reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ደረጃ 2: የአሁን ቁመት
    elif data.startswith("age_"):
        await context.bot.send_message(
            chat_id=chat_id, text="✅ ይህ ዕድሜ ላይ ያሉ ደንበኞቻችን ከፍተኛ ውጤት አግኝተዋል!"
        )

        text = "2/7 — የአሁን ቁመትዎ ስንት ውስጥ ነው?"
        keyboard = [
            [InlineKeyboardButton("ከ160 CM በታች", callback_data="height_under160")],
            [InlineKeyboardButton("160 CM - 170 CM", callback_data="height_160_170")],
            [InlineKeyboardButton("171 CM - 180 CM", callback_data="height_171_180")],
            [InlineKeyboardButton("ከ180 CM በላይ", callback_data="height_over180")],
        ]
        await context.bot.send_message(
            chat_id=chat_id, text=text, reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ደረጃ 3: የቤተሰብ ሁኔታ
    elif data.startswith("height_"):
        await context.bot.send_message(
            chat_id=chat_id, text="✅ ፕሮግራሙ ለማንኛውም ቁመት ይሰራል፤ መጠኑ በዕድሜዎ ላይ ነው።"
        )

        text = "3/7 — የትኛው ላይ ነዎት?"
        keyboard = [
            [InlineKeyboardButton("ከቤተሰቦቼ ረጅም ነኝ", callback_data="fam_tallest")],
            [InlineKeyboardButton("ከአንዷ አበላልጬ ከአንዷ ጋር እኩል ነኝ", callback_data="fam_mid")],
            [InlineKeyboardButton("ከቤተሰቦቼ እኩል ነኝ", callback_data="fam_equal")],
            [InlineKeyboardButton("ከቤተሰቦቼ ሁላ አጭር ነኝ", callback_data="fam_shortest")],
        ]
        await context.bot.send_message(
            chat_id=chat_id, text=text, reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ደረጃ 4: የቀድሞ ሙከራዎች
    elif data.startswith("fam_"):
        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                "✅ የቤተሰብዎ ሁኔታ ተረድተናል — ይህ ፕሮግራም ለእርስዎ በቀላሉ ይሰራል። "
                "የዘረመል ተፅዕኖ 60% ብቻ ነው — 40% በእርስዎ ጥረት ነው!"
            ),
        )

        text = "4/7 — ከዚህ በፊት ቁመት ለመጨመር ምን ሞክረዋል?"
        keyboard = [
            [InlineKeyboardButton("የ Youtube ቪዲዮዎችን ብቻ", callback_data="prev_yt")],
            [InlineKeyboardButton("ስፖርቶችን ብቻ", callback_data="prev_sport")],
            [InlineKeyboardButton("ምንም የቻልኩት ነገር አልነበረም", callback_data="prev_none")],
        ]
        await context.bot.send_message(
            chat_id=chat_id, text=text, reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ደረጃ 5: 8ቱ የተጠቃሚዎች ፎቶዎች (Media Group/Album)
    elif data.startswith("prev_"):
        await context.bot.send_message(
            chat_id=chat_id, text="🔥 አብረዋቸው የጀመሩ ደንበኞቻችን ያገኙትን ውጤት ይመልከቱ፦"
        )

        # 8ቱን ፎቶዎች ከአልበም መልክ መላክ
        media_group = []
        for i in range(1, 9):
            img_path = os.path.join(MEDIA_DIR, f"result_{i}.jpg")
            if os.path.exists(img_path):
                media_group.append(InputMediaPhoto(open(img_path, "rb")))

        if media_group:
            try:
                await context.bot.send_media_group(chat_id=chat_id, media=media_group)
            except Exception as e:
                logger.error(f"Media group send error: {e}")

        results_summary = (
            "5/7 — የሰዎቻችን ያገኙት ውጤት፦\n\n"
            "Nati ➔ +10 CM (6 ወር)\n"
            "Henok ➔ +8 CM (4 ወር)\n"
            "Tomas ➔ +7 CM (5 ወር)\n"
            "Abel ➔ +6 CM (4 ወር)\n"
            "Abush ➔ +6.5 CM (5 ወር)\n"
            "Dagim ➔ +7 CM (5 ወር)\n"
            "Biniyam ➔ +7 CM (5 ወር)\n\n"
            "እርስዎ ስንት CM መጨመር ይፈልጋሉ? 👇"
        )
        keyboard = [
            [InlineKeyboardButton("3 - 5 CM", callback_data="goal_3_5")],
            [InlineKeyboardButton("5 - 8 CM", callback_data="goal_5_8")],
            [InlineKeyboardButton("8 - 10 CM", callback_data="goal_8_10")],
        ]
        await context.bot.send_message(
            chat_id=chat_id,
            text=results_summary,
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # ደረጃ 6: ትኩረት/ቁርጠኝነት
    elif data.startswith("goal_"):
        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                "✅ ለውጥ ይቻላል! Biniyam 7 CM ጨመረ — ልክ ያንተ አይነት ዕድሜ ላይ ነበር። "
                "በ 2018 ዓ.ም ፕሮግራማችን ተጠቅመው ውጤት ካገኙ ሰዎች አንዱ ነው።"
            ),
        )

        text = "6/7 — በቀን ውስጥ ለዚህ የህይወት ለውጥ ምን ያህል ትኩረት አለዎት?"
        keyboard = [
            [InlineKeyboardButton("በራስ መተማመኔ ላይ ከፍተኛ ጉዳት ደርሷል", callback_data="focus_high")],
            [InlineKeyboardButton("ትኩስ በሰራ ልቤ አለኝ", callback_data="focus_mid")],
        ]
        await context.bot.send_message(
            chat_id=chat_id, text=text, reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ደረጃ 7: ዝግጁነት ማረጋገጥ
    elif
