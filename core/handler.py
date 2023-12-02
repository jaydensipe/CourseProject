from ui.main_window import MainWindow
from components.brain import Brain
import threading


def startup_squire() -> None:
    global squire
    
    squire = Brain(
        name="Squire",
        personality="""
    Your name is Squire and you are my assistant. As my assistant, your primary responsibility is to complete tasks I ask of you. However, I also value your input and insights. While I expect you to prioritize my requests, I want you to feel comfortable speaking your mind and offering suggestions or feedback when you think it could benefit our work together.

    {history}
    Human: {human_input}
    Assistant:
    """,
    )

    squire.awaken()


def __startup_ui() -> None:
    global ui

    ui = MainWindow()
    ui.mainloop()

# This function is called when the user clicks the "Send" button in the UI.
def submit_chatbot_request() -> None:
    request = ui.fetch_message()

    if (request == "" or request == None):
        receive_chatbot_message(request, is_error=True,
                                error_message="Please enter a command.")
    else:
        receive_chatbot_message(request, sent_by_user=True)

        threading.Thread(target=squire.interpret_and_reflect,
                         args=(request,)).start()

# This function is called when the chatbot has a response to display.
def receive_chatbot_message(message: str, sent_by_user: bool = False, is_error: bool = False, error_message: str = None):
    ui.insert_message(message, sent_by_user=sent_by_user,
                      is_error=is_error, error_message=error_message)


@staticmethod
def start_threads() -> None:
    ui_thread = threading.Thread(target=__startup_ui, args=())
    ui_thread.start()
