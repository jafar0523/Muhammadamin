import telebot
from telebot import types

# BotFather'dan olingan token
TOKEN = "8851034305:AAFEJS-F8FZBkjYFW3KTAPNPy1Remd5boOo"
bot = telebot.TeleBot(TOKEN)

# Test natijalari bazasi
TEST_BAZASI = {
    "112233": "📊 Test: Matematika\n✅ To'g'ri javoblar: 28 ta\n❌ Noto'g'ri javoblar: 2 ta\n🎯 Umumiy ball: 93.3%\n\nTahlil: Geometriya bo'limiga ko'proq e'tibor bering.",
    "445566": "📊 Test: Tarix\n✅ To'g'ri javoblar: 25 ta\n❌ Noto'g'ri javoblar: 5 ta\n🎯 Umumiy ball: 83.3%\n\nTahlil: Xonliklar davrini qayta takrorlang.",
    "778899": "📊 Test: English (CEFR)\n✅ To'g'ri javoblar: 20 ta\n❌ Noto'g'ri javoblar: 10 ta\n🎯 Umumiy ball: 66.6%\n\nTahlil: Listening qismida biroz xatolar bor."
}

# /start bosilganda ishlaydigan avto-javob
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    welcome_text = (
        f"Assalomu alaykum, {user_name}! 👋\n\n"
        "Natijalarni tahlil qilish botiga xush kelibsiz!\n\n"
        "📌 O'z test natijalaringizni bilish uchun sizga berilgan **maxsus kodni** botga yuboring (Masalan: 112233)"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown")

# Foydalanuvchi kod yuborganda tekshirish
@bot.message_handler(func=lambda message: True)
def check_test_code(message):
    foydalanuvchi_kodi = message.text.strip()
    
    if foydalanuvchi_kodi in TEST_BAZASI:
        javob_matni = TEST_BAZASI[foydalanuvchi_kodi]
        bot.send_message(message.chat.id, javob_matni)
    else:
        xato_matni = (
            "❌ Afsuski, bunday kod topilmadi.\n\n"
            "Iltimos, kodni to'g'ri kiritganingizni tekshiring yoki adminga murojaat qiling."
        )
        bot.send_message(message.chat.id, xato_matni)

# Botni ishga tushirish
print("Bot muvaffaqiyatli ishga tushdi...")
bot.infinity_polling()
