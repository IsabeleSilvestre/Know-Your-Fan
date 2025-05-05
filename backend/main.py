# --- IMPORTS ---
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import uuid
import os
from fastapi.responses import JSONResponse
from supabase import create_client
from datetime import date

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

# --- CONEXÃO COM O SUPABASE ---
SUPABASE_URL = "https://oqtwjbpzhcbzritkcfas.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9xdHdqYnB6aGNienJpdGtjZmFzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDY0MDM1NDUsImV4cCI6MjA2MTk3OTU0NX0.TILghr8HoQufUplJpVDZJVcbTXaUc-0wgdbLM3ykeBk"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

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

# --- FUNÇÕES UTILITÁRIAS ---
def calculate_age(birthdate):
    today = date.today()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

# --- ROTAS ATUALIZADAS ---
@app.post("/submit-profile")
async def submit_profile(profile: UserProfile):
    data = {
        "name": profile.name,
        "cpf": profile.cpf,
        "address": profile.address,
        "birthdate": profile.birthdate.isoformat(),
        "interests": profile.interests,
        "activities": profile.recent_activities,
        "events": profile.esports_events,
        "purchases": profile.purchases,
        "social_links": profile.social_links,
    }
    response = supabase.table("users").insert(data).execute()
    return {"message": "Profile submitted successfully", "data": response.data}

@app.post("/upload-document")
async def upload_document(file: UploadFile = File(...), user_id: Optional[int] = Form(None)):
    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    with open(file_path, "wb") as f:
        f.write(await file.read())

    bucket = "user-documents"
    response = supabase.storage.from_(bucket).upload(filename, file_path)

    return {"message": "File uploaded", "filename": filename, "user_id": user_id, "storage_url": response}

@app.post("/analyze-social")
async def analyze_social_links(user_id: int):
    response = supabase.table("users").select("social_links").eq("id", user_id).execute()
    
    if not response.data:
        return {"error": "Usuário não encontrado"}

    user_social_links = response.data[0].get("social_links", [])
    relevant_links = [link for link in user_social_links if "furia" in link.lower() or "esports" in link.lower()]
    
    return {"relevant_links": relevant_links, "total_links": len(user_social_links)}

@app.get("/dashboard")
async def dashboard():
    response = supabase.table("users").select("id, name, cpf, birthdate, interests, social_links").order("id", desc=True).limit(10).execute()

    users = response.data

    for user in users:
        user["interests"] = user.get("interests", [])
        user["social_links"] = user.get("social_links", [])
        user["email"] = "-"  # Placeholder
        birthdate = user.get("birthdate")
        user["age"] = calculate_age(date.fromisoformat(birthdate)) if birthdate else None

    return JSONResponse(content=users)

# --- EXECUÇÃO ---
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
