from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Cookie, Response, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone, timedelta
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import uuid
import base64
import io
from PIL import Image
import requests
import asyncio
from emergentintegrations.llm.chat import LlmChat, UserMessage, ImageContent
import bcrypt
import secrets

load_dotenv()

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB
mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
database_name = os.getenv("DATABASE_NAME", "apak_fitness")
client = MongoClient(mongo_url)
db = client[database_name]

# Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# ==================== MODELS ====================

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    email: str
    name: str
    picture: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    goal_weight_kg: Optional[float] = None
    activity_level: Optional[str] = None
    daily_calorie_goal: Optional[int] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_deleted: bool = False
    
    class Config:
        populate_by_name = True

class UserSession(BaseModel):
    user_id: str
    session_token: str
    expires_at: datetime
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class OnboardingData(BaseModel):
    age: int
    gender: str
    height_cm: float
    weight_kg: float
    goal_weight_kg: float
    activity_level: str

class FoodLog(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    food_name: str
    portion_size: str
    calories: float
    protein: Optional[float] = 0
    carbs: Optional[float] = 0
    fat: Optional[float] = 0
    image_base64: Optional[str] = None
    logged_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_deleted: bool = False

class TurkishFood(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    calories_per_100g: float
    protein_per_100g: float
    carbs_per_100g: float
    fat_per_100g: float
    category: str

class WorkoutLog(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    exercise_name: str
    duration_minutes: int
    calories_burned: float
    logged_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_deleted: bool = False

class Achievement(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    title: str
    description: str
    icon: str
    earned_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# ==================== AUTHENTICATION ====================

async def get_current_user(session_token: Optional[str] = Cookie(None), authorization: Optional[str] = Header(None)) -> User:
    token = session_token
    if not token and authorization:
        token = authorization.replace("Bearer ", "")
    
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    session = db.user_sessions.find_one({
        "session_token": token,
        "expires_at": {"$gt": datetime.now(timezone.utc)}
    })
    
    if not session:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    
    user_doc = db.users.find_one({"_id": session["user_id"], "is_deleted": False})
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_doc["id"] = user_doc.pop("_id")
    return User(**user_doc)

# ==================== AUTH ENDPOINTS ====================

@app.post("/api/auth/register")
async def register_user(email: str, password: str, name: str, response: Response):
    """Register new user with email and password"""
    # Check if user already exists
    existing_user = db.users.find_one({"email": email, "is_deleted": False})
    if existing_user:
        raise HTTPException(status_code=400, detail="Bu email adresi zaten kayıtlı")
    
    # Hash password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Create user
    user_id = str(uuid.uuid4())
    db.users.insert_one({
        "_id": user_id,
        "email": email,
        "name": name,
        "password_hash": password_hash.decode('utf-8'),
        "picture": None,
        "created_at": datetime.now(timezone.utc),
        "is_deleted": False
    })
    
    # Create session
    session_token = secrets.token_urlsafe(32)
    db.user_sessions.insert_one({
        "user_id": user_id,
        "session_token": session_token,
        "expires_at": datetime.now(timezone.utc) + timedelta(days=7),
        "created_at": datetime.now(timezone.utc)
    })
    
    # Set cookie
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=7 * 24 * 60 * 60,
        path="/"
    )
    
    return {"success": True, "user_id": user_id, "needs_onboarding": True}

@app.post("/api/auth/login")
async def login_user(email: str, password: str, response: Response):
    """Login user with email and password"""
    # Find user
    user = db.users.find_one({"email": email, "is_deleted": False})
    if not user:
        raise HTTPException(status_code=401, detail="Email veya şifre hatalı")
    
    # Check if user has password (not OAuth user)
    if "password_hash" not in user:
        raise HTTPException(status_code=400, detail="Bu hesap Google ile oluşturulmuş. Lütfen Google ile giriş yapın")
    
    # Verify password
    if not bcrypt.checkpw(password.encode('utf-8'), user["password_hash"].encode('utf-8')):
        raise HTTPException(status_code=401, detail="Email veya şifre hatalı")
    
    # Create session
    session_token = secrets.token_urlsafe(32)
    db.user_sessions.insert_one({
        "user_id": user["_id"],
        "session_token": session_token,
        "expires_at": datetime.now(timezone.utc) + timedelta(days=7),
        "created_at": datetime.now(timezone.utc)
    })
    
    # Set cookie
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=7 * 24 * 60 * 60,
        path="/"
    )
    
    needs_onboarding = user.get("age") is None
    
    return {"success": True, "user_id": user["_id"], "needs_onboarding": needs_onboarding}

@app.post("/api/auth/session")
async def create_session(session_id: str, response: Response):
    """Process session_id from Emergent Auth"""
    auth_response = requests.get(
        "https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data",
        headers={"X-Session-ID": session_id}
    )
    
    if auth_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Invalid session ID")
    
    user_data = auth_response.json()
    
    # Check if user exists
    existing_user = db.users.find_one({"email": user_data["email"], "is_deleted": False})
    
    if existing_user:
        user_id = existing_user["_id"]
    else:
        user_id = str(uuid.uuid4())
        db.users.insert_one({
            "_id": user_id,
            "email": user_data["email"],
            "name": user_data["name"],
            "picture": user_data.get("picture"),
            "created_at": datetime.now(timezone.utc),
            "is_deleted": False
        })
    
    # Create session
    session_token = user_data["session_token"]
    db.user_sessions.insert_one({
        "user_id": user_id,
        "session_token": session_token,
        "expires_at": datetime.now(timezone.utc) + timedelta(days=7),
        "created_at": datetime.now(timezone.utc)
    })
    
    # Set cookie
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=7 * 24 * 60 * 60,
        path="/"
    )
    
    return {"success": True, "user_id": user_id, "needs_onboarding": existing_user is None or existing_user.get("age") is None}

@app.get("/api/auth/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.post("/api/auth/logout")
async def logout(response: Response, session_token: Optional[str] = Cookie(None)):
    if session_token:
        db.user_sessions.delete_one({"session_token": session_token})
    response.delete_cookie(key="session_token", path="/")
    return {"success": True}

@app.post("/api/auth/onboarding")
async def complete_onboarding(data: OnboardingData, current_user: User = Depends(get_current_user)):
    # Calculate BMR and daily calories
    if data.gender.lower() == "erkek":
        bmr = 10 * data.weight_kg + 6.25 * data.height_cm - 5 * data.age + 5
    else:
        bmr = 10 * data.weight_kg + 6.25 * data.height_cm - 5 * data.age - 161
    
    activity_multipliers = {
        "sedanter": 1.2,
        "hafif": 1.375,
        "orta": 1.55,
        "aktif": 1.725,
        "çok_aktif": 1.9
    }
    
    tdee = bmr * activity_multipliers.get(data.activity_level, 1.2)
    
    # Adjust based on goal
    if data.goal_weight_kg < data.weight_kg:
        daily_calories = int(tdee - 500)  # Deficit for weight loss
    elif data.goal_weight_kg > data.weight_kg:
        daily_calories = int(tdee + 300)  # Surplus for weight gain
    else:
        daily_calories = int(tdee)  # Maintenance
    
    db.users.update_one(
        {"_id": current_user.id},
        {"$set": {
            "age": data.age,
            "gender": data.gender,
            "height_cm": data.height_cm,
            "weight_kg": data.weight_kg,
            "goal_weight_kg": data.goal_weight_kg,
            "activity_level": data.activity_level,
            "daily_calorie_goal": daily_calories
        }}
    )
    
    return {"success": True, "daily_calorie_goal": daily_calories}

# ==================== FOOD ANALYSIS WITH GEMINI ====================

@app.post("/api/analyze-food")
async def analyze_food(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    # Read image
    image_data = await file.read()
    image_base64 = base64.b64encode(image_data).decode('utf-8')
    
    # Analyze with Gemini
    try:
        chat = LlmChat(
            api_key=GEMINI_API_KEY,
            session_id=f"food_analysis_{uuid.uuid4()}",
            system_message="Sen bir beslenme uzmanısın. Yemek fotoğraflarını analiz ederek yemek adını, tahmini porsiyon miktarını ve besin değerlerini tahmin ediyorsun."
        ).with_model("gemini", "gemini-2.0-flash")
        
        image_content = ImageContent(image_base64=image_base64)
        
        prompt = """Bu görseldeki yemeği analiz et ve aşağıdaki bilgileri JSON formatında ver:
{
  "food_name": "yemek adı (Türkçe)",
  "portion_size": "tahmini porsiyon (örn: '1 porsiyon', 'yarım porsiyon', 'çeyrek ekmek', '2 dilim', '100 gram', vb.)",
  "calories": tahmini kalori sayısı (sayı),
  "protein": protein gramı (sayı),
  "carbs": karbonhidrat gramı (sayı),
  "fat": yağ gramı (sayı)
}

Sadece JSON formatında cevap ver, başka açıklama ekleme."""
        
        user_message = UserMessage(
            text=prompt,
            file_contents=[image_content]
        )
        
        response = await chat.send_message(user_message)
        
        # Parse response
        import json
        response_text = response.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        food_data = json.loads(response_text)
        
        # Save to database
        food_log = {
            "id": str(uuid.uuid4()),
            "user_id": current_user.id,
            "food_name": food_data["food_name"],
            "portion_size": food_data["portion_size"],
            "calories": float(food_data["calories"]),
            "protein": float(food_data.get("protein", 0)),
            "carbs": float(food_data.get("carbs", 0)),
            "fat": float(food_data.get("fat", 0)),
            "image_base64": image_base64,
            "logged_at": datetime.now(timezone.utc),
            "is_deleted": False
        }
        
        db.food_logs.insert_one(food_log)
        
        return food_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analiz hatası: {str(e)}")

# ==================== FOOD LOGS ====================

@app.get("/api/food-logs")
async def get_food_logs(date: Optional[str] = None, current_user: User = Depends(get_current_user)):
    query = {"user_id": current_user.id, "is_deleted": False}
    
    if date:
        start_date = datetime.fromisoformat(date.replace('Z', '+00:00'))
        end_date = start_date + timedelta(days=1)
        query["logged_at"] = {"$gte": start_date, "$lt": end_date}
    
    logs = list(db.food_logs.find(query).sort("logged_at", -1))
    for log in logs:
        log["_id"] = str(log.get("_id", ""))
    return logs

@app.delete("/api/food-logs/{log_id}")
async def delete_food_log(log_id: str, current_user: User = Depends(get_current_user)):
    db.food_logs.update_one(
        {"id": log_id, "user_id": current_user.id},
        {"$set": {"is_deleted": True}}
    )
    return {"success": True}

# ==================== TURKISH FOODS DATABASE ====================

@app.get("/api/turkish-foods")
async def get_turkish_foods(search: Optional[str] = None):
    query = {}
    if search:
        query["name"] = {"$regex": search, "$options": "i"}
    
    foods = list(db.turkish_foods.find(query).limit(50))
    for food in foods:
        food["_id"] = str(food.get("_id", ""))
    return foods

@app.post("/api/food-logs/manual")
async def add_manual_food_log(food_name: str, portion_grams: float, current_user: User = Depends(get_current_user)):
    # Find food in Turkish foods database
    food = db.turkish_foods.find_one({"name": {"$regex": food_name, "$options": "i"}})
    
    if not food:
        raise HTTPException(status_code=404, detail="Yemek bulunamadı")
    
    # Calculate nutrition based on portion
    multiplier = portion_grams / 100
    
    food_log = {
        "id": str(uuid.uuid4()),
        "user_id": current_user.id,
        "food_name": food["name"],
        "portion_size": f"{portion_grams}g",
        "calories": food["calories_per_100g"] * multiplier,
        "protein": food["protein_per_100g"] * multiplier,
        "carbs": food["carbs_per_100g"] * multiplier,
        "fat": food["fat_per_100g"] * multiplier,
        "logged_at": datetime.now(timezone.utc),
        "is_deleted": False
    }
    
    db.food_logs.insert_one(food_log)
    # Remove MongoDB _id for JSON serialization
    food_log.pop("_id", None)
    return food_log

# ==================== WORKOUT LOGS ====================

@app.get("/api/workout-logs")
async def get_workout_logs(date: Optional[str] = None, current_user: User = Depends(get_current_user)):
    query = {"user_id": current_user.id, "is_deleted": False}
    
    if date:
        start_date = datetime.fromisoformat(date.replace('Z', '+00:00'))
        end_date = start_date + timedelta(days=1)
        query["logged_at"] = {"$gte": start_date, "$lt": end_date}
    
    logs = list(db.workout_logs.find(query).sort("logged_at", -1))
    for log in logs:
        log["_id"] = str(log.get("_id", ""))
    return logs

@app.post("/api/workout-logs")
async def add_workout_log(exercise_name: str, duration_minutes: int, calories_burned: float, current_user: User = Depends(get_current_user)):
    workout_log = {
        "id": str(uuid.uuid4()),
        "user_id": current_user.id,
        "exercise_name": exercise_name,
        "duration_minutes": duration_minutes,
        "calories_burned": calories_burned,
        "logged_at": datetime.now(timezone.utc),
        "is_deleted": False
    }
    
    db.workout_logs.insert_one(workout_log)
    # Remove MongoDB _id for JSON serialization
    workout_log.pop("_id", None)
    return workout_log

@app.delete("/api/workout-logs/{log_id}")
async def delete_workout_log(log_id: str, current_user: User = Depends(get_current_user)):
    db.workout_logs.update_one(
        {"id": log_id, "user_id": current_user.id},
        {"$set": {"is_deleted": True}}
    )
    return {"success": True}

# ==================== STATS ====================

@app.get("/api/stats/daily")
async def get_daily_stats(date: Optional[str] = None, current_user: User = Depends(get_current_user)):
    if date:
        target_date = datetime.fromisoformat(date.replace('Z', '+00:00'))
    else:
        target_date = datetime.now(timezone.utc)
    
    start_date = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = start_date + timedelta(days=1)
    
    # Get food logs
    food_logs = list(db.food_logs.find({
        "user_id": current_user.id,
        "is_deleted": False,
        "logged_at": {"$gte": start_date, "$lt": end_date}
    }))
    
    # Get workout logs
    workout_logs = list(db.workout_logs.find({
        "user_id": current_user.id,
        "is_deleted": False,
        "logged_at": {"$gte": start_date, "$lt": end_date}
    }))
    
    total_calories_consumed = sum(log["calories"] for log in food_logs)
    total_calories_burned = sum(log["calories_burned"] for log in workout_logs)
    total_protein = sum(log.get("protein", 0) for log in food_logs)
    total_carbs = sum(log.get("carbs", 0) for log in food_logs)
    total_fat = sum(log.get("fat", 0) for log in food_logs)
    
    net_calories = total_calories_consumed - total_calories_burned
    
    return {
        "date": start_date.isoformat(),
        "calories_consumed": total_calories_consumed,
        "calories_burned": total_calories_burned,
        "net_calories": net_calories,
        "daily_goal": current_user.daily_calorie_goal or 2000,
        "protein": total_protein,
        "carbs": total_carbs,
        "fat": total_fat,
        "meals_count": len(food_logs),
        "workouts_count": len(workout_logs)
    }

@app.get("/api/stats/weekly")
async def get_weekly_stats(current_user: User = Depends(get_current_user)):
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=7)
    
    daily_stats = []
    for i in range(7):
        day = start_date + timedelta(days=i)
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        
        food_logs = list(db.food_logs.find({
            "user_id": current_user.id,
            "is_deleted": False,
            "logged_at": {"$gte": day_start, "$lt": day_end}
        }))
        
        workout_logs = list(db.workout_logs.find({
            "user_id": current_user.id,
            "is_deleted": False,
            "logged_at": {"$gte": day_start, "$lt": day_end}
        }))
        
        calories_consumed = sum(log["calories"] for log in food_logs)
        calories_burned = sum(log["calories_burned"] for log in workout_logs)
        
        daily_stats.append({
            "date": day_start.isoformat(),
            "calories_consumed": calories_consumed,
            "calories_burned": calories_burned,
            "net_calories": calories_consumed - calories_burned
        })
    
    return daily_stats

# ==================== ACHIEVEMENTS ====================

@app.get("/api/achievements")
async def get_achievements(current_user: User = Depends(get_current_user)):
    achievements = list(db.achievements.find({"user_id": current_user.id}).sort("earned_at", -1))
    for achievement in achievements:
        achievement["_id"] = str(achievement.get("_id", ""))
    return achievements

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)