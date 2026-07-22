import io
import json
import logging
import math
import os
import re

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from telebot import TeleBot

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN_HERE")
bot = TeleBot(BOT_TOKEN)

ADMIN_ID = 5541785551
DATA_FILE = "data.json"

CORRECT_ANSWERS = {
    1: {"ans": "A", "diff": -1.0},
    2: {"ans": "A", "diff": -1.0},
    3: {"ans": "A", "diff": -1.0},
    4: {"ans": "A", "diff": -0.8},
    5: {"ans": "A", "diff": -0.8},
    6: {"ans": "A", "diff": -0.5},
    7: {"ans": "A", "diff": -0.5},
    8: {"ans": "A", "diff": -0.5},
    9: {"ans": "A", "diff": 0.0},
    10: {"ans": "A", "diff": 0.0},
    11: {"ans": "B", "diff": 0.0},
    12: {"ans": "B", "diff": 0.0},
    13: {"ans": "B", "diff": 0.2},
    14: {"ans": "B", "diff": 0.2},
    15: {"ans": "B", "diff": 0.5},
    16: {"ans": "B", "diff": 0.5},
    17: {"ans": "B", "diff": 0.5},
    18: {"ans": "B", "diff": 0.8},
    19: {"ans": "B", "diff": 0.8},
    20: {"ans": "C", "diff": 1.0},
    21: {"ans": "C", "diff": 1.0},
    22: {"ans": "C", "diff": 1.0},
    23: {"ans": "C", "diff": 1.2},
    24: {"ans": "C", "diff": 1.2},
    25: {"ans": "C", "diff": 1.5},
    26: {"ans": "C", "diff": 1.5},
    27: {"ans": "C", "diff": 1.5},
    28: {"ans": "D", "diff": 1.8},
    29: {"ans": "D", "diff": 1.8},
    30: {"ans": "D", "diff": 2.0},
    31: {"ans": "D", "diff": 2.0},
    32: {"ans": "D", "diff": 2.2},
    33: {"ans": "D", "diff": 2.2},
    34: {"ans": "D", "diff": 2.5},
    35: {"ans": "D", "diff": 2.5},
    36: {"ans": "GERMANIYA", "diff": 2.0},
    37: {"ans": "ITALIYA", "diff": 2.0},
    38: {"ans": "ARMADA", "diff": 2.2},
    39: {"ans": "ABDULAZIZ", "diff": 2.2},
    40: {"ans": "MUHAMMADAMIN", "diff": 2.5},
    41: {"ans": "JAVOHIR", "diff": 2.5},
    42: {"ans": "OTABEK", "diff": 2.8},
    43: {"ans": "SHOMURODOV", "diff": 2.8},
    44: {"ans": "KALBOSH", "diff": 3.0},
    45: {"ans": "KABRAL", "diff": 3.0},
}


def calculate_rasch_score(user_answers):
  total_questions = len(CORRECT_ANSWERS)
  correct_count = 0
  sum_diff_correct = 0

  for q_num, q_info in CORRECT_ANSWERS.items():
    user_ans = user_answers.get(q_num, "")
    if user_ans == q_info["ans"].upper():
      correct_count += 1
      sum_diff_correct += q_info["diff"]

  if correct_count == 0:
    ability_theta = -3.5
  elif correct_count == total_questions:
    ability_theta = 4.5
  else:
    r = correct_count
    n = total_questions
    mean_diff = sum_diff_correct / r if r > 0 else 0
    ability_theta = math.log(r / (n - r)) + (mean_diff * 0.2)

  rasch_scale_score = min(100, max(0, round(50 + (ability_theta * 10), 1)))
  return correct_count, total_questions, round(ability_theta, 2), rasch_scale_score


def load_data():
  if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
    return {
        "tokens": {
            "f9N3fj5wQ1mH7dN6": {"used": False},
            "token123": {"used": False},
        },
        "users": {},
        "user_submissions": {},
        "is_active": True,
    }
  try:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
      data = json.load(f)
      if "tokens" not in data or not isinstance(data["tokens"], dict):
        data["tokens"] = {}
      if "users" not in data:
        data["users"] = {}
      if "user_submissions" not in data:
        data["user_submissions"] = {}
      if "is_active" not in data:
        data["is_active"] = True
      return data
  except Exception as e:
    logging.error(f"Faylni o'qishda xatolik: {e}")
    return {
        "tokens": {},
        "users": {},
        "user_submissions": {},
        "is_active": True,
    }


def save_data(data):
  try:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
      json.dump(data, f, indent=2, ensure_ascii=False)
  except Exception as e:
    logging.error(f"Faylga saqlashda xatolik: {e}")


def parse_user_answers(text):
  answers = {}
  matches = re.findall(
      r"(\d+)[\s\-\:\.\=]+([A-Za-zА-Яа-яO‘o‘O’o’G‘g‘ʻʼ’`]+)", text
  )
  for q_num, ans in matches:
    answers[int(q_num)] = ans.strip().upper()
  return answers


def generate_pdf_report(submissions):
  buffer = io.BytesIO()
  doc = SimpleDocTemplate(
      buffer, pagesize=A4, rightMargin=25, leftMargin=25, topMargin=30, bottomMargin=30
  )
  elements = []

  styles = getSampleStyleSheet()
  title_style = styles["Heading1"]
  title_style.alignment = 1

  elements.append(
      Paragraph("<b>TEST NATIJALARI (RASCH MODELI)</b>", title_style)
  )
  elements.append(Spacer(1, 15))

  table_data = [[
      "№",
      "Ism Familiya",
      "To'g'ri",
      "Rasch Logit (θ)",
      "Rasch Ball (0-100)",
  ]]

  count = 1
  for u_id, sub in submissions.items():
    name = sub.get("full_name", "Noma'lum")
    score = sub.get("score", "0/45")
    theta = str(sub.get("rasch_theta", "0.0"))
    rasch_score = str(sub.get("rasch_score", "0"))

    table_data.append([str(count), name, score, theta, rasch_score])
    count += 1

  table = Table(table_data, colWidths=[30, 210, 80, 100, 100])
  table.setStyle(
      TableStyle([
          ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1A365D")),
          ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
          ("ALIGN", (0, 0), (-1, -1), "CENTER"),
          ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
          ("FONTSIZE", (0, 0), (-1, 0), 10),
          ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
          ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F7FAFC")),
          ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E0")),
      ])
  )

  elements.append(table)
  doc.build(elements)

  buffer.seek(0)
  return buffer


