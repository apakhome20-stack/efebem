from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
database_name = os.getenv("DATABASE_NAME", "apak_fitness")
client = MongoClient(mongo_url)
db = client[database_name]

# Comprehensive workout/exercise database with calorie burn rates per minute
workout_exercises = [
    # Kardiyo Egzersizleri
    {"name": "Koşu (Yavaş - 8 km/sa)", "calories_per_minute": 8, "category": "Kardiyo", "intensity": "Orta"},
    {"name": "Koşu (Orta - 10 km/sa)", "calories_per_minute": 10, "category": "Kardiyo", "intensity": "Yüksek"},
    {"name": "Koşu (Hızlı - 12+ km/sa)", "calories_per_minute": 13, "category": "Kardiyo", "intensity": "Çok Yüksek"},
    {"name": "Yürüyüş (Yavaş)", "calories_per_minute": 3, "category": "Kardiyo", "intensity": "Düşük"},
    {"name": "Yürüyüş (Hızlı)", "calories_per_minute": 5, "category": "Kardiyo", "intensity": "Orta"},
    {"name": "Bisiklet (Yavaş)", "calories_per_minute": 5, "category": "Kardiyo", "intensity": "Orta"},
    {"name": "Bisiklet (Orta)", "calories_per_minute": 8, "category": "Kardiyo", "intensity": "Yüksek"},
    {"name": "Bisiklet (Hızlı)", "calories_per_minute": 12, "category": "Kardiyo", "intensity": "Çok Yüksek"},
    {"name": "Yüzme (Yavaş)", "calories_per_minute": 6, "category": "Kardiyo", "intensity": "Orta"},
    {"name": "Yüzme (Hızlı)", "calories_per_minute": 11, "category": "Kardiyo", "intensity": "Yüksek"},
    {"name": "İp Atlama", "calories_per_minute": 12, "category": "Kardiyo", "intensity": "Yüksek"},
    {"name": "Eliptik Bisiklet", "calories_per_minute": 9, "category": "Kardiyo", "intensity": "Yüksek"},
    {"name": "Merdiven Çıkma", "calories_per_minute": 10, "category": "Kardiyo", "intensity": "Yüksek"},
    {"name": "Dans", "calories_per_minute": 6, "category": "Kardiyo", "intensity": "Orta"},
    {"name": "Aerobik", "calories_per_minute": 7, "category": "Kardiyo", "intensity": "Yüksek"},
    {"name": "Zumba", "calories_per_minute": 8, "category": "Kardiyo", "intensity": "Yüksek"},
    {"name": "Kick Boks", "calories_per_minute": 10, "category": "Kardiyo", "intensity": "Yüksek"},
    {"name": "Boks", "calories_per_minute": 9, "category": "Kardiyo", "intensity": "Yüksek"},
    
    # Kuvvet Antrenmanları
    {"name": "Ağırlık Kaldırma (Hafif)", "calories_per_minute": 3, "category": "Kuvvet", "intensity": "Orta"},
    {"name": "Ağırlık Kaldırma (Ağır)", "calories_per_minute": 6, "category": "Kuvvet", "intensity": "Yüksek"},
    {"name": "Bench Press", "calories_per_minute": 5, "category": "Kuvvet", "intensity": "Yüksek"},
    {"name": "Squat", "calories_per_minute": 6, "category": "Kuvvet", "intensity": "Yüksek"},
    {"name": "Deadlift", "calories_per_minute": 7, "category": "Kuvvet", "intensity": "Çok Yüksek"},
    {"name": "Shoulder Press", "calories_per_minute": 4, "category": "Kuvvet", "intensity": "Orta"},
    {"name": "Bicep Curl", "calories_per_minute": 3, "category": "Kuvvet", "intensity": "Orta"},
    {"name": "Tricep Extension", "calories_per_minute": 3, "category": "Kuvvet", "intensity": "Orta"},
    {"name": "Lat Pulldown", "calories_per_minute": 4, "category": "Kuvvet", "intensity": "Orta"},
    {"name": "Leg Press", "calories_per_minute": 5, "category": "Kuvvet", "intensity": "Yüksek"},
    {"name": "Leg Curl", "calories_per_minute": 4, "category": "Kuvvet", "intensity": "Orta"},
    {"name": "Leg Extension", "calories_per_minute": 4, "category": "Kuvvet", "intensity": "Orta"},
    {"name": "Cable Crossover", "calories_per_minute": 4, "category": "Kuvvet", "intensity": "Orta"},
    {"name": "Pull-up", "calories_per_minute": 6, "category": "Kuvvet", "intensity": "Yüksek"},
    {"name": "Dips", "calories_per_minute": 5, "category": "Kuvvet", "intensity": "Yüksek"},
    
    # Vücut Ağırlığı Egzersizleri
    {"name": "Şınav", "calories_per_minute": 7, "category": "Vücut Ağırlığı", "intensity": "Yüksek"},
    {"name": "Mekik", "calories_per_minute": 6, "category": "Vücut Ağırlığı", "intensity": "Orta"},
    {"name": "Plank", "calories_per_minute": 5, "category": "Vücut Ağırlığı", "intensity": "Orta"},
    {"name": "Burpee", "calories_per_minute": 10, "category": "Vücut Ağırlığı", "intensity": "Çok Yüksek"},
    {"name": "Mountain Climber", "calories_per_minute": 8, "category": "Vücut Ağırlığı", "intensity": "Yüksek"},
    {"name": "Jumping Jacks", "calories_per_minute": 8, "category": "Vücut Ağırlığı", "intensity": "Yüksek"},
    {"name": "Squat (Vücut Ağırlığı)", "calories_per_minute": 5, "category": "Vücut Ağırlığı", "intensity": "Orta"},
    {"name": "Lunges", "calories_per_minute": 6, "category": "Vücut Ağırlığı", "intensity": "Orta"},
    
    # HIIT ve CrossFit
    {"name": "HIIT", "calories_per_minute": 12, "category": "HIIT", "intensity": "Çok Yüksek"},
    {"name": "Tabata", "calories_per_minute": 13, "category": "HIIT", "intensity": "Çok Yüksek"},
    {"name": "CrossFit", "calories_per_minute": 11, "category": "CrossFit", "intensity": "Çok Yüksek"},
    {"name": "Circuit Training", "calories_per_minute": 9, "category": "HIIT", "intensity": "Yüksek"},
    
    # Yoga ve Pilates
    {"name": "Yoga (Hatha)", "calories_per_minute": 3, "category": "Yoga", "intensity": "Düşük"},
    {"name": "Yoga (Vinyasa)", "calories_per_minute": 5, "category": "Yoga", "intensity": "Orta"},
    {"name": "Yoga (Ashtanga)", "calories_per_minute": 6, "category": "Yoga", "intensity": "Yüksek"},
    {"name": "Pilates", "calories_per_minute": 4, "category": "Pilates", "intensity": "Orta"},
    {"name": "Pilates (Makine)", "calories_per_minute": 5, "category": "Pilates", "intensity": "Orta"},
    
    # Sporlar
    {"name": "Futbol", "calories_per_minute": 9, "category": "Takım Sporu", "intensity": "Yüksek"},
    {"name": "Basketbol", "calories_per_minute": 8, "category": "Takım Sporu", "intensity": "Yüksek"},
    {"name": "Voleybol", "calories_per_minute": 6, "category": "Takım Sporu", "intensity": "Orta"},
    {"name": "Tenis", "calories_per_minute": 7, "category": "Raket Sporu", "intensity": "Yüksek"},
    {"name": "Badminton", "calories_per_minute": 6, "category": "Raket Sporu", "intensity": "Orta"},
    {"name": "Masa Tenisi", "calories_per_minute": 4, "category": "Raket Sporu", "intensity": "Orta"},
    {"name": "Kayak", "calories_per_100g": 7, "category": "Kış Sporu", "intensity": "Yüksek"},
    {"name": "Snowboard", "calories_per_minute": 6, "category": "Kış Sporu", "intensity": "Yüksek"},
    
    # Diğer Aktiviteler
    {"name": "Bahçe İşleri", "calories_per_minute": 4, "category": "Aktivite", "intensity": "Orta"},
    {"name": "Temizlik", "calories_per_minute": 3, "category": "Aktivite", "intensity": "Düşük"},
    {"name": "Çim Biçme", "calories_per_minute": 5, "category": "Aktivite", "intensity": "Orta"},
    {"name": "Kar Küreme", "calories_per_minute": 7, "category": "Aktivite", "intensity": "Yüksek"},
]

# Create collection for workout reference
db.workout_exercises.delete_many({})
for exercise in workout_exercises:
    exercise["id"] = exercise["name"].lower().replace(" ", "_").replace("(", "").replace(")", "")
    db.workout_exercises.insert_one(exercise)

print(f"✅ {len(workout_exercises)} workout exercises inserted successfully!")
