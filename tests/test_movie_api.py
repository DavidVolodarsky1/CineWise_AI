import os
from app.tools import MovieTools
from dotenv import load_dotenv

load_dotenv()

def quick_test():
    """
    Perform a quick integration test to ensure connectivity with the TMDB API
    and verify that the MovieTools methods return the expected data structures.
    """
    print("🎬 Testing TMDB API Connectivity...")
    tools = MovieTools()
    
    # Test Case 1: Search Functionality
    # We verify that searching for 'Inception' returns a valid result set.
    print("\n🔍 Testing search_movie: 'Inception'...")
    results = tools.search_movie("Inception")
    
    if isinstance(results, list) and len(results) > 0:
        print(f"✅ Success! Movie found: {results[0]['title']}")
        print(f"⭐ Rating: {results[0]['rating']}")
        # Ensure the poster URL was correctly constructed
        if results[0].get('poster'):
            print(f"🖼️ Poster URL retrieved: {results[0]['poster'][:50]}...")
    else:
        print("❌ Error: No results returned. Please check your TMDB_API_KEY in the '.env' file.")

    # Test Case 2: Metadata Retrieval (Genres)
    # We verify that we can fetch the genre mapping table from TMDB.
    print("\n🎭 Testing get_genres...")
    genres = tools.get_genres()
    if isinstance(genres, list) and len(genres) > 0:
        print(f"✅ Success! Found {len(genres)} genres.")
    else:
        print("❌ Error: Failed to fetch genres.")

if __name__ == "__main__":
    quick_test()