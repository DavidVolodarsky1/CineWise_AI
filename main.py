from app.agent import CineWiseAgent
from dotenv import load_dotenv

load_dotenv()

def main():
    agent = CineWiseAgent()
    print("--- 🎬 CineWise AI: סוכן הסרטים האישי שלך מוכן! ---")
    print("(הקלד 'יציאה' כדי לסיים)")

    while True:
        user_input = input("\n👤 אתה: ")
        if user_input.lower() in ["יציאה", "exit", "quit"]:
            break
        
        try:
            response = agent.chat(user_input)
            print(f"\n🤖 CineWise: {response}")
        except Exception as e:
            print(f"\n❌ שגיאה: {e}")

if __name__ == "__main__":
    main()