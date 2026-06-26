# Marketplace AI Agent

An intelligent sales assistant that answers user questions about cars, smartphones, and construction machinery by querying a real PostgreSQL database — powered by Google Gemini and LangChain.

---

## What Does the Agent Do?

The user asks a question in plain Uzbek. The agent processes it in **4 steps**:

```
User Question
      │
      ▼
┌─────────────────┐
│  1. CLASSIFY    │  → Is this a database question or just a chat?
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
   "db"     "chat"
    │         │
    ▼         ▼
┌────────┐  ┌──────────────────┐
│2. SQL  │  │  Conversational  │
│  GEN   │  │  reply via LLM   │
└───┬────┘  └──────────────────┘
    │
    ▼
┌────────────┐
│ 3. EXECUTE │  → Runs the SQL against PostgreSQL
└─────┬──────┘
      │
      ▼
┌──────────────┐
│ 4. GENERATE  │  → Returns a friendly Uzbek-language answer
│   ANSWER     │
└──────────────┘
```

### Real Example

**Question:** `"BYD Song Plus ning narxi qancha?"` *(What is the price of BYD Song Plus?)*

**What happens inside the agent:**
1. Classifies the question as `"db"`
2. AI generates SQL: `SELECT price FROM cars WHERE brand='BYD' AND model='Song Plus';`
3. Fetches the result from PostgreSQL
4. Returns a human-readable answer: *"BYD Song Plus costs $35,000."*

---

## Database

The agent works with 3 tables:

| Table | Contents |
|-------|----------|
| `cars` | Passenger cars (Chevrolet, BYD, Kia, ...) |
| `phones` | Smartphones (Apple, Samsung, Xiaomi, ...) |
| `construction_machinery` | Excavators, cranes, bulldozers, and other heavy equipment |

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| **FastAPI** | REST API server |
| **Google Gemini 2.5 Flash** | AI model — classification, SQL generation, answer generation |
| **LangChain** | Prompt chain management |
| **PostgreSQL** | Product database |
| **psycopg2** | Python–PostgreSQL connector |

---

## Why an Agent?

A regular chatbot only returns pre-written answers. **An agent:**

- **Understands** the question and **decides on its own** what action to take
- **Writes SQL by itself** — no need for a developer to hardcode queries for every possible question
- Answers from **real, live data** in the database
- Handles **3 different product categories** (cars, phones, heavy machinery) in one system
- **Distinguishes** between casual conversation and data queries

---

## Why Is It Useful?

### For Business
- Customers get answers **24/7** — no sales manager required
- Adding new products needs no code change — just insert a row in the database
- Small teams can manage a large catalog with **a single agent**

### Technically
- Every step's execution time is **logged** (easy to debug and optimize)
- Prompts can be **updated without touching the core logic**
- Adding a new product category only requires updating the database schema description

---

## Setup & Run

```bash
# 1. Clone the repository
git clone https://github.com/Quvonchbek21/agent.git
cd agent

# 2. Create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create a .env file with your credentials
# GOOGLE_API_KEY=your_google_api_key_here
# DATABASE_URL=postgresql://user:password@localhost:5432/marketplace

# 5. Start the server
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

---

## API Usage

**Endpoint:** `POST /ask`

```json
// Request
{
  "text": "Ekskavator ijarasi kuniga qancha turadi?"
}

// Response
{
  "category": "db",
  "generated_sql": "SELECT type, brand, model, price_per_day FROM construction_machinery WHERE type='Ekskavator';",
  "result": "Available excavators start at $250 per day...",
  "logs": {
    "classify_time": 0.45,
    "sql_generation_time": 0.82,
    "db_execution_time": 0.03,
    "generate_answer_time": 0.91,
    "total_time": 2.21
  }
}
```

Interactive API docs available at: `http://localhost:8000/docs`

---

## Project Structure

```
marketplace_agent/
├── app/
│   ├── main.py        # FastAPI server and endpoint
│   ├── agent.py       # Core agent logic (4 steps)
│   ├── database.py    # PostgreSQL connection and SQL execution
│   └── config.py      # Environment variables
├── requirements.txt
├── .gitignore
└── README.md
```
