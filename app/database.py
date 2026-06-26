import psycopg2
from psycopg2.extras import RealDictCursor
from app.config import DATABASE_URL

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def get_db_schema():
    """
    AI Agent ma'lumotlar bazasidagi barcha jadvallarni, ularning ustunlarini va 
    o'zaro bog'lanishlarini aniq tushunishi uchun DDL va biznes mantiqi sxemasi.
    """
    schema_info = """
    Jadval 1: cars (Yengil moshinalar ro'yxati)
    Ustunlar:
    - id: SERIAL PRIMARY KEY (Moshina ID raqami)
    - brand: VARCHAR (Brend nomi, masalan: Chevrolet, BYD, Kia)
    - model: VARCHAR (Model nomi, masalan: Malibu, Song Plus, K5)
    - year: INT (Ishlab chiqarilgan yili)
    - price: DECIMAL (Moshina narxi dollarda)
    - status: VARCHAR (Holati: 'sotuvda' yoki 'sotilgan')

    Jadval 2: phones (Smartfonlar do'koni ro'yxati)
    Ustunlar:
    - id: SERIAL PRIMARY KEY (Telefon ID raqami)
    - brand: VARCHAR (Brend nomi, masalan: Apple, Samsung, Xiaomi, Google)
    - model: VARCHAR (Model nomi, masalan: iPhone 15 Pro, Galaxy S24, Redmi Note 13)
    - storage_gb: INT (Xotira hajmi gigabaytda, masalan: 128, 256, 512)
    - color: VARCHAR (Rangi, masalan: Qora, Oq, Tabiiy Titan)
    - price: DECIMAL (Telefon narxi dollarda)
    - stock_quantity: INT (Do'konda yoki omborda qolgan soni)
    - status: VARCHAR (Holati: 'bor' yoki 'tugagan')

    Jadval 3: construction_machinery (Qurilish texnikalari va og'ir mashinalar)
    Ustunlar:
    - id: SERIAL PRIMARY KEY (Texnika ID raqami)
    - type: VARCHAR (Texnika turi, masalan: Ekskavator, Avtokran, Buldozer, Samosval, Pogruzchik, Katok)
    - brand: VARCHAR (Brend nomi, masalan: CAT, Komatsu, XCMG, Shacman, Howo)
    - model: VARCHAR (Model nomi, masalan: 320 GX, X3000, SD16)
    - capacity_ton: DECIMAL (Yuk ko'tarish quvvati tonnada - Avtokran, Samosval va Buldozerlar uchun)
    - bucket_capacity_m3: DECIMAL (Paqir/Chelak hajmi kub metrda - Ekskavator va Pogruzchiklar uchun)
    - year: INT (Ishlab chiqarilgan yili)
    - price_per_day: DECIMAL (Kunlik ijara narxi dollarda)
    - price_sale: DECIMAL (Sotilish narxi dollarda)
    - status: VARCHAR (Holati: 'bo'sh', 'ishda' yoki 'sotilgan')
    
    Qoidalar:
    - Agar foydalanuvchi qurilish texnikasini ijaraga olish haqida so'rasa, 'price_per_day' ustunidan foydalaning.
    - Agar qurilish texnikasini sotib olish haqida so'rasa, 'price_sale' ustunidan foydalaning.
    - So'rov matniga qarab tegishli jadvalni (cars, phones yoki construction_machinery) aniqlab, faqat kerakli jadvalga SQL yozing.
    """
    return schema_info.strip()

def execute_sql_query(query: str):
    """AI yozgan SQL kodni bazada xavfsiz bajaradi"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
    except Exception as e:
        return f"Xatolik yuz berdi: {str(e)}"
    finally:
        conn.close()