# Marketplace AI Agent

O'zbek tilida ishlaydigan aqlli savdo yordamchisi — avtomobillar, smartfonlar va qurilish texnikasi bo'yicha foydalanuvchi savollariga real ma'lumotlar bazasidan javob beradi.

---

## Agent nima qiladi?

Foydalanuvchi oddiy o'zbek tilidagi savol yozadi. Agent uni **4 bosqichda** qayta ishlaydi:

```
Foydalanuvchi savoli
       │
       ▼
┌─────────────────┐
│  1. CLASSIFY    │  → Savol ma'lumotlar bazasiga tegishlimi yoki oddiy suhbatmi?
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
  "db"      "chat"
    │         │
    ▼         ▼
┌────────┐  ┌──────────────────┐
│2. SQL  │  │ Suhbat javobi    │
│GENERA- │  │ (LLM orqali)     │
│ TION   │  └──────────────────┘
└───┬────┘
    │
    ▼
┌────────────┐
│ 3. EXECUTE │  → PostgreSQL bazasida SQL so'rovini bajaradi
└─────┬──────┘
      │
      ▼
┌──────────────┐
│ 4. GENERATE  │  → Natijani o'zbek tilida chiroyli tushuntiradi
│   ANSWER     │
└──────────────┘
```

### Amaliy misol

**Savol:** `"BYD Song Plus ning narxi qancha?"`

**Agent ichida nima bo'ladi:**
1. Savolni `"db"` deb tasniflaydi
2. AI o'zi SQL yozadi: `SELECT price FROM cars WHERE brand='BYD' AND model='Song Plus';`
3. PostgreSQL bazasidan natija oladi
4. O'zbek tilida javob beradi: *"BYD Song Plus narxi 35,000 dollar."*

---

## Ma'lumotlar bazasi

Agent 3 ta jadval bilan ishlaydi:

| Jadval | Nima saqlaydi |
|--------|---------------|
| `cars` | Yengil avtomobillar (Chevrolet, BYD, Kia...) |
| `phones` | Smartfonlar (Apple, Samsung, Xiaomi...) |
| `construction_machinery` | Ekskavator, Kran, Buldozer va boshqa og'ir texnika |

---

## Texnologiyalar

| Texnologiya | Maqsadi |
|-------------|---------|
| **FastAPI** | REST API server |
| **Google Gemini 2.5 Flash** | AI modeli (tasniflash, SQL yozish, javob generatsiya) |
| **LangChain** | AI prompt zanjirlarini boshqarish |
| **PostgreSQL** | Mahsulotlar ma'lumotlar bazasi |
| **psycopg2** | Python–PostgreSQL ulanishi |

---

## Nima uchun Agent?

Oddiy chatbot faqat yodlangan javoblarni qaytaradi. **Agent esa:**

- Savolni **o'zi tahlil qiladi** va qanday harakat qilishini **o'zi hal qiladi**
- Ma'lumotlar bazasiga **o'zi SQL yozadi** — dasturchi har bir savol uchun kod yozishi shart emas
- Bazadagi **real, yangilangan ma'lumotlardan** javob beradi
- Bir vaqtning o'zida **3 xil toifadagi** mahsulot (moshina, telefon, texnika) bo'yicha ishlaydi
- Oddiy suhbat va murakkab so'rovlarni **farqlay oladi**

---

## Nima uchun foydali?

### Biznes uchun
- Mijozlar **24/7** savollarga javob oladi — menejer kerak emas
- Har bir yangi mahsulot qo'shilganda kod o'zgartirish shart emas, faqat bazaga qo'shiladi
- Kichik jamoalar katta katalogni **bitta agent** orqali boshqaradi

### Texnik jihatdan
- Har bir bosqichning vaqti **logga yoziladi** (debug uchun qulay)
- LangChain yordamida promptlarni **osonlikcha o'zgartirish** mumkin
- Yangi jadval yoki toifa qo'shish uchun faqat sxemani yangilash kifoya

---

## O'rnatish va ishga tushirish

```bash
# 1. Repozitoriyani klonlash
git clone https://github.com/Quvonchbek21/agent.git
cd agent

# 2. Virtual muhit
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

# 3. Kutubxonalarni o'rnatish
pip install -r requirements.txt

# 4. .env faylini yaratish
# .env fayliga quyidagilarni yozing:
# GOOGLE_API_KEY=your_google_api_key_here
# DATABASE_URL=postgresql://user:password@localhost:5432/marketplace

# 5. Serverni ishga tushirish
uvicorn app.main:app --reload
```

API `http://localhost:8000` manzilida ishlaydi.

---

## API Ishlatish

**Endpoint:** `POST /ask`

```json
// So'rov
{
  "text": "Ekskavator ijarasi kuniga qancha turadi?"
}

// Javob
{
  "category": "db",
  "generated_sql": "SELECT type, brand, model, price_per_day FROM construction_machinery WHERE type='Ekskavator';",
  "result": "Bo'sh ekskavatorlar kunlik ijarasi 250 dollardan boshlanadi...",
  "logs": {
    "classify_time": 0.45,
    "sql_generation_time": 0.82,
    "db_execution_time": 0.03,
    "generate_answer_time": 0.91,
    "total_time": 2.21
  }
}
```

Interaktiv API hujjatlari: `http://localhost:8000/docs`

---

## Loyiha tuzilmasi

```
marketplace_agent/
├── app/
│   ├── main.py        # FastAPI server va endpoint
│   ├── agent.py       # AI agentning asosiy mantiqi (4 bosqich)
│   ├── database.py    # PostgreSQL ulanish va SQL bajarish
│   └── config.py      # Muhit o'zgaruvchilari
├── requirements.txt
├── .gitignore
└── README.md
```
