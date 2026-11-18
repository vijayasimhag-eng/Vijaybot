import os
import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# IKKADA NEE KOTTHA TOKEN PETTU - Revoke chesaka vachina kottha token
TOKEN = os.getenv("BOT_TOKEN")
trades = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Namaste Vijay! 🙏\nPaper Trading Journal Bot Ready!\n\n"
        "Commands:\n"
        "/trade S1 PE Buy 25257 25180 - Trade add cheyadaniki\n"
        "/today - Eroju summary chudataniki"
    )

async def trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        strategy = args[0]
        side = args[1] + " " + args[2]
        entry = args[3]
        exit_p = args[4]
        trades.append(f"{strategy} {side} | Entry {entry} -> Exit {exit_p}")
        await update.message.reply_text(f"✅ Trade Saved!\n{strategy} {side}\nEntry: {entry} | Exit: {exit_p}")
    except:
        await update.message.reply_text("Format thappu Vijay!\nIla pampu: /trade S1 PE Buy 25257 25180")

async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not trades:
        await update.message.reply_text("Eroju inka trade ledu Vijay. S1 kosam wait cheddam.")
        return
    msg = "📓 Today Journal - " + str(datetime.date.today()) + "\n\n"
    for t in trades:
        msg += "• " + t + "\n"
    await update.message.reply_text(msg)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("trade", trade))
    app.add_handler(CommandHandler("today", today))
    print("Bot Running... PC off cheyaku")
    app.run_polling()