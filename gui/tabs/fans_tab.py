import customtkinter as ctk

class FansTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.section_fans = ctk.CTkLabel(self, text="Fans & Sensors", font=ctk.CTkFont(size=14, weight="bold"))
        self.section_fans.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")
        
        self.sensors_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.sensors_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.sensors_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.sensor_widgets = {}
        
        # Initial message
        self.no_data_lbl = ctk.CTkLabel(self.sensors_frame, text="Loading sensors...")
        self.no_data_lbl.grid(row=0, column=0, columnspan=2, pady=20)

    def get_temp_status(self, temp):
        if temp < 45: return "(Cool)"
        if temp < 75: return "(Warm)"
        return "(Hot)"

    def update_data_dynamic(self, info):
        fans = info.get("fans", [])
        
        if not fans:
            self.no_data_lbl.configure(text="No fan sensors detected on this system.")
            return

        self.no_data_lbl.grid_forget()
        
        for i, fan in enumerate(fans):
            name = fan["name"]
            reading = fan["reading"]
            unit = fan["unit"]
            
            status = ""
            if "Temperature" in name:
                status = f" {self.get_temp_status(reading)}"
            
            if name not in self.sensor_widgets:
                lbl = ctk.CTkLabel(self.sensors_frame, text=name, font=ctk.CTkFont(size=12, weight="bold"))
                lbl.grid(row=i, column=0, padx=20, pady=2, sticky="w")
                
                val = ctk.CTkLabel(self.sensors_frame, text=f"{reading} {unit}{status}")
                val.grid(row=i, column=1, padx=20, pady=2, sticky="e")
                
                self.sensor_widgets[name] = val
            else:
                self.sensor_widgets[name].configure(text=f"{reading} {unit}{status}")
