import os
import threading
from datetime import datetime
from flask import Flask
import telebot
from telebot import types
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# BOT VA ADMIN SOZLAMALARI
BOT_TOKEN = "7449551322:AAEq_mN6k9-V3L4YmZfX2-0q1XN4b8v6X9Y"
ADMIN_ID = 5541785551

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

USER_DATA = {}
# Tokenlar bazasi
ACTIVE_TOKENS = {
    "A7B9kL2pQ5xV1mR8", "w3N6zT9jH4fS7dK2", "m5Y2vC8xQ1nR9bL4", 
    "k9P4fJ7sD2hV5xN3", "r1X6tM3qL8pZ2vH9", "v4B8nK1sF7jP3mQ5", 
    "z2D7hG4rX9tL6bN8", "q5J3mV1pN8kS2fH7", "c9N2lD6xR4vP7kQ1", "b4H7fQ9jT2sL5nM3"
}
EXAM_ACTIVE = True

CORRECT_ANSWERS = {
    "1": "D", "2": "A", "3": "A", "4": "A", "5": "B", "7": "D", "8": "B", "9": "D", "10": "B",
    "11": "A", "12": "B", "13": "D", "14": "A", "15": "C", "16": "B", "17": "C", "18": "C", "19": "A", "20": "A",
    "21": "C", "23": "C", "24": "C", "25": "B", "27": "A", "28": "C", "29": "A", "30": "C", "31": "B", "32": "A",
    "33": "F", "34": "E", "35": "D",
    "36": "a) 80 mu, b) 6 sotix",
    "37": "a) Italiya fashistik partiyasi, b) Milan",
    "38": "a) 19 ta, b) 10%",
    "39": "a) 143-a'zosi, b) Si Szinpin",
    "40": "a) Mihail Romanov va Nikolay II, b) Pyotr I",
    "41": "a) Iosip Broz Tito",
    "42": "a) Marg'ilon, b) Oila muhiti va akasi Oxunjon",
    "43": "a) Mirkomilboy, b) Turkiya",
    "44": "a) Jimmi Karter, b) Eron islom inqilobi",
    "45": "a) Afrasiyob, b) Varaxsha va Paykend"
}
# ==========================================
# 2. BOT VA FLASK LOGIKASI
# ==========================================
@app.route('/')
def home():
    return "Bot status: Running!"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    if chat_id == ADMIN_ID:
        bot.send_message(chat_id, "Admin, testni yakunlash uchun /yakunlash yuboring.")
        return
    USER_DATA[chat_id] = {"step": "name", "name": None, "answers": None}
    bot.send_message(chat_id, "Ism va familiyangizni kiriting:")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    chat_id = message.chat.id
    text = message.text.strip()

    if chat_id == ADMIN_ID and text == "/yakunlash":
        handle_yakunlash_start(message)
        return
    
    if chat_id not in USER_DATA: return
    
    user = USER_DATA[chat_id]
    
    if user["step"] == "name":
        user["name"] = text
        user["step"] = "token"
        bot.send_message(chat_id, "Tokeningizni kiriting:")
        
    elif user["step"] == "token":
        if text in ACTIVE_TOKENS:
            ACTIVE_TOKENS.remove(text)
            user["step"] = "answers"
            bot.send_message(chat_id, "Token to'g'ri! Endi javoblaringizni yuboring (masalan: 1-A, 2-B...):")
        else:
            bot.send_message(chat_id, "Noto'g'ri yoki ishlatilgan token! Qaytadan urinib ko'ring.")
            
    elif user["step"] == "answers":
        user["answers"] = text
        user["date"] = datetime.now().strftime("%d.%m.%y")
        user["time"] = datetime.now().strftime("%H:%M")
        user["step"] = "done"
        bot.send_message(chat_id, "Javoblaringiz qabul qilindi. Natijalar admin yakunlagandan keyin yuboriladi.")
            # ==========================================
# 3. NATIJALARNI HISOBLASH VA PDF GENERATOR
# ==========================================
def parse_user_answers(raw_text):
    parsed = {}
    lines = raw_text.replace(",", "\n").split("\n")
    for line in lines:
        if "-" in line:
            parts = line.split("-", 1)
            q_num = parts[0].strip()
            q_ans = parts[1].strip().upper()
            parsed[q_num] = q_ans
    return parsed

def get_daraja(percentage):
    if percentage >= 86: return "A+"
    elif percentage >= 70: return "A"
    elif percentage >= 60: return "B+"
    elif percentage >= 50: return "B"
    else: return "C"

def process_results_and_send():
    results_list = []
    for chat_id, data in USER_DATA.items():
        if "answers" not in data: continue
        
        user_answers = parse_user_answers(data["answers"])
        correct_count = sum(1 for q, ans in CORRECT_ANSWERS.items() if user_answers.get(q, "").lower() in ans.lower() or ans.lower() in user_answers.get(q, "").lower())
        
        total = len(CORRECT_ANSWERS)
        foiz = round((correct_count / total) * 100, 2)
        ball = round(foiz * 0.86, 2)
        
        results_list.append({
            "chat_id": chat_id, "name": data["name"], "score": correct_count,
            "ball": ball, "foiz": f"{foiz}%", "daraja": get_daraja(foiz),
            "date": data["date"], "time": data["time"]
        })
    
    results_list.sort(key=lambda x: x["ball"], reverse=True)
    create_pdf(results_list)
    # ==========================================
# 4. PDF GENERATOR, YUBORISH VA START
# ==========================================
def create_pdf(results_list):
    pdf_filename = "Natijalar.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    
    elements = [Paragraph("<b>Tarix Sertifikat Test Natijalari</b>", styles['Heading1']), Spacer(1, 10)]
    
    table_data = [["№", "Ism-familiya", "Ball", "Foiz", "To'g'ri", "Daraja", "Sana", "Vaqt"]]
    for idx, res in enumerate(results_list, start=1):
        table_data.append([str(idx), res["name"], str(res["ball"]), res["foiz"], str(res["score"]), res["daraja"], res["date"], res["time"]])
    
    t = Table(table_data, colWidths=[30, 150, 40, 50, 40, 40, 60, 50])
    elements.append(t)
    doc.build(elements)
    
    with open(pdf_filename, 'rb') as pdf:
        bot.send_document(ADMIN_ID, pdf, caption="📊 Yakuniy natijalar jadvali.")
        for res in results_list:
            pdf.seek(0)
            try:
                bot.send_document(res["chat_id"], pdf, caption=f"📢 Natijangiz: {res['ball']} ball.")
            except: pass
    if os.path.exists(pdf_filename): os.remove(pdf_filename)

def handle_yakunlash_start(message):
    global EXAM_ACTIVE
    EXAM_ACTIVE = False
    process_results_and_send()

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    print("Bot ishga tushdi...")
    bot.infinity_polling()
