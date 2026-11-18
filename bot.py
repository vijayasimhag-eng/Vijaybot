import asyncio
import os
from datetime import datetime
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Render kosam chinna Web Server - idi unte Live avuthundi
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is Live")
    def log_message(self, *args):
        pass

def keep_alive():
    port = int(os.environ.get("PORT", 10000))
    Thread(target=HTTPServer(("0.0.0.0", port), Handler).serve_forever, daemon=True).start()

TOKEN = os.environ.get("BOT_TOKEN") or os.environ.get("TELEGRAM_TOKEN") or os.environ.get("TELEGRAM_BOT_TOKEN")

# Trades anni ikkada save avuthayi
trades = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Namaste Vijay! 🙏\n"
        "Paper Trading Journal Bot Ready!\n\n"
        "Commands:\n"
        "/trade S1 PE Buy 25257 25180 - Trade save cheyadaniki\n"
        "/today - Eeroju Summary chudataniki"
    )

async def trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # /trade S1 PE Buy 25257 25180
    args = context.args
    if len(args) < 5:
        await update.message.reply_text("Format: /trade S1 PE Buy 25257 25180")
        return

    setup = args[0]  # S1
    option = args[1]  # PE
    side = args[2]  # Buy
    entry = args[3]
    exit_price = args[4]

    trade_text = f"{setup} {option} {side}"
    trades.append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "text": trade_text,
        "entry": entry,
        "exit": exit_price
    })

    await update.message.reply_text(
        f"✅ Trade Saved!\n"
        f"{trade_text}\n"
        f"Entry: {entry} | Exit: {exit_price}"
    )

async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today_date = datetime.now().strftime("%Y-%m-%d")
    today_trades = [t for t in trades if t["date"] == today_date]

    if not today_trades:
        await update.message.reply_text(f"📓 Today Journal - {today_date}\n\nInka trades levu.")
        return

    msg = f"📓 Today Journal - {today_date}\n\n"
    for t in today_trades:
        msg += f"• {t['text']} | Entry {t['entry']} -> Exit {t['exit']}\n"

    await update.message.reply_text(msg)

def main():
    print("Bot Running... PC off cheyaku", flush=True)
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("trade", trade))
    app.add_handler(CommandHandler("today", today))
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app.run_polling()

if __name__ == "__main__":
    main()
