import customtkinter
import handler

# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("Dark")

# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("blue")

customtkinter.set_widget_scaling(float(1.3))


class MainWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Squire: Chat Assistant")
        self.geometry(f"{1280}x{720}")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(
            self, width=140, corner_radius=0)

        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Settings", font=customtkinter.CTkFont(size=24, weight="bold"))

        self.logo_label.grid(row=0, column=0, padx=10, pady=(20, 10))

        self.appearance_mode_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Appearance Mode:", anchor="w")

        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))

        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(
            row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["1.0x", "1.1x", "1.2x", "1.3x"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # Create main entry and button
        self.entry = customtkinter.CTkEntry(
            self, placeholder_text="Please type a command...")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(
            20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(text="Submit",
                                                     master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=handler.submit_chatbot_request)

        self.main_button_1.grid(row=3, column=3, padx=(
            20, 20), pady=(20, 20), sticky="nsew")

        # Create textbox
        self.textbox = customtkinter.CTkScrollableFrame(self, width=300)
        self.textbox.grid(row=0, column=1, columnspan=3, padx=(
            20, 0), pady=(20, 0), sticky="nsew")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = float(new_scaling.replace("x", ""))
        customtkinter.set_widget_scaling(float(new_scaling_float) + 0.3)

    from PIL import Image, ImageTk
    from tkinter import LEFT

    def insert_message(self, message: str, sent_by_user: bool = False):
        frame = customtkinter.CTkFrame(self.textbox)
        frame.pack(fill='x')

        # Create the text label
        if sent_by_user:
            label = customtkinter.CTkLabel(frame, text=message, anchor='e')
        else:
            label = customtkinter.CTkLabel(frame, text="🤖" + message, anchor='w')

        label.pack(fill='x')