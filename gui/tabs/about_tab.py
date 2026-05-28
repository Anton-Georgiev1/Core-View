import customtkinter as ctk

class AboutTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.label = ctk.CTkLabel(self, text="Core View (CPU-Z Clone)", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.pack(pady=20)
        
        self.desc = ctk.CTkLabel(self, text="A modern system information tool built with CustomTkinter.", font=ctk.CTkFont(size=14))
        self.desc.pack(pady=10)
        
        self.version = ctk.CTkLabel(self, text="Version 1.0.0", font=ctk.CTkFont(size=12))
        self.version.pack(pady=5)
