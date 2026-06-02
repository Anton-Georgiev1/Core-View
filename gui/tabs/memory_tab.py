import customtkinter as ctk

class MemoryTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure((0, 1), weight=1)
        
        self.section_mem = ctk.CTkLabel(self, text="Memory RAM", font=ctk.CTkFont(size=14, weight="bold"))
        self.section_mem.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")
        
        self.mem_size_val = self.create_info_row("Total Size", "Loading...", 1)
        self.ram_slots_val = self.create_info_row("RAM Slots", "Loading...", 2)

        # Storage Section
        self.section_storage = ctk.CTkLabel(self, text="Storage", font=ctk.CTkFont(size=14, weight="bold"))
        self.section_storage.grid(row=3, column=0, columnspan=2, padx=10, pady=(20, 5), sticky="w")
        
        self.disk_total_val = self.create_info_row("Total Capacity", "Loading...", 4)
        self.disk_used_val = self.create_info_row("Used", "Loading...", 5)
        self.disk_free_val = self.create_info_row("Free", "Loading...", 6)
        self.disk_usage_val = self.create_info_row("Usage Percent", "Loading...", 7)

    def create_info_row(self, label, value, row):
        lbl = ctk.CTkLabel(self, text=label, font=ctk.CTkFont(size=12, weight="bold"))
        lbl.grid(row=row, column=0, padx=20, pady=2, sticky="w")
        
        val = ctk.CTkLabel(self, text=value)
        val.grid(row=row, column=1, padx=20, pady=2, sticky="e")
        return val

    def update_data(self, info):
        self.mem_size_val.configure(text=f"{info['total_ram']} GB")
        self.ram_slots_val.configure(text=f"{info['ram_slots_filled']} / {info['ram_slots_total']} slots")
        
        self.disk_total_val.configure(text=f"{info['disk_total']} GB")
        self.disk_used_val.configure(text=f"{info['disk_used']} GB")
        self.disk_free_val.configure(text=f"{info['disk_free']} GB")
        self.disk_usage_val.configure(text=f"{info['disk_percent']}%")
