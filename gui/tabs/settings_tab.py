import customtkinter as ctk

class SettingsTab(ctk.CTkFrame):
    def __init__(self, master, app_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.app_callback = app_callback
        
        self.grid_columnconfigure(0, weight=1)
        
        # Theme Section
        self.theme_label = ctk.CTkLabel(self, text="Appearance", font=ctk.CTkFont(size=14, weight="bold"))
        self.theme_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        self.theme_var = ctk.StringVar(value="Dark")
        self.dark_radio = ctk.CTkRadioButton(self, text="Dark Mode", variable=self.theme_var, value="Dark", command=self.update_theme)
        self.dark_radio.grid(row=1, column=0, padx=30, pady=5, sticky="w")
        
        self.light_radio = ctk.CTkRadioButton(self, text="Light Mode", variable=self.theme_var, value="Light", command=self.update_theme)
        self.light_radio.grid(row=2, column=0, padx=30, pady=5, sticky="w")
        
        # Tray Section
        self.tray_label = ctk.CTkLabel(self, text="Behavior", font=ctk.CTkFont(size=14, weight="bold"))
        self.tray_label.grid(row=3, column=0, padx=20, pady=(20, 10), sticky="w")
        
        self.tray_var = ctk.BooleanVar(value=True)
        self.tray_checkbox = ctk.CTkCheckBox(self, text="Minimize to Tray on Close", variable=self.tray_var, command=self.update_tray_opt)
        self.tray_checkbox.grid(row=4, column=0, padx=30, pady=5, sticky="w")

    def update_theme(self):
        self.app_callback("theme", self.theme_var.get())

    def update_tray_opt(self):
        self.app_callback("tray_on_close", self.tray_var.get())
