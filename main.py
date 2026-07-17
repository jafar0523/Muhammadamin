import telebot
from telebot import types
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import os

# Botingiz tokensini shu yerga qo'ying
TOKEN = "8851034305:AAFEJS-F8FZBkjYFW3KTAPNPy1Remd5boOo"
bot = telebot.TeleBot(TOKEN)

# 1. RENDER PORT XATOLIGINI TUZATISH UCHUN SEXTA WEB-SERVER
class DummyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Bot is running...")

def run_web_server():
    # Render o'zi avtomatik taqdim etadigan portni olamiz, topilmasa 10000 ni ishlatamiz
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), DummyServer)
    print(f"Web server started on port {port}")
    server.serve_forever()

# Web-serverni alohida oqimda (thread) ishga tushiramiz, u botning ishlashiga xalaqit bermaydi
threading.Thread(target=run_web_server, daemon=True).start()


# 45 talik Milliy sertifikat darajasidagi Tarix testi bazasi
SAVOLLAR = {
    # 1-BLOK (1-10)
    1: {"tur": "variant", "savol": "1-savol: Qadimgi Baqtriya davlati hududida olib borilgan arxeologik qazishmalar davomida topilgan, ilk shaharsozlik madaniyatiga oid bo'lgan eng qadimgi yodgorlikni aniqlang.", "variantlar": ["Qo'ziqiriq", "Jonbozqal'a", "Sapallitepa", "Afrosiyob"], "javob": "Sapallitepa"},
    2: {"tur": "variant", "savol": "2-savol: Miloddan avvalgi V asrda Afinada demokratik islohotlarni yanada mustahkamlab, xalq majlisining rolini oshirgan va strateg lavozimida uzoq muddat faoliyat yuritgan davlat arbobini ko'rsating.", "variantlar": ["Solon", "Perikl", "Klisfen", "Pisistrat"], "javob": "Perikl"},
    3: {"tur": "variant", "savol": "3-savol: VI-VIII asrlarda O'rta Osiyo hududida pul muomalasi tizimida keng qo'llanilgan, sug'diy yozuvli va o'rtasi teshik mis tangalar asosan qaysi davlat boshqaruvi an'analariga taqlidan zarb qilingan?", "variantlar": ["Sosoniylar imperiyasi", "Xitoy (Tan sulolasi)", "Kushon qirolligi", "Vizantiya imperiyasi"], "javob": "Xitoy (Tan sulolasi)"},
    4: {"tur": "variant", "savol": "4-savol: 1215-yilda Angliyada qabul qilingan va qirol hokimiyatini qonun yo'li bilan cheklab, fuqarolarning shaxsiy huquqlarini himoya qilishga zamin yaratgan hujjat qanday nomlanadi?", "variantlar": ["Huquqlar to'g'risidagi bill", "Buyuk erkinliklar xartiyasi (Magna Carta)", "Klarendon konstitutsiyalari", "To'rt modda shartnomasi"], "javob": "Buyuk erkinliklar xartiyasi (Magna Carta)"},
    5: {"tur": "variant", "savol": "5-savol: Amir Temur harbiy yurishlari davomida raqiblariga nisbatan qo'llagan, qo'shinni jang maydonida markaz (qalb), o'ng qanot (maymana), chap qanot (maysara) va kanbullardan tashqari alohida 'g'ul' (gvardiya) sifatida bo'lish taktikasi qaysi jangda unga to'liq g'alaba keltirgan?", "variantlar": ["Loy jangi (1365-y)", "Terek daryosi bo'yidagi jang (1395-y)", "Anqara jangi (1402-y)", "Qunduzcha jangi (1391-y)"], "javob": "Qunduzcha jangi (1391-y)"},
    6: {"tur": "variant", "savol": "6-savol: 1789-yilgi Buyuk Fransiya inqilobi davrida qabul qilingan, 'Barcha insonlar erkin va teng huquqli bo'lib tug'iladilar' degan g'oyani ilgari surgan tarixiy hujjatni belgilang.", "variantlar": ["Mustaqillik deklaratsiyasi", "Inson va fuqaro huquqlari deklaratsiyasi", "Konvent dekreti", "Napoleon kodeksi"], "javob": "Inson va fuqaro huquqlari deklaratsiyasi"},
    7: {"tur": "variant", "savol": "7-savol: XVIII asrning ikkinchi yarmida Buxoro amirligida mang'itlar sulolasi hukronligini rasman boshlab bergan va davlat boshqaruvida markazlashtirish siyosatini olib borgan hukmdorni aniqlang.", "variantlar": ["Muhammad Rahimbiyliy", "Amir Shohmurod", "Amir Haydar", "Doniyorbiyliy"], "javob": "Muhammad Rahimbiyliy"},
    8: {"tur": "variant", "savol": "8-savol: 1919-yilda Birinchi jahon urushi yakunlari bo'yicha tuzilgan va dunyoning yeni siyosiy xaritasi hamda xalqaro munosabatlar tizimini (Millatlar Ligasini) belgilab bergan shartnoma qaysi?", "variantlar": ["Boston shartnomasi", "Versal sulh shartnomasi", "Vashington bitimi", "Rapallo shartnomasi"], "javob": "Versal sulh shartnomasi"},
    9: {"tur": "variant", "savol": "9-savol: 1867-yilda tuzilgan Turkiston general-gubernatorligining birinchi rahbari bo'lgan va o'lkada qat'iy harbiy-pauza boshqaruv tizimini joriy etgan general kim edi?", "variantlar": ["K.P. fon Kaufmann", "M.G. Chernyayev", "N.A. Ivanov", "A.V. Samsonov"], "javob": "K.P. fon Kaufmann"},
    10: {"tur": "variant", "savol": "10-savol: O'zbekiston Respublikasining 1992-yil 8-dekabrda qabul qilingan Konstitutsiyasida davlat hokimiyatining bo'linish prinsipi qaysi moddada qat'iy belgilab qo'yilgan?", "variantlar": ["5-modda", "11-modda", "7-modda", "15-modda"], "javob": "11-modda"},

    # 2-BLOK (11-20)
    11: {"tur": "variant", "savol": "11-savol: Miloddan avvalgi 529-yilda massagetlar malikasi To'maris va Axamaniylar hukmdori Kir II o'rtasida bo'lib o'tgan tarixiy jang qaysi hudud yoki daryo bo'yida sodir bo'lgan deb taxmin qilinadi?", "variantlar": ["Amudaryo (Oks)", "Sirdaryo (Yaksart)", "Zarafshon (Politemet)", "Murg'ob"], "javob": "Amudaryo (Oks)"},
    12: {"tur": "variant", "savol": "12-savol: Qadimgi Rimda plebeylar va patritsiylar o'rtasidagi uzoq muddatli kurashlar natijasida miloddan avvalgi V asr o'rtalarida qabul qilingan va Rim huquqining asosini tashkil etgan ilk yozma qonunlar majmuasini aniqlang.", "variantlar": ["Xammurapi qonunlari", "12 jadval qonunlari", "Solon qonunlari", "Yustinian kodeksi"], "javob": "12 jadval qonunlari"},
    13: {"tur": "variant", "savol": "13-savol: VI asrning ikkinchi yarmida o'z qudratining cho'qqisiga erishgan va Sosoniylar eroni bilan ittifoqda eftaliylar davlatini tor-mor keltirgan xoqonlikni ko'rsating.", "variantlar": ["G'arbiy Turk xoqonligi", "Uyg'ur xoqonligi", "Turk xoqonligi", "Xazar xoqonligi"], "javob": "Turk xoqonligi"},
    14: {"tur": "variant", "savol": "14-savol: IX-XI asrlarda Yevropada 'Vikinglar davri' nomi bilan mashhur bo'lgan, dengiz orqali bosqinchilik yurishlari uyushtirib, keyinchalik Normandiya gersogligi va Angliyada o'z sulolasini boshlagan shimollik xalqlar qanday atalgan?", "variantlar": ["Normanlar", "Vangallar", "Franklar", "Gotlar"], "javob": "Normanlar"},
    15: {"tur": "variant", "savol": "15-savol: 1221-yilda Xorazmshohlar davlatining poytaxti Gurganj (Ko'hna Urganch) mudofaasiga boshchilik qilgan va mo'g'ullarga qarshi mardona kurashib halok bo'lgan xalq qahramonini belgilang.", "variantlar": ["Temur Malik", "Najmiddin Kubro", "Jaloliddin Manguberdi", "Mahmud Torobiy"], "javob": "Najmiddin Kubro"},
    16: {"tur": "variant", "savol": "16-savol: 1640-1660-yillarda bo'lib o'tgan, qirol hokimiyati va parlament o'rtasidagi ziddiyatlar fuqarolar urushiga aylanib, Yevropada kapitalistik munosabatlarning rivojlanishiga kuchli turtki bergan inqilob qaysi davlatda sodir bo'lgan?", "variantlar": ["Fransiya", "Niderlandiya", "Angliya", "AQSH"], "javob": "Angliya"},
    17: {"tur": "variant", "savol": "17-savol: XIX asrning birinchi yarmida Xiva xonligida markaziy hokimiyatni mustahkamlash, soliq tizimini tartibga solish va pul islohoti o'tkazib, oltin tangalar zarb ettirgan qo'ng'irotlar sulolasi vakilini aniqlang.", "variantlar": ["Eltuzarxon", "Muhammad Rahimxon I", "Olloqulixon", "Sayyid Muhammadxon"], "javob": "Muhammad Rahimxon I"},
    18: {"tur": "variant", "savol": "18-savol: 1945-yil fevral oyida bo'lib o'tgan, unda Ikkinchi jahon urushidan keyingi dunyo tartiboti, Germaniyaning taqdiri va BMTni tuzish masalalari 'Katta uchlik' (Stalin, Ruzvelt, Cherchill) tomonidan hal qilingan konferensiyaniy ko'rsating.", "variantlar": ["Tehron konferensiyasi", "Potsdam konferensiyasi", "Yalta konferensiyasi", "San-Fransisko konferensiyasi"], "javob": "Yalta konferensiyasi"},
    19: {"tur": "variant", "savol": "19-savol: 1916-yilda Turkiston o'lkasida mardikorlikka olish to'g'risidagi podsho farmoniga qarshi bosh ko'targan xalq qo'zg'olonining Jizzaxdagi rahbarlaridan biri kim edi?", "variantlar": ["Polvonniyoz hoji Yusupov", "Nazir xo'ja", "Qurbonjon dodxoh", "Bobo niyat og'li"], "javob": "Nazir xo'ja"},
    20: {"tur": "variant", "savol": "20-savol: O'zbekiston Respublikasi o'z mustaqilligini e'lon qilgandan so'ng, xalqaro hamjamiyatning teng huquqli a'zosiga aylanish yo'lida qaysi sanada Birlashgan Millatlar Tashkilotiga (BMT) rasman a'zo bo'lib qabul qilingan?", "variantlar": ["1991-yil 31-avgust", "1992-yil 2-mart", "1992-yil 8-dekabr", "1993-yil 10-may"], "javob": "1992-yil 2-mart"},

    # 3-BLOK (21-30)
    21: {"tur": "variant", "savol": "21-savol: Miloddan avvalgi IV asrning ikkinchi yarmida Aleksandr Makedonskiy qo'shinlariga qarshi Sug'diyona va Baqtriya hududida uch yil davomida (m.av. 329–327-yy.) partizanlik urushini olib borgan mard sarkardani aniqlang.", "variantlar": ["Spitamen", "Oksart", "batan", "To'maris"], "javob": "Spitamen"},
    22: {"tur": "variant", "savol": "22-savol: Miloddan avvalgi III asrda Qadimgi Rim va Karfagen davlatlari o'rtasida O'rta yer dengizida hukmronlik qilish uchun boshlanib, uch bosqichda davom etgan va Karfagenning butkul vayron bo'lishi bilan yakunlangan urushlar qanday nomlanadi?", "variantlar": ["Midiya urushlari", "Puni urushlari", "Peloponnes urushlari", "Galliya urushlari"], "javob": "Puni urushlari"},
    23: {"tur": "variant", "savol": "23-savol: Arab xalifaligi davrida (VIII asr boshlari) Movarounnahr hududini bosib olishga boshchilik qilgan va mahalliy hukmdorlar o'rtasidagi parokandalikdan foydalanib, Buxoro, Samarqand va Xorazmni bo'ysundirgan arab sarkardasi kim edi?", "variantlar": ["Qutayba ibn Muslim", "Abu Muslim", "Nasr ibn Sayyor", "Ziyod ibn Solih"], "javob": "Qutayba ibn Muslim"},
    24: {"tur": "variant", "savol": "24-savol: 1453-yilda Usmonli turklar sultonligi tomonidan Konstantinopol shahrining zabt etilishi qaysi buyuk imperiyaning rasman tugatilishiga olib keldi?", "variantlar": ["Muqaddas Rim imperiyasi", "G'arbiy Rim imperiyasi", "Vizantiya imperiyasi", "Franklar qirolligi"], "javob": "Vizantiya imperiyasi"},
    25: {"tur": "variant", "savol": "25-savol: Temuriylar davri madaniy hayotida muhim o'rin tutgan, XV asrda Hirotda o'zining noyob asarlari bilan miniatyura san'atini eng yuksak cho'qqiga olib chiqqan va 'Sharq Rafaeli' deb nom olgan musavvirni ko'rsating.", "variantlar": ["Kamoliddin Behzod", "Mirak Naqqosh", "Sulton Ali Mashhadiy", "Davlatshoh Samarqandiy"], "javob": "Kamoliddin Behzod"},
    26: {"tur": "variant", "savol": "26-savol: 1861-1865-yillarda AQSHda shimoliy va janubiy shtatlar o'rtasidagi fuqarolar urushida qullikni rasman bekor qilish to'g'risidagi deklaratsiyani imzolagan AQSH prezidentini aniqlang.", "variantlar": ["Jorj Vashington", "Tomas Joferson", "Avraam Linkoln", "Teodor Ruzvelt"], "javob": "Avraam Linkoln"},
    27: {"tur": "variant", "savol": "27-savol: 1842-yilda Buxoro amiri Nasrullaxon tomonidan Qo'qon xonligi poytaxtining bosib olinishi va Qo'qon hukmdori Muhammad Alixonning qatl etilishiga mahalliy aholining noroziligi sabab bo'lib, xonlik taxtiga kim o'tqaziladi?", "variantlar": ["Sheralixon", "Xudoyorxon", "Mallaxon", "Olimxon"], "javob": "Sheralixon"},
    28: {"tur": "variant", "savol": "28-savol: 1962-yilda AQSH va SSSR o'rtasida Yamayka yaqinidagi orolda joylashtirilgan yadro raketalari sababli kelib chiqqan va dunyoni uchinchi jahon urushi yoqasiga olib kelgan xalqaro siyosiy inqiroz qanday ataladi?", "variantlar": ["Berlin inqirozi", "Karib inqirozi", "Suvaysh inqirozi", "Koreya urushi"], "javob": "Karib inqirozi"},
    29: {"tur": "variant", "savol": "29-savol: XIX asr oxiri va XX asr boshlarida Turkistonda vujudga kelgan, milliy uyg'onish, maktablarni isloh qilish, gazeta va teatr orqali xalqni ma'rifatli qilishni maqsad qilgan ijtimoiy-siyosiy harakat vakillari qanday nomlangan?", "variantlar": ["Jadidlar", "Qizilboshlilar", "Eshonlar", "Muxtoriyatchilar"], "javob": "Jadidlar"},
    30: {"tur": "variant", "savol": "30-savol: O'zbekiston Respublikasining mustaqillik yillarida qabul qilingan, ta'lim tizimini tubdan isloh qilish va kadrlar tayyorlashning milliy modelini yaratishga qaratilgan eng muhim dasturiy qonun hujjati qaysi?", "variantlar": ["Yoshlarga oid davlat siyosati to'g'risidagi Qonun", "Ta'lim to'g'risidaxi Qonun", "Ma'naviyat va ma'rifat konsepsiyasi", "Innovatsion faoliyat to'g'risidaxi Qonun"], "javob": "Ta'lim to'g'risidaxi Qonun"},

    # 4-BLOK (31-40)
    31: {"tur": "variant", "savol": "31-savol: Milodiy I-IV asrlarda Markaziy Osiyo, Afg'oniston va Shimoliy Hindiston hududlarini birlashtirgan, Kanishka I davrida o'z qudratining cho'qqisiga chiqib, buddizm dinini davlat miqyosida qo'llab-quvvatlagan imperiyani aniqlang.", "variantlar": ["Parfiya qirolligi", "Kushon imperiyasi", "Eftaliylar davlati", "Kangyu davlati"], "javob": "Kushon imperiyasi"},
    32: {"tur": "variant", "savol": "32-savol: Miloddan avvalgi 331-yilda Aleksandr Makedonskiy va Eronda Axamaniylar hukmdori Doro III o'rtasida bo'lib o'tgan, Eron qo'shinlarining mutqlo mag'lubiyati va Axamaniylar imperiyasining parchalanishiga olib kelgan hal qiluvchi jangni ko'rsating.", "variantlar": ["Granik jangi", "Iss jangi", "Gavgamela jangi", "Xeronoya jangi"], "javob": "Gavgamela jangi"},
    33: {"tur": "variant", "savol": "33-savol: IX Asr oxirida Movarounnahrni yagona davlatga birga keltirib, poytaxtni Buxoro shahriga ko'chirgan va somoniylar sulolasining mustaqil davlatiga asos solgan hukmdorni belgilang.", "variantlar": ["Ismoil Somoniy", "Nasr I ibn Ahmad", "Ahmad ibn Asad", "Nuh ibn Mansur"], "javob": "Ismoil Somoniy"},
    34: {"tur": "variant", "savol": "34-savol: XI asr oxirida (1095-yil) Klermon soborida xristian dunyosini muqaddas Quddus (Iyerusalim) shahrini musulmonlardan qaytarib olishga chaqirib, 'Salb yurishlari'ni boshlab bergan Rim papasi kim edi?", "variantlar": ["Urban II", "Innokentiy III", "Grigoriy VII", "Bonifatsiy VIII"], "javob": "Urban II"},
    35: {"tur": "variant", "savol": "35-savol: 1447-1449-yillarda Temuriylar imperiyasini boshqargan, fanda yuksak kashfiyotlar qibly, 'Ziji jadidi Ko'ragoniy' yulduzlar jadvalini yaratgan buyuk astronom-hukmdor kim?", "variantlar": ["Shohruh Mirzo", "Mirzo Ulug'bek", "Sulton Husayn Boyqaro", "Abu Said Mirzo"], "javob": "Mirzo Ulug'bek"},
    36: {"tur": "variant", "savol": "36-savol: XIX asrning ikkinchi yarmida 'Temir kansler' taxallusi bilan mashhur bo'lgan va tarqoq nemis yerlarini 'qon va temir' siyosati orqali yagona Prussiya atrofiga birlashtirib, Germaniya imperiyasini tuzgan davlat arbobini aniqlang.", "variantlar": ["Otto fon Bismark", "Vilgelm I", "Napoleon III", "Klemens fon Metternix"], "javob": "Otto fon Bismark"},
    37: {"tur": "variant", "savol": "37-savol: XIX asr o'rtalarida Qo'qon xonligida ichki nizolar va qipchoqlar ta'siri kuchaygan davrda, taxtga uch marta o'tirgan va Rossiya imperiyasi qo'shinlarining hujumlariga qarshi kurashgan hukmdorni ko'rsating.", "variantlar": ["Xudoyorxon", "Sheralixon", "Po'latxon", "Nasriddinxon"], "javob": "Xudoyorxon"},
    38: {"tur": "variant", "savol": "38-savol: 1939-yil 23-avgustda SSSR va Germaniya o'rtasida imzolangan, o'zaro hujum qilmaslik va Sharqiy Yevropani ta'sir doiralariga bo'lib olishni ko'zda tutgan maxfiy bitim tarixda qanday nom bilan ataladi?", "variantlar": ["Molotov-Ribbentrop pakti", "Myunxen kelishuvi", "Anti-Komintern pakti", "Lokarno shartnomasi"], "javob": "Molotov-Ribbentrop pakti"},
    39: {"tur": "variant", "savol": "39-savol: O'zbekiston SSR hududida 1980-yillarning ikkinchi yarmida Moskva markaziy hukumati tomonidan uyushtirilgan, respublikaning ko'plab rahbarlari va mutaxassislarini asossiz qatag'on qilishga qaratilgan siyosiy kompaniya nima deb atalgan?", "variantlar": ["Paxta ishi", "Katta qatag'on", "Kosmopolitizmga qarshi kurash", "Xalq dushmanlarini tugatish"], "javob": "Paxta ishi"},
    40: {"tur": "variant", "savol": "40-savol: O'zbekiston Respublikasi jahon hamjamiyati bilan iqtisodiy va logistik aloqalarni mustahkamlash maqsadida qaysi yilda qadimiy 'Buyuk Ipak yo'li'ni qayta tiklash ramzi bo'lgan transmilliy 'Asr loyihasi' — Qamchiq dovoni orqali o'tgan Angren-Pop elektrlashtirilgan temir yo'lini rasman ishga tushirdi?", "variantlar": ["2012-yil", "2016-yil", "2018-yil", "2020-yil"], "javob": "2016-yil"},

    # 5-BLOK: YOZMA SAVOLLAR (41-45)
    41: {"tur": "yozma", "savol": "41-savol (Yozma): Qadimgi Bobil davlatining eng mashhur hukmdori, miloddan avvalgi XVIII asrda dunyoda birinchi bo'lib qat'iy va mukammal yozma qonunlar to'plamini tuzdirgan shaxsning ismini yozing.", "javob": "Xammurapi"},
    42: {"tur": "yozma", "savol": "42-savol (Yozma): 1220-yilda Samarqand shahrini mo'g'ullar bosqinidan mardona himoya qilgan, ammo sotqinlik tufayli shahar taslim bo'lgach, o'zining kichik guruhi bilan dushman halqasini yorib chiqib, Sirdaryo bo'yidagi Xujand shahrida mudofaani davom ettirgan Xorazmshohlar sarkardasi kim edi?", "javob": "Temur Malik"},
    43: {"tur": "yozma", "savol": "43-savol (Yozma): 1492-yilda Ispaniya qiroli ko'magida g'arbiy yo'nalish bo'ylab Hindistonga dengiz yo'lini qidirib yo'lga chiqqan va Yevropaliklar uchun mutqlo noma'lum bo'lgan yangi qit'ani (Amerikani) kashf etgan dengiz sayyohining ismini yozing.", "javob": "Xristofor Kolumb"},
    44: {"tur": "yozma", "savol": "44-savol (Yozma): 1898-yilda chor Rossiyasining mustamlakachilik va zulm siyosatiga qarshi Farg'ona vodiysida (Andijonda) bosh ko'targan yirik xalq qo'zg'olonining g'oyaviy rahbari bo'lgan shaxsning ismini yozing.", "javob": "Dukchi Eshon"},
    45: {"tur": "yozma", "savol": "45-savol (Yozma): O'zbekiston Respublikasi o'z mustaqilligining huquqiy asoslarini mustahkamlab, mustaqil ichki va tashqi siyosat yuritish kafolati bo'lgan 'Mustaqillik deklaratsiyasi'ni nechanchi yilning qaysi sanasida (kun va oy, masalan: 20-iyun) qabul qilgan?", "javob": "20-iyun"}
}

