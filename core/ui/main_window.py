import datetime
import customtkinter
import handler

# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("Dark")

# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("core/ui/custom_theme.json")

customtkinter.set_widget_scaling(float(1.3))

last_sent_time_message = datetime.datetime.now()


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
            self, placeholder_text="Please type a command...", corner_radius=8, border_width=0)
        self.entry.grid(row=3, column=1, columnspan=2, padx=(
            20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(text="Submit",
                                                     master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=handler.submit_chatbot_request)

        self.main_button_1.grid(row=3, column=3, padx=(
            20, 20), pady=(20, 20), sticky="nsew")

        self.bind('<Return>', lambda event: handler.submit_chatbot_request())

        # Create textbox
        self.textbox = customtkinter.CTkScrollableFrame(self, width=300)
        self.textbox.grid(row=0, rowspan=2, column=1, columnspan=3, padx=(
            20, 20), pady=(20, 0), sticky="nsew")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = float(new_scaling.replace("x", ""))
        customtkinter.set_widget_scaling(float(new_scaling_float) + 0.3)

    def insert_message(self, message: str, sent_by_user: bool = False, is_error: bool = False, error_message: str = None):
        frame = customtkinter.CTkFrame(self.textbox)
        frame.pack(fill='x')

        # TODO: FIX THIS
        # Create the timestamp label
        if (last_sent_time_message + datetime.timedelta(seconds=5) > datetime.datetime.now()):
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
        label.bind('<Configure>', lambda event: label.configure(
            wraplength=label.winfo_width()))
