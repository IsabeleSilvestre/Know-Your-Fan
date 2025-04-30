# backend/main.py

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import uuid
import os
from fastapi.responses import HTMLResponse

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

# --- DATABASE SETUP ---
import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    'dbname': 'kyf_db',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': 5432
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

# --- SCHEMA MODELS ---
class UserProfile(BaseModel):
    name: str
    cpf: str
    address: str
    interests: List[str]
    recent_activities: List[str]
    esports_events: List[str]
    purchases: List[str]
    social_links: List[str]

# --- ROUTES ---
@app.post("/submit-profile")
async def submit_profile(profile: UserProfile):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (name, cpf, address, interests, activities, events, purchases, social_links)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        profile.name,
        profile.cpf,
        profile.address,
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
    # Aqui entraria integração com API de IA para validação
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

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, cpf, interests, events FROM users ORDER BY id DESC LIMIT 10")
    users = cur.fetchall()
    cur.close()
    conn.close()

    html = """
    <html><head><title>Dashboard KYF</title></head><body>
    <h1>Últimos Perfis Cadastrados</h1>
    <table border='1' cellpadding='5' cellspacing='0'>
        <tr><th>ID</th><th>Nome</th><th>CPF</th><th>Interesses</th><th>Eventos</th></tr>
    """
    for user in users:
        html += f"<tr><td>{user['id']}</td><td>{user['name']}</td><td>{user['cpf']}</td>"
        html += f"<td>{', '.join(user['interests'])}</td><td>{', '.join(user['events'])}</td></tr>"

    html += "</table></body></html>"
    return html

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
