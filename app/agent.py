import time
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from app.database import get_db_schema, execute_sql_query
from app.config import GOOGLE_API_KEY


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    google_api_key=GOOGLE_API_KEY, 
    temperature=0
)

def run_ai_agent(user_input: dict) -> dict:
    text = user_input["text"]
    logs = {}
    
    # ---- 1. CLASSIFY BOSQICHI (Universal holatga keltirildi) ----
    start_time = time.time()
    classify_prompt = ChatPromptTemplate.from_template(
        "Foydalanuvchi so'rovini faqat bitta so'z bilan klassifikatsiya qiling: "
        "Agar so'rov do'kondagi maxsulotlar (moshina, telefon, smartfon, ekskavator, kran, og'ir texnika) haqida ma'lumot qidirish, "
        "narx bilish yoki ijara haqida bo'lsa 'db' deb javob bering. "
        "Agar oddiy salom-alik, rahmat aytish yoki umumiy suhbat bo'lsa 'chat' deb javob bering.\nSo'rov: {text}"
    )
    # TO'G'RILANDI: .format_messages() ishlatildi
    category_messages = classify_prompt.format_messages(text=text)
    category = llm.invoke(category_messages).content.strip().lower()
    logs["classify_time"] = round(time.time() - start_time, 4)
    
    if "chat" in category:
        start_time = time.time()
        chat_prompt = ChatPromptTemplate.from_template("Siz avtosalon, smartfonlar va texnika do'koni yordamchisiz. Suhbatni chiroyli davom ettiring: {text}")
        
        # TO'G'RILANDI: .format_messages() ishlatildi
        chat_messages = chat_prompt.format_messages(text=text)
        response = llm.invoke(chat_messages).content
        logs["generate_answer_time"] = round(time.time() - start_time, 4)
        return {"category": "chat", "result": response, "logs": logs}

    # ---- 2. DDL -> QUERY GENERATION BOSQICHI (O'z holatida, to'g'ri yozilgan) ----
    start_time = time.time()
    db_schema = get_db_schema()
    sql_prompt = ChatPromptTemplate.from_template(
        "Siz PostgreSQL ekspertisiz. Berilgan jadval sxemasidan foydalanib, foydalanuvchi savoliga mos faqat bitta SQL so'rovini yozing. "
        "Hech qanday markdown (```sql) belgilari qo'shmang, faqat toza SQL kodini qaytaring.\n\n"
        "Sxema:\n{schema}\n\nSavol: {text}"
    )
    formatted_messages = sql_prompt.format_messages(schema=db_schema, text=text)
    sql_query = llm.invoke(formatted_messages).content.strip()
    
    # AI yozgan SQL kodini VS Code terminalida kuzatish uchun print:
    print("\n--- AI GENERATED SQL ---")
    print(sql_query)
    print("------------------------\n")
    
    logs["sql_generation_time"] = round(time.time() - start_time, 4)

    # ---- 3. EXECUTE SQL BOSQICHI ----
    start_time = time.time()
    db_result = execute_sql_query(sql_query)
    logs["db_execution_time"] = round(time.time() - start_time, 4)

    # ---- 4. GENERATE ANSWER BOSQICHI (Universal yordamchiga aylantirildi) ----
    start_time = time.time()
    final_prompt = ChatPromptTemplate.from_template(
        "Siz do'kon va og'ir texnika ijarasi markazi yordamchisiz. Foydalanuvchi savoliga ma'lumotlar bazasidan "
        "olingan natija (agar xatolik bo'lsa xatolik matni) asosida tushunarli va chiroyli o'zbek tilida javob yozing.\n"
        "Savol: {text}\n"
        "SQL Natijasi: {result}"
    )
    # TO'G'RILANDI: .format_messages() ishlatildi
    final_messages = final_prompt.format_messages(text=text, result=db_result)
    final_answer = llm.invoke(final_messages).content
    logs["generate_answer_time"] = round(time.time() - start_time, 4)

    return {
        "category": "db",
        "generated_sql": sql_query,
        "db_raw_result": db_result,
        "result": final_answer,
        "logs": logs
    }