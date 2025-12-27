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
            raise ValueError("❌ GROQ_API_KEY is missing in .env file")
        
        self.client = Groq(api_key=api_key)
        
        # Using Llama 3.3 70B for superior reasoning and tool calling accuracy
        self.model = "llama-3.3-70b-versatile" 
       
        self.tools = MovieTools()
        
        # Load the system prompt containing CoT instructions and visual formatting rules
        with open("prompts/system_prompt.txt", "r", encoding="utf-8") as f:
            system_content = f.read()
            
        self.history = [
            {"role": "system", "content": system_content}
        ]

    def chat(self, user_input):
        self.history.append({"role": "user", "content": user_input})
        
        # STEP 1: Thought & Action
        # The model analyzes the request and decides which tool to invoke
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.history,
            tools=MOVIE_TOOLS_SCHEMA,
            tool_choice="auto",
            temperature=0.1 # Low temperature for consistent reasoning
        )

        response_message = response.choices[0].message
        
        # Display the Agent's internal thought process if provided
        if response_message.content:
            print(f"\n🧠 [Agent Thought]: {response_message.content}")
        
        # Append assistant message (including tool calls) to history - Essential for multi-turn LLM Tool Calling
        self.history.append(response_message)

        # STEP 2: Execution & Observation
        if response_message.tool_calls:
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                
                print(f"🎬 [Action]: Executing {function_name}...")
                
                # Dynamic Tool Execution logic
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

                # Return the Observation (API result) back to the model
                self.history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": json.dumps(result)
                })

            # STEP 3: Final Verification & Response Synthesis
            # The model reviews the observations and formulates a grounded response
            final_response = self.client.chat.completions.create(
                model=self.model,
                messages=self.history
            )
            ans = final_response.choices[0].message.content
            self.history.append({"role": "assistant", "content": ans})
            return ans
        
        # Fallback if no tool calls were generated (e.g., general greetings or out-of-scope topics)
        ans = response_message.content
        self.history.append({"role": "assistant", "content": ans})
        return ans