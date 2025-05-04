# --- IMPORTS ---
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import uuid
import os
from fastapi.responses import JSONResponse
import psycopg2
from psycopg2.extras import RealDictCursor

# --- CONFIGURAÇÕES INICIAIS ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- CONEXÃO COM O BANCO DE DADOS ---
DB_CONFIG = {
    'dbname': 'furiosos',
    'user': 'postgres',
    'password': '2108',
    'host': 'localhost',
    'port': 5432
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

# --- MODELOS ---
class UserProfile(BaseModel):
    name: str
    cpf: str
    address: str
    birthdate: date
    interests: List[str]
    recent_activities: List[str]
    esports_events: List[str]
    purchases: List[str]
    social_links: List[str]

# --- ROTAS EXISTENTES (submit, upload, social, dashboard) ---

@app.post("/submit-profile")
async def submit_profile(profile: UserProfile):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (name, cpf, address, birthdate, interests, activities, events, purchases, social_links)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        profile.name,
        profile.cpf,
        profile.address,
        profile.birthdate,
        profile.interests,
        profile.recent_activities,
        profile.esports_events,
        profile.purchases,
        profile.social_links
    ))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Profile submitted successfully"}

@app.post("/upload-document")
async def upload_document(file: UploadFile = File(...), user_id: Optional[int] = Form(None)):
    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"message": "File uploaded", "filename": filename, "user_id": user_id}

@app.post("/analyze-social")
async def analyze_social_links(user_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT social_links FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if not user:
        return {"error": "Usuário não encontrado"}

    relevant_links = [link for link in user['social_links'] if "furia" in link.lower() or "esports" in link.lower()]
    return {"relevant_links": relevant_links, "total_links": len(user['social_links'])}

# --- NOVA ROTA DASHBOARD ATUALIZADA ---
from datetime import date

def calculate_age(birthdate):
    today = date.today()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

@app.get("/dashboard")
async def dashboard():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, cpf, birthdate, interests, social_links FROM users ORDER BY id DESC LIMIT 10")
    users = cur.fetchall()
    cur.close()
    conn.close()

    for user in users:
        user["interests"] = user.get("interests", [])
        user["social_links"] = user.get("social_links", [])
        user["email"] = "-"  # pode ser substituído futuramente
        birthdate = user.get("birthdate")
        user["age"] = calculate_age(birthdate) if birthdate else None  # idade calculada

    return JSONResponse(content=users)

# --- EXECUÇÃO ---
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
