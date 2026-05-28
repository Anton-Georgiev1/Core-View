import customtkinter as ctk
from utils.cpu_info import get_cpu_info

class CPUTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure((0, 1), weight=1)
        
        # CPU Brand/Name
        self.brand_label = ctk.CTkLabel(self, text="Processor", font=ctk.CTkFont(size=14, weight="bold"))
        self.brand_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="w")
        
        self.brand_value = ctk.CTkLabel(self, text="Loading...", font=ctk.CTkFont(size=16))
        self.brand_value.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 10), sticky="w")

        # Architecture & Bits
        self.create_label_value("Architecture", 2, 0)
        self.arch_val = self.create_label_value("", 2, 1)
        
        # Cores & Threads
        self.create_label_value("Cores", 3, 0)
        self.cores_val = self.create_label_value("", 3, 1)
        
        self.create_label_value("Logical Processors", 4, 0)
        self.threads_val = self.create_label_value("", 4, 1)

        # Clocks
        self.create_label_value("Current Speed", 5, 0)
        self.clock_val = self.create_label_value("", 5, 1)
        
        self.create_label_value("Usage", 6, 0)
        self.usage_val = self.create_label_value("", 6, 1)

        self.update_info()

    def create_label_value(self, label_text, row, col):
        if label_text:
            lbl = ctk.CTkLabel(self, text=label_text, font=ctk.CTkFont(size=12, weight="bold"))
            lbl.grid(row=row, column=col, padx=10, pady=5, sticky="w")
            return None
        else:
            val = ctk.CTkLabel(self, text="Loading...")
            val.grid(row=row, column=col, padx=10, pady=5, sticky="e")
            return val

    def update_info(self):
        info = get_cpu_info()
        
        self.brand_value.configure(text=info["brand_raw"])
        
        if self.arch_val:
            self.arch_val.configure(text=f"{info['arch']} ({info['bits']} bit)")
        if self.cores_val:
            self.cores_val.configure(text=str(info["count"]))
        if self.threads_val:
            self.threads_val.configure(text=str(info["logical_count"]))
        if self.clock_val:
            self.clock_val.configure(text=f"{info['frequency_current']:.2f} MHz")
        if self.usage_val:
            self.usage_val.configure(text=f"{info['usage_percent']}%")
            
        # Schedule next update
        self.after(1000, self.update_info)
