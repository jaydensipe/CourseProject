import handler


class Mouth:

    # Speak words
    @staticmethod
    def speak(words: str, is_error: bool = False) -> None:
        if (words == "" or words == None):
            return

        if is_error:
            handler.receive_chatbot_message(
                message=words, is_error=True, error_message=words)
        else:
            handler.receive_chatbot_message(message=words)

        print("Squire: " + words)
