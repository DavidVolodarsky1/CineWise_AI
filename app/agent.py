import os
import json
from groq import Groq
from app.tools import MovieTools
from app.schemas import MOVIE_TOOLS_SCHEMA
from dotenv import load_dotenv

load_dotenv()

class CineWiseAgent:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("❌ GROQ_API_KEY חסר בקובץ .env")
        
        self.client = Groq(api_key=api_key)
        # שימוש במודל 70B כדי להבטיח יכולות Reasoning גבוהות
        # self.model = "llama-3.3-70b-versatile" 
        # שנה את השורה הזו:
        self.model = "llama-3.1-8b-instant"
        
        self.tools = MovieTools()
        
        # טעינת הפרומפט המעודכן (עם הוראות ה-CoT וה-Verification)
        with open("prompts/system_prompt.txt", "r", encoding="utf-8") as f:
            system_content = f.read()
            
        self.history = [
            {"role": "system", "content": system_content}
        ]

    def chat(self, user_input):
        self.history.append({"role": "user", "content": user_input})
        
        # שלב 1: Thought & Action
        # המודל מנתח את הבקשה ומחליט אם להפעיל כלי
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.history,
            tools=MOVIE_TOOLS_SCHEMA,
            tool_choice="auto",
            temperature=0.1 # טמפרטורה נמוכה לדיוק ב-Reasoning
        )

        response_message = response.choices[0].message
        
        # הצגת ה-Thought של הסוכן (אם הוא כתב כזה לפני הקריאה לכלי)
        if response_message.content:
            print(f"\n🧠 [Agent Thought]: {response_message.content}")
        
        # הוספת הודעת האסיסטנט (כולל ה-Tool Calls) להיסטוריה - קריטי ל-LLM Tool Calling
        self.history.append(response_message)

        # שלב 2: Execution & Observation
        if response_message.tool_calls:
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                
                print(f"🎬 [Action]: מפעיל {function_name}...")
                
                # הרצת הכלי
                if function_name == "search_movie":
                    result = self.tools.search_movie(**args)
                elif function_name == "discover_movies":
                    result = self.tools.discover_movies(**args)
                elif function_name == "get_genres":
                    result = self.tools.get_genres()
                elif function_name == "get_watch_providers":
                    result = self.tools.get_watch_providers(**args)
                else:
                    result = {"error": "Tool not found"}

                # החזרת ה-Observation (התוצאה) למודל
                self.history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": json.dumps(result)
                })

            # שלב 3: Final Verification & Response
            # המודל בוחן את התוצאות ומנסח תשובה סופית למשתמש
            final_response = self.client.chat.completions.create(
                model=self.model,
                messages=self.history
            )
            ans = final_response.choices[0].message.content
            self.history.append({"role": "assistant", "content": ans})
            return ans
        
        # אם לא היו Tool Calls, פשוט מחזירים את התשובה (כמו במקרה של "פסטה")
        ans = response_message.content
        self.history.append({"role": "assistant", "content": ans})
        return ans