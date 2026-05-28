import customtkinter as ctk
from utils.sys_info import get_sys_info

class MainboardTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure((0, 1), weight=1)
        
        info = get_sys_info()
        
        # Motherboard Section
        self.section_mb = ctk.CTkLabel(self, text="Motherboard", font=ctk.CTkFont(size=14, weight="bold"))
        self.section_mb.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")
        
        self.create_info_row("Manufacturer", info["mb_manufacturer"], 1)
        self.create_info_row("Model", info["mb_product"], 2)
        self.create_info_row("Version", info["mb_version"], 3)
        
        # BIOS Section
        self.section_bios = ctk.CTkLabel(self, text="BIOS", font=ctk.CTkFont(size=14, weight="bold"))
        self.section_bios.grid(row=4, column=0, columnspan=2, padx=10, pady=(15, 5), sticky="w")
        
        self.create_info_row("Brand", info["bios_vendor"], 5)
        self.create_info_row("Version", info["bios_version"], 6)
        self.create_info_row("Date", info["bios_date"], 7)

    def create_info_row(self, label, value, row):
        lbl = ctk.CTkLabel(self, text=label, font=ctk.CTkFont(size=12, weight="bold"))
        lbl.grid(row=row, column=0, padx=20, pady=2, sticky="w")
        
        val = ctk.CTkLabel(self, text=value)
        val.grid(row=row, column=1, padx=20, pady=2, sticky="e")
