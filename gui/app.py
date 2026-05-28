import customtkinter as ctk
from gui.tabs.cpu_tab import CPUTab
from gui.tabs.mainboard_tab import MainboardTab
from gui.tabs.memory_tab import MemoryTab
from gui.tabs.graphics_tab import GraphicsTab
from gui.tabs.about_tab import AboutTab

class CoreViewApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Core View")
        self.geometry("500x400")
        
        # Appearance
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Tabview
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # Tabs
        self.tabview.add("CPU")
        self.tabview.add("Mainboard")
        self.tabview.add("Memory")
        self.tabview.add("Graphics")
        self.tabview.add("About")

        # Tab contents
        self.cpu_tab = CPUTab(self.tabview.tab("CPU"))
        self.cpu_tab.pack(fill="both", expand=True)

        self.mb_tab = MainboardTab(self.tabview.tab("Mainboard"))
        self.mb_tab.pack(fill="both", expand=True)

        self.mem_tab = MemoryTab(self.tabview.tab("Memory"))
        self.mem_tab.pack(fill="both", expand=True)

        self.gpu_tab = GraphicsTab(self.tabview.tab("Graphics"))
        self.gpu_tab.pack(fill="both", expand=True)

        self.about_tab = AboutTab(self.tabview.tab("About"))
        self.about_tab.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = CoreViewApp()
    app.mainloop()
