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

# ADMIN TELEGRAM ID
ADMIN_ID = 5541785551

DATA_FILE = "data.json"

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
  """JSON fayldan ma'lumotlarni o'qish."""
  if not os.path.exists(DATA_FILE):
    return {"tokens": {}, "users": {}, "user_submissions": {}}
  try:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
      return json.load(f)
  except Exception as e:
    logging.error(f"Faylni o'qishda xatolik: {e}")
    return {"tokens": {}, "users": {}, "user_submissions": {}}


def save_data(data):
  """JSON faylga saqlash."""
  try:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
      json.dump(data, f, indent=2, ensure_ascii=False)
  except Exception as e:
    logging.error(f"Faylga saqlashda xatolik: {e}")


def parse_user_answers(text):
  """Javoblarni ajratish."""
  answers = {}
  matches = re.findall(
      r"(\d+)[\s\-\:\.\=]+([A-Za-zА-Яа-яO‘o‘O’o’G‘g‘ʻʼ’`]+)", text
  )
  for q_num, ans in matches:
    answers[int(q_num)] = ans.strip().upper()
  return answers


# --- ADMIN PANEL BUYRUG'I ---
@bot.message_handler(commands=["admin"])
def admin_handler(message):
  if message.from_user.id != ADMIN_ID:
    bot.reply_to(message, "❌ Siz bot admini emassiz!")
    return

  data = load_data()
  submissions = data.get("user_submissions", {})
  tokens = data.get("tokens", {})

  used_tokens_count = sum(1 for t in tokens.values() if t.get("used", False))

  text = "⚙️ **ADMIN PANEL**\n\n"
  text += f"Jami tokenlar: {len(tokens)}\n"
  text += f"Ishlatilgan tokenlar: {used_tokens_count}\n"
  text += f"Test topshirganlar: {len(submissions)}\n\n"
  text += "📋 **Natijalar:**\n"

  if not submissions:
    text += "Hozircha hech kim test topshirmadi."
  else:
    for u_id, sub in submissions.items():
      name = sub.get("full_name", "Noma'lum")
      score = sub.get("score", "0")
      text += f"• **{name}**: {score}\n"

  bot.send_message(message.chat.id, text, parse_mode="Markdown")


# --- START BUYRUG'I ---
@bot.message_handler(commands=["start"])
def start_handler(message):
  welcome_text = (
      f"Assalomu alaykum, **{message.from_user.first_name}**!\n\n"
      "Tizimdan foydalanish uchun, iltimos, to'liq **Ismingiz va Familiyangizni** kiriting (masalan: *Ali Valiyev*):"
  )
  bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown")


# --- XABARLARNI QAYTA ISHLASH ---
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

  # 1-BOSQICH: Ism va Familiya
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
    tokens = data.get("tokens", {})
    clean_input = user_input.replace(" ", "").strip().lower()

    matched_token_key = None
    for token_key in tokens.keys():
      if token_key.strip().lower() == clean_input:
        matched_token_key = token_key
        break

    if matched_token_key:
      token_info = tokens[matched_token_key]

      if not token_info.get("used", False):
        tokens[matched_token_key]["used"] = True
        tokens[matched_token_key]["used_by"] = message.from_user.id

        data["users"][user_id]["activated_token"] = matched_token_key
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
          "❌ **Noto'g'ri token kiritildi.**\n"
          "Iltimos, sizga berilgan to'g'ri tokeningizni kiriting.",
      )
    return

  # 3-BOSQICH: Javoblarni hisoblash
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
