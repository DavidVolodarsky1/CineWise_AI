import os
import requests
from dotenv import load_dotenv

load_dotenv()

class MovieTools:
    def __init__(self):
        self.api_key = os.getenv("TMDB_API_KEY")
        self.base_url = "https://api.themoviedb.org/3"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "accept": "application/json"
        }
    def search_movie(self, title):
        url = f"{self.base_url}/search/movie"
        params = {"api_key": self.api_key, "query": title, "language": "he-IL"}
        response = requests.get(url, params=params)
        data = response.json()
        
        results = []
        for m in data.get('results', [])[:3]:
            # יצירת לינק מלא לתמונה
            poster_url = f"https://image.tmdb.org/t/p/w500{m.get('poster_path')}" if m.get('poster_path') else None
            results.append({
                "id": m.get("id"),
                "title": m.get("title"),
                "overview": m.get("overview"),
                "rating": m.get("vote_average"),
                "poster": poster_url # הוספת הפוסטר לנתונים
            })
        return results
    # def search_movie(self, title: str):
    #     url = f"{self.base_url}/search/movie"
    #     params = {"query": title, "language": "he-IL"}
    #     response = requests.get(url, headers=self.headers, params=params)
        
    #     if response.status_code == 200:
    #         data = response.json().get('results', [])
    #         return [
    #             {
    #                 "title": m.get('title'),
    #                 "rating": m.get('vote_average'), # וודא שזה vote_average
    #                 "release_date": m.get('release_date'),
    #                 "overview": m.get('overview')
    #             } for m in data[:3]
    #         ]
    #     return []

    def discover_movies(self, genre_id: int = None, year: int = None):
        """גילוי סרטים לפי ז'אנר או שנת יציאה."""
        url = f"{self.base_url}/discover/movie"
        params = {
            "language": "he-IL",
            "sort_by": "popularity.desc",
            "with_genres": genre_id,
            "primary_release_year": year
        }
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json().get('results', [])[:5]
        return {"error": "שגיאה במשיכת סרטים."}

    def get_genres(self):
        """מביא את רשימת הז'אנרים וה-ID שלהם."""
        url = f"{self.base_url}/genre/movie/list?language=he-IL"
        response = requests.get(url, headers=self.headers)
        return response.json().get('genres', [])
    
    def get_watch_providers(self, movie_title: str):
        """בדיקה איפה הסרט זמין לצפייה (נטפליקס, אפל וכו') בישראל."""
        # קודם מוצאים את ה-ID של הסרט
        search_url = f"{self.base_url}/search/movie?query={movie_title}&language=he-IL"
        res = requests.get(search_url, headers=self.headers).json()
        if not res.get('results'): return "לא נמצאו פרטי צפייה."
        
        movie_id = res['results'][0]['id']
        # שליחת בקשה לספקי צפייה
        url = f"{self.base_url}/movie/{movie_id}/watch/providers"
        response = requests.get(url, headers=self.headers).json()
        
        results = response.get('results', {}).get('IL', {}) # מיקוד לישראל
        
        providers = {
            "flatrate": [p['provider_name'] for p in results.get('flatrate', [])],
            "rent": [p['provider_name'] for p in results.get('rent', [])],
            "buy": [p['provider_name'] for p in results.get('buy', [])]
        }
        return providers if any(providers.values()) else "הסרט לא זמין כרגע בסטרימינג בישראל."