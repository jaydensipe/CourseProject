import handler

class Mouth:
    
    # Speak words
    @staticmethod
    def speak(words: str) -> None:
        print("Squire: " + words)
        
        handler.receive_chatbot_message(message=words)
