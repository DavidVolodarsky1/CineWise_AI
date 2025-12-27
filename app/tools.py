import os
import requests
from dotenv import load_dotenv

load_dotenv()

class MovieTools:
    def __init__(self):
        """
        Initialize the TMDB API client.
        The API Key should be the standard API Key (v3 auth).
        """
        self.api_key = os.getenv("TMDB_API_KEY")
        self.base_url = "https://api.themoviedb.org/3"

    def search_movie(self, title):
        """
        Search for a movie by title.
        Returns a list of movie objects including IDs, titles, overviews, and posters.
        """
        url = f"{self.base_url}/search/movie"
        params = {
            "api_key": self.api_key,
            "query": title,
            "language": "he-IL"
        }
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            results = []
            for m in data.get('results', [])[:3]:
                # Constructing the absolute URL for the movie poster
                poster_path = m.get("poster_path")
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
                
                results.append({
                    "id": m.get("id"),
                    "title": m.get("title"),
                    "overview": m.get("overview"),
                    "rating": m.get("vote_average"),
                    "poster": poster_url
                })
            return results
        return []

    def discover_movies(self, genre_id: int = None, year: int = None):
        """
        Discover movies based on genre IDs and release year.
        Uses TMDB discover endpoint with popularity-based sorting.
        """
        url = f"{self.base_url}/discover/movie"
        params = {
            "api_key": self.api_key,
            "language": "he-IL",
            "sort_by": "popularity.desc",
            "with_genres": genre_id,
            "primary_release_year": year
        }
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json().get('results', [])[:5]
            results = []
            for m in data:
                poster_path = m.get("poster_path")
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
                results.append({
                    "id": m.get("id"),
                    "title": m.get("title"),
                    "rating": m.get("vote_average"),
                    "poster": poster_url,
                    "release_date": m.get("release_date")
                })
            return results
        return []

    def get_genres(self):
        """
        Retrieve the official list of genres and their respective IDs.
        """
        url = f"{self.base_url}/genre/movie/list"
        params = {"api_key": self.api_key, "language": "he-IL"}
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            return response.json().get('genres', [])
        return []

    def get_watch_providers(self, movie_title: str):
        """
        Identify streaming, rental, and purchase providers for a specific movie in Israel.
        Performs a search to obtain the movie ID before querying watch providers.
        """
        # Step 1: Resolve movie ID via search
        movie_results = self.search_movie(movie_title)
        if not movie_results:
            return "Watch provider information not found."
        
        movie_id = movie_results[0]['id']
        url = f"{self.base_url}/movie/{movie_id}/watch/providers"
        params = {"api_key": self.api_key}
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            # Focusing results on the Israeli market (IL)
            results = response.json().get('results', {}).get('IL', {})
            providers = {
                "flatrate": [p['provider_name'] for p in results.get('flatrate', [])],
                "rent": [p['provider_name'] for p in results.get('rent', [])],
                "buy": [p['provider_name'] for p in results.get('buy', [])]
            }
            return providers if any(providers.values()) else "Movie is not currently available for streaming in Israel."
        return "Error occurred while fetching watch providers."