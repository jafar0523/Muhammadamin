import io
import json
import logging
import os
import re

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
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

# To'g'ri javoblar shabloni
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


def get_grade(score):
  if score >= 40:
    return "A+"
  elif score >= 32:
    return "A"
  elif score >= 25:
    return "B+"
  elif score >= 18:
    return "B"
  else:
    return "C"


def load_data():
  if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
    initial_data = {
        "tokens": {
            "TOKEN123": {"used": False},
            "TEST2026": {"used": False},
        },
        "users": {},
        "user_submissions": {},
        "is_active": True,
    }
    save_data(initial_data)
    return initial_data

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
  # Har qanday formatdagi (1-A, 1.A, 1:A, 1 A) javoblarni aniq o'qish uchun regex
  matches = re.findall(
      r"(\d+)[\s\-\:\.\=]+([A-Za-zА-Яа-яO‘o‘O’o’G‘g‘ʻʼ’`]+)", text
  )
  for q_num, ans in matches:
    answers[int(q_num)] = ans.strip().upper()
  return answers


def generate_pdf_report(submissions):
  buffer = io.BytesIO()
  doc = SimpleDocTemplate(
      buffer,
      pagesize=landscape(A4),
      rightMargin=20,
      leftMargin=20,
      topMargin=25,
      bottomMargin=25,
  )
  elements = []

  styles = getSampleStyleSheet()
  title_style = styles["Heading1"]
  title_style.alignment = 1
  title_style.fontSize = 16

  elements.append(Paragraph("<b>TEST NATIJALARI (BALL TIZIMI)</b>", title_style))
  elements.append(Spacer(1, 15))

  sorted_subs = sorted(
      submissions.values(),
      key=lambda x: int(x.get("correct_count", 0)),
      reverse=True,
  )

  table_data = [["№", "Ism Familiya", "To'g'ri javob", "Foiz", "Daraja"]]

  for idx, sub in enumerate(sorted_subs, start=1):
    name = sub.get("full_name", "Noma'lum")
    correct_cnt = int(sub.get("correct_count", 0))
    total_q = len(CORRECT_ANSWERS)
    percentage = f"{(correct_cnt / total_q) * 100:.1f}%"
    score_str = f"{correct_cnt} / {total_q}"
    grade = get_grade(correct_cnt)

    table_data.append([str(idx), name, score_str, percentage, grade])

  table = Table(table_data, colWidths=[40, 300, 100, 100, 100])
  table.setStyle(
      TableStyle([
          ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1A365D")),
          ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
          ("ALIGN", (0, 0), (-1, -1), "CENTER"),
          ("ALIGN", (1, 1), (1, -1), "LEFT"),
          ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
          ("FONTSIZE", (0, 0), (-1, 0), 10),
          ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
          ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F7FAFC")),
          ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E0")),
          ("FONTSIZE", (0, 1), (-1, -1), 9),
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
  text += "• `/stop` - Testni to'xtatish va yakuniy PDF hisobotni olish\n"
  text += "• `/pdf` - Natijalar PDF hisobotini qo'lda olish\n"
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

  bot.send_message(message.chat.id, "📄 PDF hisoboti tayyorlanmoqda...")
  pdf_buffer = generate_pdf_report(submissions)

  bot.send_document(
      message.chat.id,
      document=("test_natijalari.pdf", pdf_buffer, "application/pdf"),
      caption="📊 **Test Natijalari Hisoboti**",
  )


@bot.message_handler(commands=["stop"])
def stop_test_handler(message):
  if message.from_user.id != ADMIN_ID:
    return

  data = load_data()
  data["is_active"] = False
  save_data(data)

  bot.reply_to(
      message,
      "🔴 **Test qabul qilish to'xtatildi!**\nNatijalar hisoboti"
      " tayyorlanmoqda...",
  )

  submissions = data.get("user_submissions", {})
  if submissions:
    pdf_buffer = generate_pdf_report(submissions)
    bot.send_document(
        message.chat.id,
        document=("test_natijalari.pdf", pdf_buffer, "application/pdf"),
        caption=(
            "📊 **Test yakunlandi!** Barcha qatnashchilar natijalari to'liq"
            " PDF hisoboti."
        ),
    )
  else:
    bot.send_message(
        message.chat.id, "⚠️ Hozircha test topshirgan foydalanuvchilar mavjud emas."
    )


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
        "⛔ **Test qabul qilish to'xtatilgan.**\nAdmin testni yakunlagan.",
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
    clean_input = user_input.strip().lower()

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

  # Javoblarni o'qish
  user_answers = parse_user_answers(user_input)

  if not user_answers:
    bot.reply_to(
        message,
        "⚠️ **Javoblar formati aniqlanmadi.**\n\n"
        "Javoblarni quyidagicha formatda yuboring:\n"
        "`1-A 2-B 3-C ... 36-JAVOB`",
    )
    return

  # To'g'ri javoblarni solishtirish
  correct_count = 0
  total_questions = len(CORRECT_ANSWERS)

  for q_num, correct_ans in CORRECT_ANSWERS.items():
    user_ans = user_answers.get(q_num)
    if user_ans and user_ans == str(correct_ans).upper():
      correct_count += 1

  data["user_submissions"][user_id] = {
      "full_name": user_data.get("full_name"),
      "correct_count": correct_count,
      "answers": user_answers,
  }
  save_data(data)

  bot.reply_to(
      message,
      f"📊 **{user_data.get('full_name')}**, javoblaringiz qabul qilindi!\n\n"
      f"• To'g'ri topilganlar: **{correct_count} / {total_questions}**\n\n"
      "Test yakunlangach admin tomonidan to'liq natijalar e'lon qilinadi.",
      parse_mode="Markdown",
  )


if __name__ == "__main__":
  logging.info("Bot ishga tushdi...")
  try:
    bot.remove_webhook()
  except Exception:
    pass
  bot.infinity_polling(skip_pending=True)