USER_TESTS = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    bot.send_message(
        message.chat.id,
        f"Assalomu alaykum, {user_name}! 👋\n\n"
        "Tarix fanidan Milliy sertifikat darajasidagi 45 talik rasmiy test tizimiga xush kelibsiz.\n\n"
        "🔑 Imtihonni faollashtirish va birinchi 10 ta savolni olish uchun maxsus test kodini yuboring:"
    )

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    chat_id = message.chat.id
    text = message.text.strip()

    # 1. TEST KODINI TEKSHIRISH
    if text == "6789002":
        USER_TESTS[chat_id] = {
            "current_q": 1,
            "score": 0,
            "answers": {},
            "paket_limit": 10
        }
        bot.send_message(chat_id, "✅ Imtihon kodi qabul qilindi!\nTarix fanidan 45 talik test boshlanmoqda. Omad tilaymiz! 🚀")
        yuborish_savol(chat_id)
        return

    # 2. YOZMA SAVOLLAR JAVOBLARINI QABUL QILISH
    if chat_id in USER_TESTS:
        status = USER_TESTS[chat_id]
        q_num = status["current_q"]
        
        if q_num <= 45 and SAVOLLAR[q_num]["tur"] == "yozma":
            togri_javob = SAVOLLAR[q_num]["javob"].lower()
            
            if text.lower() in togri_javob or togri_javob in text.lower():
                status["score"] += 1
                status["answers"][q_num] = f"✅ Savol {q_num}: To'g'ri (Siz: {text})"
            else:
                status["answers"][q_num] = f"❌ Savol {q_num}: Noto'g'ri (Siz: {text} | Asli: {SAVOLLAR[q_num]['javob']})"
            
            status["current_q"] += 1
            yuborish_savol(chat_id)
        else:
            bot.send_message(chat_id, "⚠️ Iltimos, savollarga variant tugmalari orqali javob bering.")
    else:
        bot.send_message(chat_id, "❌ Noto'g'ri kod kiritdingiz yoki imtihon faol emas.")

def yuborish_savol(chat_id):
    status = USER_TESTS[chat_id]
    q_num = status["current_q"]

    if q_num > 45:
        yakunlash_test(chat_id)
        return

    # Har 10 ta savoldan keyin to'xtash va tugma chiqarish
    if q_num > status["paket_limit"]:
        st
