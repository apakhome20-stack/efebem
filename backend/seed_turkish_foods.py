from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
database_name = os.getenv("DATABASE_NAME", "apak_fitness")
client = MongoClient(mongo_url)
db = client[database_name]

# Comprehensive Turkish food database
turkish_foods = [
    # Ekmek ve Tahıllar
    {"name": "Beyaz Ekmek", "calories_per_100g": 265, "protein_per_100g": 9, "carbs_per_100g": 49, "fat_per_100g": 3.2, "category": "Ekmek"},
    {"name": "Tam Buğday Ekmeği", "calories_per_100g": 247, "protein_per_100g": 13, "carbs_per_100g": 41, "fat_per_100g": 3.4, "category": "Ekmek"},
    {"name": "Çavdar Ekmeği", "calories_per_100g": 259, "protein_per_100g": 8.5, "carbs_per_100g": 48, "fat_per_100g": 3.3, "category": "Ekmek"},
    {"name": "Simit", "calories_per_100g": 420, "protein_per_100g": 11, "carbs_per_100g": 68, "fat_per_100g": 11, "category": "Ekmek"},
    {"name": "Pide", "calories_per_100g": 275, "protein_per_100g": 8, "carbs_per_100g": 50, "fat_per_100g": 4.5, "category": "Ekmek"},
    {"name": "Lavaş", "calories_per_100g": 258, "protein_per_100g": 8.7, "carbs_per_100g": 50, "fat_per_100g": 1.2, "category": "Ekmek"},
    {"name": "Yufka", "calories_per_100g": 300, "protein_per_100g": 9, "carbs_per_100g": 62, "fat_per_100g": 2, "category": "Ekmek"},
    {"name": "Bulgur Pilavı", "calories_per_100g": 342, "protein_per_100g": 12, "carbs_per_100g": 76, "fat_per_100g": 1.3, "category": "Tahıl"},
    {"name": "Pirinç Pilavı", "calories_per_100g": 130, "protein_per_100g": 2.7, "carbs_per_100g": 28, "fat_per_100g": 0.3, "category": "Tahıl"},
    {"name": "Makarna", "calories_per_100g": 158, "protein_per_100g": 5.8, "carbs_per_100g": 31, "fat_per_100g": 0.9, "category": "Tahıl"},
    
    # Ana Yemekler - Et
    {"name": "Adana Kebap", "calories_per_100g": 280, "protein_per_100g": 18, "carbs_per_100g": 2, "fat_per_100g": 23, "category": "Et"},
    {"name": "Urfa Kebap", "calories_per_100g": 260, "protein_per_100g": 19, "carbs_per_100g": 1.5, "fat_per_100g": 20, "category": "Et"},
    {"name": "Şiş Kebap", "calories_per_100g": 220, "protein_per_100g": 25, "carbs_per_100g": 0, "fat_per_100g": 13, "category": "Et"},
    {"name": "İskender Kebap", "calories_per_100g": 195, "protein_per_100g": 16, "carbs_per_100g": 10, "fat_per_100g": 11, "category": "Et"},
    {"name": "Tavuk Şiş", "calories_per_100g": 165, "protein_per_100g": 31, "carbs_per_100g": 0, "fat_per_100g": 3.6, "category": "Tavuk"},
    {"name": "Tavuk Döner", "calories_per_100g": 178, "protein_per_100g": 27, "carbs_per_100g": 5, "fat_per_100g": 6, "category": "Tavuk"},
    {"name": "Et Döner", "calories_per_100g": 265, "protein_per_100g": 20, "carbs_per_100g": 3, "fat_per_100g": 19, "category": "Et"},
    {"name": "Köfte", "calories_per_100g": 255, "protein_per_100g": 17, "carbs_per_100g": 8, "fat_per_100g": 17, "category": "Et"},
    {"name": "İnegöl Köfte", "calories_per_100g": 280, "protein_per_100g": 18, "carbs_per_100g": 6, "fat_per_100g": 20, "category": "Et"},
    {"name": "Kuru Fasulye", "calories_per_100g": 127, "protein_per_100g": 8.7, "carbs_per_100g": 23, "fat_per_100g": 0.5, "category": "Baklagil"},
    {"name": "Kuzu Tandır", "calories_per_100g": 295, "protein_per_100g": 25, "carbs_per_100g": 0, "fat_per_100g": 21, "category": "Et"},
    {"name": "Ali Nazik Kebap", "calories_per_100g": 180, "protein_per_100g": 14, "carbs_per_100g": 8, "fat_per_100g": 11, "category": "Et"},
    {"name": "Hünkar Beğendi", "calories_per_100g": 150, "protein_per_100g": 12, "carbs_per_100g": 9, "fat_per_100g": 8, "category": "Et"},
    
    # Balık ve Deniz Ürünleri
    {"name": "Hamsi Tava", "calories_per_100g": 185, "protein_per_100g": 18, "carbs_per_100g": 8, "fat_per_100g": 9, "category": "Balık"},
    {"name": "Levrek Izgara", "calories_per_100g": 97, "protein_per_100g": 18, "carbs_per_100g": 0, "fat_per_100g": 2, "category": "Balık"},
    {"name": "Çupra Izgara", "calories_per_100g": 115, "protein_per_100g": 20, "carbs_per_100g": 0, "fat_per_100g": 3.5, "category": "Balık"},
    {"name": "Somon Balığı", "calories_per_100g": 208, "protein_per_100g": 20, "carbs_per_100g": 0, "fat_per_100g": 13, "category": "Balık"},
    {"name": "Palamut", "calories_per_100g": 158, "protein_per_100g": 24, "carbs_per_100g": 0, "fat_per_100g": 6.3, "category": "Balık"},
    {"name": "Midye Dolma", "calories_per_100g": 172, "protein_per_100g": 10, "carbs_per_100g": 24, "fat_per_100g": 4, "category": "Deniz Ürünleri"},
    
    # Zeytinyağlılar
    {"name": "İmam Bayıldı", "calories_per_100g": 120, "protein_per_100g": 2, "carbs_per_100g": 12, "fat_per_100g": 7, "category": "Zeytinyağlı"},
    {"name": "Zeytinyağlı Yaprak Sarma", "calories_per_100g": 95, "protein_per_100g": 2.5, "carbs_per_100g": 15, "fat_per_100g": 3, "category": "Zeytinyağlı"},
    {"name": "Zeytinyağlı Fasulye", "calories_per_100g": 85, "protein_per_100g": 3, "carbs_per_100g": 12, "fat_per_100g": 3, "category": "Zeytinyağlı"},
    {"name": "Zeytinyağlı Enginar", "calories_per_100g": 68, "protein_per_100g": 2.8, "carbs_per_100g": 10, "fat_per_100g": 2, "category": "Zeytinyağlı"},
    {"name": "Patlıcan Musakka", "calories_per_100g": 140, "protein_per_100g": 5, "carbs_per_100g": 10, "fat_per_100g": 9, "category": "Zeytinyağlı"},
    
    # Çorbalar
    {"name": "Mercimek Çorbası", "calories_per_100g": 95, "protein_per_100g": 5, "carbs_per_100g": 16, "fat_per_100g": 1.5, "category": "Çorba"},
    {"name": "Ezogelin Çorbası", "calories_per_100g": 88, "protein_per_100g": 4, "carbs_per_100g": 15, "fat_per_100g": 1.2, "category": "Çorba"},
    {"name": "Tarhana Çorbası", "calories_per_100g": 92, "protein_per_100g": 4.5, "carbs_per_100g": 16, "fat_per_100g": 1.5, "category": "Çorba"},
    {"name": "İşkembe Çorbası", "calories_per_100g": 108, "protein_per_100g": 11, "carbs_per_100g": 7, "fat_per_100g": 4, "category": "Çorba"},
    {"name": "Yayla Çorbası", "calories_per_100g": 65, "protein_per_100g": 3, "carbs_per_100g": 10, "fat_per_100g": 1.5, "category": "Çorba"},
    {"name": "Domates Çorbası", "calories_per_100g": 74, "protein_per_100g": 2, "carbs_per_100g": 13, "fat_per_100g": 1.8, "category": "Çorba"},
    
    # Börekler ve Hamur İşleri
    {"name": "Su Böreği", "calories_per_100g": 195, "protein_per_100g": 7, "carbs_per_100g": 22, "fat_per_100g": 9, "category": "Börek"},
    {"name": "Kol Böreği", "calories_per_100g": 310, "protein_per_100g": 8, "carbs_per_100g": 28, "fat_per_100g": 18, "category": "Börek"},
    {"name": "Sigara Böreği", "calories_per_100g": 290, "protein_per_100g": 9, "carbs_per_100g": 25, "fat_per_100g": 17, "category": "Börek"},
    {"name": "Gözleme (Peynirli)", "calories_per_100g": 235, "protein_per_100g": 9, "carbs_per_100g": 30, "fat_per_100g": 9, "category": "Börek"},
    {"name": "Lahmacun", "calories_per_100g": 260, "protein_per_100g": 10, "carbs_per_100g": 35, "fat_per_100g": 9, "category": "Hamur İşi"},
    {"name": "Pide (Kıymalı)", "calories_per_100g": 290, "protein_per_100g": 12, "carbs_per_100g": 38, "fat_per_100g": 11, "category": "Hamur İşi"},
    {"name": "Mantı", "calories_per_100g": 165, "protein_per_100g": 8, "carbs_per_100g": 24, "fat_per_100g": 4, "category": "Hamur İşi"},
    
    # Sebze Yemekleri
    {"name": "Karnıyarık", "calories_per_100g": 158, "protein_per_100g": 6, "carbs_per_100g": 12, "fat_per_100g": 10, "category": "Sebze"},
    {"name": "Türlü", "calories_per_100g": 85, "protein_per_100g": 3, "carbs_per_100g": 14, "fat_per_100g": 2, "category": "Sebze"},
    {"name": "Dolma (Etli)", "calories_per_100g": 145, "protein_per_100g": 7, "carbs_per_100g": 16, "fat_per_100g": 6, "category": "Sebze"},
    {"name": "Bamya", "calories_per_100g": 92, "protein_per_100g": 4, "carbs_per_100g": 14, "fat_per_100g": 2.5, "category": "Sebze"},
    {"name": "Ispanak Yemeği", "calories_per_100g": 68, "protein_per_100g": 4, "carbs_per_100g": 8, "fat_per_100g": 2.5, "category": "Sebze"},
    {"name": "Pırasa Yemeği", "calories_per_100g": 75, "protein_per_100g": 2.5, "carbs_per_100g": 12, "fat_per_100g": 2, "category": "Sebze"},
    
    # Salatalar
    {"name": "Çoban Salata", "calories_per_100g": 45, "protein_per_100g": 1.5, "carbs_per_100g": 8, "fat_per_100g": 1.2, "category": "Salata"},
    {"name": "Mevsim Salata", "calories_per_100g": 35, "protein_per_100g": 1.2, "carbs_per_100g": 7, "fat_per_100g": 0.5, "category": "Salata"},
    {"name": "Çingene Salatası", "calories_per_100g": 52, "protein_per_100g": 2, "carbs_per_100g": 9, "fat_per_100g": 1.5, "category": "Salata"},
    {"name": "Piyaz", "calories_per_100g": 125, "protein_per_100g": 5, "carbs_per_100g": 20, "fat_per_100g": 3, "category": "Salata"},
    {"name": "Atom", "calories_per_100g": 58, "protein_per_100g": 2.5, "carbs_per_100g": 10, "fat_per_100g": 1.5, "category": "Salata"},
    
    # Mezeler
    {"name": "Haydari", "calories_per_100g": 145, "protein_per_100g": 6, "carbs_per_100g": 8, "fat_per_100g": 10, "category": "Meze"},
    {"name": "Cacık", "calories_per_100g": 48, "protein_per_100g": 2.5, "carbs_per_100g": 4, "fat_per_100g": 2.5, "category": "Meze"},
    {"name": "Humus", "calories_per_100g": 166, "protein_per_100g": 8, "carbs_per_100g": 14, "fat_per_100g": 10, "category": "Meze"},
    {"name": "Babaganuş", "calories_per_100g": 105, "protein_per_100g": 2.5, "carbs_per_100g": 12, "fat_per_100g": 6, "category": "Meze"},
    {"name": "Ezme", "calories_per_100g": 65, "protein_per_100g": 2, "carbs_per_100g": 12, "fat_per_100g": 1.5, "category": "Meze"},
    {"name": "Tarama", "calories_per_100g": 185, "protein_per_100g": 5, "carbs_per_100g": 10, "fat_per_100g": 14, "category": "Meze"},
    
    # Süt Ürünleri
    {"name": "Beyaz Peynir", "calories_per_100g": 264, "protein_per_100g": 18, "carbs_per_100g": 1.5, "fat_per_100g": 21, "category": "Süt Ürünü"},
    {"name": "Kaşar Peyniri", "calories_per_100g": 330, "protein_per_100g": 23, "carbs_per_100g": 0, "fat_per_100g": 27, "category": "Süt Ürünü"},
    {"name": "Lor Peyniri", "calories_per_100g": 166, "protein_per_100g": 13, "carbs_per_100g": 3, "fat_per_100g": 11, "category": "Süt Ürünü"},
    {"name": "Süzme Yoğurt", "calories_per_100g": 85, "protein_per_100g": 8, "carbs_per_100g": 6, "fat_per_100g": 3.5, "category": "Süt Ürünü"},
    {"name": "Ayran", "calories_per_100g": 36, "protein_per_100g": 1.7, "carbs_per_100g": 4.5, "fat_per_100g": 1, "category": "Süt Ürünü"},
    {"name": "Tam Yağlı Süt", "calories_per_100g": 61, "protein_per_100g": 3.2, "carbs_per_100g": 4.8, "fat_per_100g": 3.3, "category": "Süt Ürünü"},
    
    # Tatlılar
    {"name": "Baklava", "calories_per_100g": 428, "protein_per_100g": 7, "carbs_per_100g": 51, "fat_per_100g": 22, "category": "Tatlı"},
    {"name": "Künefe", "calories_per_100g": 385, "protein_per_100g": 8, "carbs_per_100g": 48, "fat_per_100g": 18, "category": "Tatlı"},
    {"name": "Revani", "calories_per_100g": 340, "protein_per_100g": 5, "carbs_per_100g": 52, "fat_per_100g": 12, "category": "Tatlı"},
    {"name": "Sütlaç", "calories_per_100g": 130, "protein_per_100g": 4, "carbs_per_100g": 22, "fat_per_100g": 3, "category": "Tatlı"},
    {"name": "Kazandibi", "calories_per_100g": 195, "protein_per_100g": 5, "carbs_per_100g": 28, "fat_per_100g": 7, "category": "Tatlı"},
    {"name": "Lokma", "calories_per_100g": 325, "protein_per_100g": 5, "carbs_per_100g": 48, "fat_per_100g": 14, "category": "Tatlı"},
    {"name": "Tulumba Tatlısı", "calories_per_100g": 330, "protein_per_100g": 4, "carbs_per_100g": 50, "fat_per_100g": 13, "category": "Tatlı"},
    
    # İçecekler
    {"name": "Türk Kahvesi", "calories_per_100g": 12, "protein_per_100g": 0.5, "carbs_per_100g": 2, "fat_per_100g": 0.5, "category": "İçecek"},
    {"name": "Çay (Şekersiz)", "calories_per_100g": 1, "protein_per_100g": 0, "carbs_per_100g": 0.3, "fat_per_100g": 0, "category": "İçecek"},
    {"name": "Şalgam Suyu", "calories_per_100g": 12, "protein_per_100g": 0.5, "carbs_per_100g": 2.5, "fat_per_100g": 0, "category": "İçecek"},
    {"name": "Boza", "calories_per_100g": 95, "protein_per_100g": 1.5, "carbs_per_100g": 21, "fat_per_100g": 0.5, "category": "İçecek"},
    {"name": "Sahlep", "calories_per_100g": 75, "protein_per_100g": 3, "carbs_per_100g": 13, "fat_per_100g": 1.5, "category": "İçecek"},
    
    # Fast Food (Türk Stili)
    {"name": "Döner Dürüm", "calories_per_100g": 215, "protein_per_100g": 15, "carbs_per_100g": 20, "fat_per_100g": 9, "category": "Fast Food"},
    {"name": "Tantuni", "calories_per_100g": 190, "protein_per_100g": 14, "carbs_per_100g": 18, "fat_per_100g": 8, "category": "Fast Food"},
    {"name": "Kokoreç", "calories_per_100g": 265, "protein_per_100g": 18, "carbs_per_100g": 3, "fat_per_100g": 20, "category": "Fast Food"},
    {"name": "Islak Hamburger", "calories_per_100g": 240, "protein_per_100g": 12, "carbs_per_100g": 28, "fat_per_100g": 9, "category": "Fast Food"},
    
    # Kahvaltılık
    {"name": "Menemen", "calories_per_100g": 156, "protein_per_100g": 8, "carbs_per_100g": 6, "fat_per_100g": 11, "category": "Kahvaltı"},
    {"name": "Sucuklu Yumurta", "calories_per_100g": 285, "protein_per_100g": 16, "carbs_per_100g": 2, "fat_per_100g": 24, "category": "Kahvaltı"},
    {"name": "Kavurma", "calories_per_100g": 380, "protein_per_100g": 22, "carbs_per_100g": 0, "fat_per_100g": 32, "category": "Kahvaltı"},
    {"name": "Tahin-Pekmez", "calories_per_100g": 465, "protein_per_100g": 12, "carbs_per_100g": 48, "fat_per_100g": 26, "category": "Kahvaltı"},
    {"name": "Bal", "calories_per_100g": 304, "protein_per_100g": 0.3, "carbs_per_100g": 82, "fat_per_100g": 0, "category": "Kahvaltı"},
    {"name": "Reçel", "calories_per_100g": 278, "protein_per_100g": 0.4, "carbs_per_100g": 69, "fat_per_100g": 0.1, "category": "Kahvaltı"},
    {"name": "Zeytin (Siyah)", "calories_per_100g": 115, "protein_per_100g": 0.8, "carbs_per_100g": 6, "fat_per_100g": 11, "category": "Kahvaltı"},
    {"name": "Zeytin (Yeşil)", "calories_per_100g": 145, "protein_per_100g": 1, "carbs_per_100g": 4, "fat_per_100g": 15, "category": "Kahvaltı"},
    
    # Atıştırmalıklar
    {"name": "Fındık", "calories_per_100g": 628, "protein_per_100g": 15, "carbs_per_100g": 17, "fat_per_100g": 61, "category": "Atıştırmalık"},
    {"name": "Ceviz", "calories_per_100g": 654, "protein_per_100g": 15, "carbs_per_100g": 14, "fat_per_100g": 65, "category": "Atıştırmalık"},
    {"name": "Antep Fıstığı", "calories_per_100g": 562, "protein_per_100g": 20, "carbs_per_100g": 28, "fat_per_100g": 45, "category": "Atıştırmalık"},
    {"name": "Leblebi", "calories_per_100g": 368, "protein_per_100g": 20, "carbs_per_100g": 61, "fat_per_100g": 6, "category": "Atıştırmalık"},
    {"name": "Çerez Karışımı", "calories_per_100g": 520, "protein_per_100g": 17, "carbs_per_100g": 30, "fat_per_100g": 38, "category": "Atıştırmalık"},
]

# Clear existing and insert
db.turkish_foods.delete_many({})
for food in turkish_foods:
    food["id"] = food["name"].lower().replace(" ", "_")
    db.turkish_foods.insert_one(food)

print(f"✅ {len(turkish_foods)} Turkish foods inserted successfully!")
