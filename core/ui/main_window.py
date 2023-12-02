import datetime
import customtkinter
import handler
from components.ears import Ears
from PIL import Image
from external.external import save_external_api_tokens, get_external_api_tokens

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("core/ui/custom_theme.json")
customtkinter.set_widget_scaling(float(1.3))


class MainWindow(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configure window
        self.title("Squire: Chat Assistant")
        self.last_sent_time_message = datetime.datetime.now()
        self.geometry(f"{1280}x{720}")
        self.minsize(800, 600)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(
            self, width=140, corner_radius=0)

        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Integrations", font=customtkinter.CTkFont(size=24, weight="bold", underline=True))

        self.logo_label.grid(row=0, column=0, padx=10, pady=(20, 0))

        # External Integrations
        self.load_external_api_buttons()

        self.appearance_mode_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Appearance Mode:", anchor="w")

        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))

        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"],
                                                                       command=self.__change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(
            row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["1.0x", "1.1x", "1.2x", "1.3x"],
                                                               command=self.__change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # Create main entry and button
        self.entry = customtkinter.CTkEntry(
            self, placeholder_text="Please type a command...", corner_radius=8, border_width=0)
        self.entry.grid(row=3, column=1, columnspan=2, padx=(
            20, 0), pady=(20, 20), sticky="nsew")

        self.button_image = customtkinter.CTkImage(
            Image.open("core/ui/images/mic.png"), size=(18, 18))

        self.mic_button = customtkinter.CTkButton(
            master=self, text="", width=24, height=24, image=self.button_image, border_width=2, command=self.__listen_with_mic)
        self.mic_button.grid(row=3, column=3, padx=(
            20, 0), pady=(20, 20), sticky="nsew")

        self.is_talking = False

        self.original_fg_color = self.mic_button.cget('fg_color')

        self.main_button_1 = customtkinter.CTkButton(text="Submit",
                                                     master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=handler.submit_chatbot_request)

        self.main_button_1.grid(row=3, column=4, padx=(
            20, 20), pady=(20, 20), sticky="nsew")

        self.bind('<Return>', lambda event: handler.submit_chatbot_request())

        # Create textbox
        self.textbox = customtkinter.CTkScrollableFrame(self, width=300)
        self.textbox.grid(row=0, rowspan=2, column=1, columnspan=4, padx=(
            20, 20), pady=(20, 0), sticky="nsew")

    def __change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def __change_scaling_event(self, new_scaling: str):
        new_scaling_float = float(new_scaling.replace("x", ""))
        customtkinter.set_widget_scaling(float(new_scaling_float) + 0.3)

    def fetch_message(self) -> str:
        msg = self.entry.get()
        self.entry.delete(0, "end")

        return msg

    def __listen_with_mic(self) -> None:
        if (self.is_talking):
            self.stop_listening()
            return

        self.is_talking = True
        self.mic_button.configure(fg_color="red")
        self.entry.delete(0, 'end')
        self.entry.insert(0, "Listening...")
        self.entry.configure(state="disabled")
        self.main_button_1.configure(state="disabled")

        Ears.listen_with_mic()

    def stop_listening(self) -> None:
        self.is_talking = False

        self.entry.configure(state="normal")
        self.entry.delete(0, 'end')
        self.main_button_1.configure(state="normal")

        self.mic_button.configure(fg_color=self.original_fg_color)

    def insert_message(self, message: str, sent_by_user: bool = False, is_error: bool = False, error_message: str = None):
        frame = customtkinter.CTkFrame(self.textbox)
        frame.pack(fill='x')

        # Create the timestamp label
        if (self.last_sent_time_message + datetime.timedelta(seconds=10) < datetime.datetime.now()):
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            timestamp_label = customtkinter.CTkLabel(frame, text=timestamp)
            timestamp_label.pack()

        # Create the text label
        if sent_by_user:
            label = customtkinter.CTkLabel(frame, text=message.strip(
            ), anchor='e', fg_color=("#b9becc", "#112546"), corner_radius=8)
            label.pack(anchor='e', padx=10, pady=10)
        else:
            if (is_error):
                label = customtkinter.CTkLabel(frame, text=error_message.strip(
                ), anchor='w', fg_color=("#e57266", "#e74c3c"), corner_radius=8)
            else:
                label = customtkinter.CTkLabel(frame, text=message.strip(
                ), anchor='w', fg_color=("#f0f5ff", "#6993ff"), corner_radius=8)
            label.pack(anchor='w', padx=10, pady=10, ipadx=10, ipady=10)

        self.textbox._parent_canvas.yview_moveto(1.0)

        # Bind a function to the <Configure> event
        frame.bind('<Configure>', lambda event: label.configure(
            wraplength=frame.winfo_width() - 300))

        self.last_sent_time_message = datetime.datetime.now()

    def load_external_api_buttons(self) -> None:
        pady = 0
        for key, value in get_external_api_tokens().items():
            if (value and value != ''):
                customtkinter.CTkButton(text=str.upper(key),
                                        master=self, fg_color="#06b006", border_width=2, text_color=("gray10", "#DCE4EE"), command=lambda key=key: self.set_external_api(key)).grid(row=0, column=0, padx=(
                                            20, 20), pady=(pady, 0))
            else:
                customtkinter.CTkButton(text=str.upper(key),
                                        master=self, fg_color="#b00606", border_width=2, text_color=("gray10", "#DCE4EE"), command=lambda key=key: self.set_external_api(key)).grid(row=0, column=0, padx=(
                                            20, 20), pady=(pady, 0))

            pady += 100

    def set_external_api(self, api: str) -> None:
        dialog = customtkinter.CTkInputDialog(
            text="Enter in your API key for " + str.upper(api) + ":", title="API Key Input")

        save_external_api_tokens(api, dialog.get_input())

        self.load_external_api_buttons()
