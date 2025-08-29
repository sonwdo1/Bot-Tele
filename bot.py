import os
import subprocess
import requests
import zipfile
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# ================== CONFIG ==================
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Railway Config Variables
RESOURCES_URL = "https://drive.google.com/file/d/1TQOJhgDtQkFeJRGDhmjc9nMgbqefOkOv/view?usp=drivesdk"  # Link Google Drive trực tiếp
ZIP_FILE = "resources.zip"
RESOURCE_DIR = "resources"
OUTPUT_DIR = os.path.join(RESOURCE_DIR, "output")

# ================== AUTO DOWNLOAD RESOURCES ==================
if not os.path.exists(RESOURCE_DIR):
    print("🔽 Downloading resources...")
    r = requests.get(RESOURCES_URL, stream=True)
    with open(ZIP_FILE, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

    print("📂 Extracting resources...")
    with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
        zip_ref.extractall(".")
    print("✅ Resources ready.")

# Tạo thư mục output nếu chưa có
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ================== BOT COMMANDS ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Chạy Tool"], ["Hướng dẫn", "Thông tin"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Xin chào! Đây là bot tool AOV 🔥\nChọn chức năng bên dưới:",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text == "Chạy Tool":
        await update.message.reply_text("🔄 Đang chạy tool, vui lòng chờ...")

        # Gọi tool gốc
        process = subprocess.run(
            ["python3", "lbdxaov.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Gửi log output
        if process.stdout:
            await update.message.reply_text(f"✅ Tool hoàn thành:\n{process.stdout[:3500]}")
        if process.stderr:
            await update.message.reply_text(f"⚠️ Có lỗi:\n{process.stderr[:3500]}")

        # Gửi file từ output nếu có
        files = os.listdir(OUTPUT_DIR)
        if files:
            for file in files:
                file_path = os.path.join(OUTPUT_DIR, file)
                await update.message.reply_document(open(file_path, "rb"))
        else:
            await update.message.reply_text("⚠️ Không tìm thấy file output nào!")

    elif text == "Hướng dẫn":
        await update.message.reply_text("📘 Hướng dẫn:\n1. Nhấn 'Chạy Tool'\n2. Nhập tài khoản & mật khẩu\n3. Nhận file kết quả")

    elif text == "Thông tin":
        await update.message.reply_text("🤖 Bot Tool AOV by Railway\nLiên hệ admin để biết thêm chi tiết.")

    else:
        await update.message.reply_text("❓ Không hiểu lệnh, vui lòng chọn trong menu.")

# ================== MAIN ==================
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()