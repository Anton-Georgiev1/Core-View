import customtkinter as ctk
from utils.sys_info import get_sys_info

class GraphicsTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure((0, 1), weight=1)
        
        info = get_sys_info()
        
        self.section_gpu = ctk.CTkLabel(self, text="Display Device", font=ctk.CTkFont(size=14, weight="bold"))
        self.section_gpu.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")
        
        self.create_info_row("Name", info["gpu_name"], 1)

    def create_info_row(self, label, value, row):
        lbl = ctk.CTkLabel(self, text=label, font=ctk.CTkFont(size=12, weight="bold"))
        lbl.grid(row=row, column=0, padx=20, pady=2, sticky="w")
        
        val = ctk.CTkLabel(self, text=value)
        val.grid(row=row, column=1, padx=20, pady=2, sticky="e")
