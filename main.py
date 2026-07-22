import json
import logging
import os
import re
from telebot import TeleBot

# Loggingni sozlash
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN_HERE")
bot = TeleBot(BOT_TOKEN)

DATA_FILE = "data.json"

# Javoblar kaliti
CORRECT_ANSWERS = {
    1: "A",
    2: "A",
    3: "A",
    4: "A",
    5: "A",
    6: "A",
    7: "A",
    8: "A",
    9: "A",
    10: "A",
    11: "B",
    12: "B",
    13: "B",
    14: "B",
    15: "B",
    16: "B",
    17: "B",
    18: "B",
    19: "B",
    20: "C",
    21: "C",
    22: "C",
    23: "C",
    24: "C",
    25: "C",
    26: "C",
    27: "C",
    28: "D",
    29: "D",
    30: "D",
    31: "D",
    32: "D",
    33: "D",
    34: "D",
    35: "D",
    36: "GERMANIYA",
    37: "ITALIYA",
    38: "ARMADA",
    39: "ABDULAZIZ",
    40: "MUHAMMADAMIN",
    41: "JAVOHIR",
    42: "OTABEK",
    43: "SHOMURODOV",
    44: "KALBOSH",
    45: "KABRAL",
}


def load_data():
  """JSON fayldan ma'lumotlarni xavfsiz o'qish."""
  if not os.path.exists(DATA_FILE):
    return {"tokens": {}, "users": {}, "user_submissions": {}}
  try:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
      return json.load(f)
  except Exception as e:
    logging.error(f"Faylni o'qishda xatolik: {e}")
    return {"tokens": {}, "users": {}, "user_submissions": {}}


def save_data(data):
  """Ma'lumotlarni JSON faylga saqlash."""
  try:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
      json.dump(data, f, indent=2, ensure_ascii=False)
  except Exception as e:
    logging.error(f"Faylga saqlashda xatolik: {e}")


def parse_user_answers(text):
  """Foydalanuvchi javoblarini ajratib olish (1-A 2-B ... 36-GERMANIYA formatida)."""
  answers = {}
  matches = re.findall(
      r"(\d+)[\s\-\:\.\=]+([A-Za-zА-Яа-яO‘o‘O’o’G‘g‘ʻʼ’`]+)", text
  )
  for q_num, ans in matches:
    answers[int(q_num)] = ans.strip().upper()
  return answers


@bot.message_handler(commands=["start"])
def start_handler(message):
  welcome_text = (
      f"Assalomu alaykum, **{message.from_user.first_name}**!\n\n"
      "Tizimdan foydalanish uchun, iltimos, to'liq **Ismingiz va Familiyangizni** kiriting (masalan: *Ali Valiyev*):"
  )
  bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown")


@bot.message_handler(func=lambda message: True)
def process_message(message):
  user_input = message.text.strip()
  user_id = str(message.from_user.id)
  data = load_data()

  if "users" not in data:
    data["users"] = {}
  if "tokens" not in data:
    data["tokens"] = {}
  if "user_submissions" not in data:
    data["user_submissions"] = {}

  user_data = data["users"].get(user_id, {})

  # 1-BOSQICH: Ism va Familiyani qabul qilish
  if "full_name" not in user_data:
    data["users"][user_id] = {
        "telegram_name": message.from_user.first_name,
        "username": message.from_user.username,
        "full_name": user_input,
    }
    save_data(data)

    bot.reply_to(
        message,
        f"Rahmat, **{user_input}**!\n\n"
        "Endi sizga taqdim etilgan **maxsus tokeningizni** kiriting:",
        parse_mode="Markdown",
    )
    return

  # 2-BOSQICH: Tokenni tekshirish
  if "activated_token" not in user_data:
    tokens = data["tokens"]

    if user_input in tokens:
      if not tokens[user_input].get("used", False):
        tokens[user_input]["used"] = True
        tokens[user_input]["used_by"] = message.from_user.id

        data["users"][user_id]["activated_token"] = user_input
        save_data(data)

        bot.reply_to(
            message,
            "✅ **Token muvaffaqiyatli faollashtirildi!**\n\n"
            "Endi test javoblaringizni quyidagi formatda yuborishingiz mumkin:\n"
            "`1-A 2-B ... 36-GERMANIYA ... 45-KABRAL`",
            parse_mode="Markdown",
        )
      else:
        bot.reply_to(
            message,
            "❌ **Bu token allaqachon boshqa foydalanuvchi tomonidan ishlatilgan!**",
        )
    else:
      bot.reply_to(
          message,
          "❌ **Noto'g'ri token kiritildi.** Iltimos, to'g'ri token yuboring.",
      )
    return

  # 3-BOSQICH: Test javoblarini hisoblash
  user_answers = parse_user_answers(user_input)

  if not user_answers:
    bot.reply_to(
        message,
        "⚠️ **Javoblar formati aniqlanmadi.**\n\n"
        "Javoblarni quyidagicha formatda yuboring:\n"
        "`1-A 2-B 3-C ... 36-GERMANIYA`",
        parse_mode="Markdown",
    )
    return

  correct_count = 0
  total_questions = len(CORRECT_ANSWERS)

  for q_num, correct_ans in CORRECT_ANSWERS.items():
    user_ans = user_answers.get(q_num, "")
    if user_ans == correct_ans.upper():
      correct_count += 1

  data["user_submissions"][user_id] = {
      "full_name": user_data.get("full_name"),
      "score": f"{correct_count}/{total_questions}",
      "answers": user_answers,
  }
  save_data(data)

  bot.reply_to(
      message,
      f"📊 **{user_data.get('full_name')}**, sizning natijangiz: **{correct_count} / {total_questions}**\n\n"
      "Javoblaringiz muvaffaqiyatli qabul qilindi!",
      parse_mode="Markdown",
  )


if __name__ == "__main__":
  logging.info("Bot ishga tushdi...")
  bot.infinity_polling(skip_pending=True)
    
