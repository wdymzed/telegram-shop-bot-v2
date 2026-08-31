import os
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

# =========================================================
# BOT TOKEN
# =========================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")


# =========================================================
# FULL PRICELIST
# =========================================================

PRICELIST = """
🌷 <b>PRICELIST</b> 🌷
── ୨ ୧ <b>digital services</b> ୨ ୧ ── ☁️

<b>NETFLIX</b> ♡
₱70 — shared profile
₱100 — solo profile

<b>CANVA</b> ♡
₱5 — via invite
₱15 — family head

<b>YOUTUBE / YOUTUBE MUSIC</b> ♡
₱10 — via invite
₱20 — family head
₱30 — individual

<b>SPOTIFY PREMIUM</b> ♡
₱50 🪽 — 3 months link via checkout

<b>DISNEY+</b> ♡
₱50 — solo

ᥫ᭡ thank you for supporting my shop!

feel free to message
@yuuanprems & @yuuanprem
for orders & inquiries ♡
"""


# =========================================================
# INDIVIDUAL SERVICE PRICES
# =========================================================

NETFLIX = """
🌷 <b>NETFLIX</b> 🌷

₱70 ♡ — shared profile
₱100 ♡ — solo profile

For orders & inquiries:
@yuuanprems & @yuuanprem
"""

CANVA = """
🌷 <b>CANVA</b> 🌷

₱5 ♡ — via invite
₱15 ♡ — family head

For orders & inquiries:
@yuuanprems & @yuuanprem
"""

YOUTUBE = """
🌷 <b>YOUTUBE / YOUTUBE MUSIC</b> 🌷

₱10 ♡ — via invite
₱20 ♡ — family head
₱30 ♡ — individual

For orders & inquiries:
@yuuanprems & @yuuanprem
"""

SPOTIFY = """
🌷 <b>SPOTIFY PREMIUM</b> 🌷

₱50 🪽 — 3 months link via checkout

For orders & inquiries:
@yuuanprems & @yuuanprem
"""

DISNEY = """
🌷 <b>DISNEY+</b> 🌷

₱50 ♡ — solo

For orders & inquiries:
@yuuanprems & @yuuanprem
"""


# =========================================================
# AUTOMATIC REPLY FUNCTION
# =========================================================

async def reply_to_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    # Ignore messages without text
    if not update.message or not update.message.text:
        return

    message = update.message.text.lower().strip()

    # -----------------------------------------------------
    # FULL PRICELIST
    # -----------------------------------------------------

    full_pricelist_keywords = [
        "pricelist",
        "price list",
        "price",
        "prices",
        "hm",
        "magkano",
        "mag kano",
        "magkano po",
        "how much",
    ]

    # -----------------------------------------------------
    # SERVICE-SPECIFIC REPLIES
    # -----------------------------------------------------

    if "netflix" in message:
        await update.message.reply_text(
            NETFLIX,
            parse_mode="HTML"
        )
        return

    if "canva" in message:
        await update.message.reply_text(
            CANVA,
            parse_mode="HTML"
        )
        return

    if "youtube" in message or "youtube music" in message or message == "yt":
        await update.message.reply_text(
            YOUTUBE,
            parse_mode="HTML"
        )
        return

    if "spotify" in message:
        await update.message.reply_text(
            SPOTIFY,
            parse_mode="HTML"
        )
        return

    if "disney" in message or "disney+" in message:
        await update.message.reply_text(
            DISNEY,
            parse_mode="HTML"
        )
        return

    # -----------------------------------------------------
    # FULL PRICELIST RESPONSE
    # -----------------------------------------------------

    if any(keyword in message for keyword in full_pricelist_keywords):
        await update.message.reply_text(
            PRICELIST,
            parse_mode="HTML"
        )
        return


# =========================================================
# START BOT
# =========================================================

def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            reply_to_message
        )
    )

    print("Bot is running...")
    print("Press Ctrl+C to stop the bot.")

    app.run_polling()


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    main()