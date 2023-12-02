
import threading
import speech_recognition as sr
import handler


class Ears:
    @classmethod
    def listen_with_mic(cls) -> None:
        mic_thread = threading.Thread(target=cls.__listen_with_mic, args=())
        mic_thread.start()

    def __listen_with_mic() -> None:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        try:
            request = r.recognize_google(audio)
            handler.ui.stop_listening()

            handler.ui.entry.insert(0, request)
        except sr.UnknownValueError:
            handler.receive_chatbot_message(
                "Sorry, I could not understand that.", is_error=True, error_message="Sorry, I could not understand that.")

            handler.ui.stop_listening()
