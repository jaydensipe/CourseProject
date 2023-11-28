from ui.main_window import MainWindow
from components.brain import Brain
import threading
import speech_recognition as sr

squire = Brain(
    name="Squire",
    personality="""
    Your name is Squire and you are my assistant. As my assistant, your primary responsibility is to complete tasks I ask of you. However, I also value your input and insights. While I expect you to prioritize my requests, I want you to feel comfortable speaking your mind and offering suggestions or feedback when you think it could benefit our work together.

    {history}
    Human: {human_input}
    Assistant:
    """,
)


def startup_squire() -> None:
    squire.awaken()


def __startup_ui() -> None:
    global ui

    ui = MainWindow()
    ui.mainloop()


def submit_chatbot_request() -> None:
    request = ui.fetch_message()

    if (request == "" or request == None):
        receive_chatbot_message(request, is_error=True,
                                error_message="Please enter a command.")
    else:
        receive_chatbot_message(request, sent_by_user=True)

        threading.Thread(target=squire.interpret_and_reflect,
                         args=(request,)).start()


def receive_chatbot_message(message: str, sent_by_user: bool = False, is_error: bool = False, error_message: str = None):
    ui.insert_message(message, sent_by_user=sent_by_user,
                      is_error=is_error, error_message=error_message)


def listen_with_mic() -> None:
    mic_thread = threading.Thread(target=__listen_with_mic, args=())
    mic_thread.start()


def __listen_with_mic() -> None:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        request = r.recognize_google(audio)
        ui.stop_listening()

        ui.entry.insert(0, request)
    except sr.UnknownValueError:
        receive_chatbot_message(
            "Sorry, I could not understand that.", is_error=True, error_message="Sorry, I could not understand that.")

        ui.stop_listening()


@staticmethod
def start_threads() -> None:
    ui_thread = threading.Thread(target=__startup_ui, args=())
    ui_thread.start()
