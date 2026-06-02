import customtkinter as ctk

class MainboardTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure((0, 1), weight=1)
        
        # Motherboard Section
        self.section_mb = ctk.CTkLabel(self, text="Motherboard", font=ctk.CTkFont(size=14, weight="bold"))
        self.section_mb.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")
        
        self.mb_man_val = self.create_info_row("Manufacturer", "Loading...", 1)
        self.mb_prod_val = self.create_info_row("Model", "Loading...", 2)
        self.mb_ver_val = self.create_info_row("Version", "Loading...", 3)
        
        # BIOS Section
        self.section_bios = ctk.CTkLabel(self, text="BIOS", font=ctk.CTkFont(size=14, weight="bold"))
        self.section_bios.grid(row=4, column=0, columnspan=2, padx=10, pady=(15, 5), sticky="w")
        
        self.bios_brand_val = self.create_info_row("Brand", "Loading...", 5)
        self.bios_ver_val = self.create_info_row("Version", "Loading...", 6)
        self.bios_date_val = self.create_info_row("Date", "Loading...", 7)

    def create_info_row(self, label, value, row):
        lbl = ctk.CTkLabel(self, text=label, font=ctk.CTkFont(size=12, weight="bold"))
        lbl.grid(row=row, column=0, padx=20, pady=2, sticky="w")
        
        val = ctk.CTkLabel(self, text=value)
        val.grid(row=row, column=1, padx=20, pady=2, sticky="e")
        return val

    def update_data(self, info):
        self.mb_man_val.configure(text=info["mb_manufacturer"])
        self.mb_prod_val.configure(text=info["mb_product"])
        self.mb_ver_val.configure(text=info["mb_version"])
        self.bios_brand_val.configure(text=info["bios_vendor"])
        self.bios_ver_val.configure(text=info["bios_version"])
        self.bios_date_val.configure(text=info["bios_date"])
