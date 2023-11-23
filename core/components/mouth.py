import handler


class Mouth:

    # Speak words
    @staticmethod
    def speak(words: str, is_error: bool = False) -> None:
        if (words == "" or words == None):
            return

        handler.receive_chatbot_message(
            message=words, is_error=is_error, error_message=words)

        print("Squire: " + words)