@bot.message_handler(commands=["admin"])
def admin_handler(message):
  if message.from_user.id != ADMIN_ID:
    bot.reply_to(message, "❌ Siz bot admini emassiz!")
    return

  data = load_data()
  submissions = data.get("user_submissions", {})
  tokens = data.get("tokens", {})
  is_active = data.get("is_active", True)

  used_tokens_count = sum(1 for t in tokens.values() if t.get("used", False))
  status_str = "🟢 OCHIQ (Aktiv)" if is_active else "🔴 TO'XTATILGAN"

  text = f"⚙️ **ADMIN PANEL**\n\n"
  text += f"Test holati: **{status_str}**\n"
  text += f"Jami tokenlar: {len(tokens)}\n"
  text += f"Ishlatilgan tokenlar: {used_tokens_count}\n"
  text += f"Test topshirganlar: {len(submissions)}\n\n"
  text += "Boshqaruv:\n"
  text += "• `/pdf` - Rasch modeli PDF hisobotini yuklab olish\n"
  text += "• `/stop` - Testni to'xtatish\n"
  text += "• `/start_test` - Testni qayta yoqish\n"

  bot.send_message(message.chat.id, text, parse_mode="Markdown")


@bot.message_handler(commands=["pdf", "results"])
def send_pdf_handler(message):
  if message.from_user.id != ADMIN_ID:
    return

  data = load_data()
  submissions = data.get("user_submissions", {})

  if not submissions:
    bot.reply_to(message, "⚠️ Hozircha hech qanday natija yo'q.")
    return

  bot.send_message(message.chat.id, "📄 Rasch modeli PDF hisoboti tayyorlanmoqda...")
  pdf_buffer = generate_pdf_report(submissions)

  bot.send_document(
      message.chat.id,
      document=("rasch_test_natijalari.pdf", pdf_buffer, "application/pdf"),
      caption="📊 **Rasch Modeli Bo'yicha Test Natijalari**",
  )


@bot.message_handler(commands=["stop"])
def stop_test_handler(message):
  if message.from_user.id != ADMIN_ID:
    return
  data = load_data()
  data["is_active"] = False
  save_data(data)
  bot.reply_to(message, "🔴 **Test qabul qilish to'xtatildi!**")


@bot.message_handler(commands=["start_test"])
def start_test_handler(message):
  if message.from_user.id != ADMIN_ID:
    return
  data = load_data()
  data["is_active"] = True
  save_data(data)
  bot.reply_to(message, "🟢 **Test qabul qilish qayta yoqildi!**")


@bot.message_handler(commands=["start"])
def start_handler(message):
  welcome_text = (
      f"Assalomu alaykum, **{message.from_user.first_name}**!\n\n"
      "Tizimdan foydalanish uchun, iltimos, to'liq **Ismingiz va Familiyangizni** kiriting (masalan: *Ali Valiyev*):"
  )
  bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown")


@bot.message_handler(func=lambda message: True)
def process_message(message):
  data = load_data()

  if not data.get("is_active", True) and message.from_user.id != ADMIN_ID:
    bot.reply_to(
        message,
        "⛔ **Test qabul qilish vaqtincha to'xtatilgan.**\nIltimos, keyinroq"
        " harakat qilib ko'ring.",
    )
    return

  user_input = message.text.strip()
  user_id = str(message.from_user.id)

  if "users" not in data:
    data["users"] = {}
  if "tokens" not in data:
    data["tokens"] = {}
  if "user_submissions" not in data:
    data["user_submissions"] = {}

  user_data = data["users"].get(user_id, {})

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
            "`1-A 2-B ... 36-JAVOB ... 45-JAVOB`",
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

  user_answers = parse_user_answers(user_input)

  if not user_answers:
    bot.reply_to(
        message,
        "⚠️ **Javoblar formati aniqlanmadi.**\n\n"
        "Javoblarni quyidagicha formatda yuboring:\n"
        "`1-A 2-B 3-C ... 36-JAVOB`",
        parse_mode="Markdown",
    )
    return

  correct_count, total_questions, theta, rasch_score = calculate_rasch_score(
      user_answers
  )

  data["user_submissions"][user_id] = {
      "full_name": user_data.get("full_name"),
      "score": f"{correct_count}/{total_questions}",
      "rasch_theta": theta,
      "rasch_score": rasch_score,
      "answers": user_answers,
  }
  save_data(data)

  bot.reply_to(
      message,
      f"📊 **{user_data.get('full_name')}**, sizning natijangiz:\n\n"
      f"• To'g'ri javoblar: **{correct_count} / {total_questions}**\n"
      f"• Rasch Modeli Balli: **{rasch_score} / 100** (θ = {theta})\n\n"
      "Javoblaringiz muvaffaqiyatli qabul qilindi!",
      parse_mode="Markdown",
  )


if __name__ == "__main__":
  logging.info("Bot ishga tushdi...")
  try:
    bot.remove_webhook()
  except Exception:
    pass
  bot.infinity_polling(skip_pending=True)
