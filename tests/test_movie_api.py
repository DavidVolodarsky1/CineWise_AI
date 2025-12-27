import os
from app.tools import MovieTools
from dotenv import load_dotenv

load_dotenv()

def quick_test():
    print("🎬 בודק חיבור ל-TMDB...")
    tools = MovieTools()
    
    # בדיקה 1: חיפוש סרט
    print("\n🔍 בודק חיפוש סרט: 'Inception'...")
    results = tools.search_movie("Inception")
    
    if isinstance(results, list) and len(results) > 0:
        print(f"✅ הצלחה! נמצא הסרט: {results[0]['title']}")
        print(f"⭐ דירוג: {results[0]['rating']}")
    else:
        print("❌ שגיאה: לא התקבלו תוצאות. בדוק את ה-TMDB_API_KEY ב-'.env'")

    # בדיקה 2: רשימת ז'אנרים
    print("\n🎭 בודק משיכת ז'אנרים...")
    genres = tools.get_genres()
    if genres:
        print(f"✅ הצלחה! נמצאו {len(genres)} ז'אנרים.")
    else:
        print("❌ שגיאה: לא הצלחתי למשוך ז'אנרים.")

if __name__ == "__main__":
    quick_test()