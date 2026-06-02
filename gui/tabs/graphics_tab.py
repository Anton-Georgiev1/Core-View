import customtkinter as ctk

class GraphicsTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure((0, 1), weight=1)
        
        self.section_gpu = ctk.CTkLabel(self, text="Display Device", font=ctk.CTkFont(size=14, weight="bold"))
        self.section_gpu.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")
        
        self.gpu_name_val = self.create_info_row("Name", "Loading...", 1)
        self.gpu_usage_val = self.create_info_row("Usage", "Loading...", 2)

    def create_info_row(self, label, value, row):
        lbl = ctk.CTkLabel(self, text=label, font=ctk.CTkFont(size=12, weight="bold"))
        lbl.grid(row=row, column=0, padx=20, pady=2, sticky="w")
        
        val = ctk.CTkLabel(self, text=value)
        val.grid(row=row, column=1, padx=20, pady=2, sticky="e")
        return val

    def update_data(self, info):
        self.gpu_name_val.configure(text=info["gpu_name"])

    def update_data_dynamic(self, info):
        # Update GPU usage from dynamic data
        self.gpu_usage_val.configure(text=f"{info['gpu_usage']}%")
