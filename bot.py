import os
import logging
import requests
import zipfile
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# ====== BOT TOKEN (lấy từ Railway Variables hoặc thay trực tiếp nếu muốn) ======
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ====== LINK GOOGLE DRIVE ZIP (gắn trực tiếp) ======
RESOURCE_URL = "https://drive.google.com/uc?id=1b24XUdQxh_U8wmGvnSae7YSRRtLMok9I&export=download"

# ================== SETUP LOG ==================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ================== TẢI VÀ GIẢI NÉN RESOURCES ==================
def download_resources():
    print("📥 Downloading resources...")
    response = requests.get(RESOURCE_URL, stream=True)

    if response.status_code != 200:
        raise Exception("❌ Không tải được resources, kiểm tra lại link.")

    with open("resources.zip", "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print("📦 Extracting resources...")
    try:
        with zipfile.ZipFile("resources.zip", "r") as zip_ref:
            zip_ref.extractall("resources")
        print("✅ Resources extracted thành công.")
    except zipfile.BadZipFile:
        raise Exception("❌ File tải về không phải là ZIP. Kiểm tra lại RESOURCE_URL.")

# ================== COMMAND HANDLERS ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["/userid", "/choose"],
        ["/danhsachdachon", "/chaymod"],
        ["/layfile", "/chucnangthem"],
        ["/checkvip", "/timkiemskin"],
        ["/deleteskin"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("🤖 Bot đã sẵn sàng!\nChọn chức năng bên dưới:", reply_markup=reply_markup)

async def userid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🆔 ID của bạn: {update.message.from_user.id}")

async def choose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎨 Vui lòng nhập tên skin bạn muốn chọn...")

async def danhsachdachon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📋 Đây là danh sách skin đã chọn (demo).")

async def chaymod(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚙️ Đang tiến hành Auto ModSkin...")

async def layfile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_path = "output/result.txt"  # ví dụ file tool tạo
    if os.path.exists(file_path):
        await update.message.reply_document(document=open(file_path, "rb"))
    else:
        await update.message.reply_text("❌ Chưa có file kết quả.")

async def chucnangthem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔧 Chức năng: Cam xa, HD Skill, PersonalButton (demo).")

async def checkvip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💎 Bạn chưa có VIP (demo).")

async def timkiemskin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Nhập tên skin để tìm...")

async def deleteskin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🗑️ Skin đã xóa thành công (demo).")

# ================== MAIN ==================
def main():
    # Tải resource (bỏ qua bước VPN + Enter)
    download_resources()

    application = Application.builder().token(BOT_TOKEN).build()

    # Register command
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("userid", userid))
    application.add_handler(CommandHandler("choose", choose))
    application.add_handler(CommandHandler("danhsachdachon", danhsachdachon))
    application.add_handler(CommandHandler("chaymod", chaymod))
    application.add_handler(CommandHandler("layfile", layfile))
    application.add_handler(CommandHandler("chucnangthem", chucnangthem))
    application.add_handler(CommandHandler("checkvip", checkvip))
    application.add_handler(CommandHandler("timkiemskin", timkiemskin))
    application.add_handler(CommandHandler("deleteskin", deleteskin))

    # Chạy bot
    application.run_polling()

if __name__ == "__main__":
    main()
