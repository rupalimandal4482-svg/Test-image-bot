import os
from io import BytesIO
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from huggingface_hub import InferenceClient

BOT_TOKEN = os.environ["BOT_TOKEN"]
HF_TOKEN = os.environ["HF_TOKEN"]

# Powerful model
MODEL_NAME = "Lykon/dreamshaper-xl-1.0"

client = InferenceClient(
    model=MODEL_NAME,
    token=HF_TOKEN,
    timeout=180
)

# ---------- START ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Priya HF Image Bot Live\n\n"
        "Use:\n"
        "/image <prompt>"
    )

# ---------- IMAGE ----------
async def image_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage:\n/image cute anime girl")
        return

    prompt = " ".join(context.args)
    await update.message.reply_text("🎨 Generating image...")

    try:
        image = client.text_to_image(prompt)

        bio = BytesIO()
        image.save(bio, format="JPEG")
        bio.seek(0)

        await update.message.reply_photo(
            photo=InputFile(bio, "image.jpg"),
            caption=f"✨ {prompt}"
        )

    except Exception as e:
        await update.message.reply_text("❌ Generation failed")
        print("HF ERROR:", e)

# ---------- MAIN ----------
def main():
    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .connect_timeout(30)
        .read_timeout(30)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("image", image_cmd))

    print("🚀 Priya HF Hub Image Bot Running")
    app.run_polling()

if __name__ == "__main__":
    main()
