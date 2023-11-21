import handler


class Mouth:

    # Speak words
    @staticmethod
    def speak(words: str) -> None:
        if (words == "" or words == None):
            return
        
        print("Squire: " + words)

        handler.receive_chatbot_message(message=words)
