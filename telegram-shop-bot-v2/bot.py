import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters


# =========================================================
# BOT TOKEN
# =========================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is not set.")


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
₱50 ♡ — solo

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
# RENDER HTTP SERVER
# =========================================================

class HealthHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Telegram bot is running.")

    def log_message(self, format, *args):
        return


def run_health_server():
    port = int(os.getenv("PORT", "10000"))

    server = HTTPServer(
        ("0.0.0.0", port),
        HealthHandler
    )

    print(f"Health server running on port {port}")

    server.serve_forever()


# =========================================================
# AUTOMATIC REPLY FUNCTION
# =========================================================

async def reply_to_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message or not update.message.text:
        return

    message = update.message.text.lower().strip()

    # -----------------------------------------------------
    # FULL PRICELIST KEYWORDS
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
        "mag kano po",
        "how much",
        "how much po",
        "pa avail po",
        "pl",
    ]

    # -----------------------------------------------------
    # SERVICE-SPECIFIC REPLIES
    # -----------------------------------------------------

    try:

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

        if (
            "youtube music" in message
            or "youtube" in message
            or message == "yt"
        ):
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

        if "disney+" in message or "disney" in message:
            await update.message.reply_text(
                DISNEY,
                parse_mode="HTML"
            )
            return

        # -------------------------------------------------
        # FULL PRICELIST RESPONSE
        # -------------------------------------------------

        if any(
            keyword in message
            for keyword in full_pricelist_keywords
        ):
            await update.message.reply_text(
                PRICELIST,
                parse_mode="HTML"
            )
            return

    except Exception as e:

        # Prevent one failed Telegram reply
        # from causing an unhandled exception.
        print(f"Telegram reply error: {e}")


# =========================================================
# START BOT
# =========================================================

def main():

    # Start Render health server in the background.
    health_thread = threading.Thread(
        target=run_health_server,
        daemon=True
    )

    health_thread.start()

    # Create Telegram application.
    app = Application.builder().token(BOT_TOKEN).build()

    # Listen for normal text messages.
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            reply_to_message
        )
    )

    print("Bot is running...")
    print("Telegram polling started.")

    # Start Telegram polling.
    app.run_polling()


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    main()
