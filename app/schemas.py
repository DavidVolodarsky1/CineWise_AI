# app/schemas.py

MOVIE_TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "search_movie",
            "description": "Search for a movie by its title to get details like rating and overview.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "The movie name in Hebrew or English"}
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "discover_movies",
            "description": "Discover movies based on genre ID, release year, or popularity.",
            "parameters": {
                "type": "object",
                "properties": {
                    "genre_id": {"type": "integer", "description": "The TMDB genre ID"},
                    "year": {"type": "integer", "description": "Release year (e.g. 1994)"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_watch_providers",
            "description": "Check where a movie is available for streaming, rent or buy in Israel.",
            "parameters": {
                "type": "object",
                "properties": {
                    "movie_title": {"type": "string", "description": "The exact movie title"}
                },
                "required": ["movie_title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_genres",
            "description": "Fetch the complete list of movie genres and their corresponding IDs.",
            "parameters": {"type": "object", "properties": {}}
        }
    }
]