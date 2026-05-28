import customtkinter as ctk
from gui.tabs.cpu_tab import CPUTab
from gui.tabs.mainboard_tab import MainboardTab
from gui.tabs.memory_tab import MemoryTab
from gui.tabs.graphics_tab import GraphicsTab
from gui.tabs.settings_tab import SettingsTab
import pystray
from PIL import Image, ImageDraw
import threading
import sys

class CoreViewApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Core View")
        self.geometry("500x400")
        
        # Disable maximize button and fix window size
        self.resizable(False, False)
        
        # Settings state
        self.minimize_to_tray = True
        
        # Appearance - Start with Dark
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Tabview
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # Tabs
        self.tabview.add("CPU")
        self.tabview.add("Mainboard")
        self.tabview.add("Memory")
        self.tabview.add("Graphics")
        self.tabview.add("Settings")

        # Tab contents
        self.cpu_tab = CPUTab(self.tabview.tab("CPU"))
        self.cpu_tab.pack(fill="both", expand=True)

        self.mb_tab = MainboardTab(self.tabview.tab("Mainboard"))
        self.mb_tab.pack(fill="both", expand=True)

        self.mem_tab = MemoryTab(self.tabview.tab("Memory"))
        self.mem_tab.pack(fill="both", expand=True)

        self.gpu_tab = GraphicsTab(self.tabview.tab("Graphics"))
        self.gpu_tab.pack(fill="both", expand=True)
        
        self.settings_tab = SettingsTab(self.tabview.tab("Settings"), self.settings_callback)
        self.settings_tab.pack(fill="both", expand=True)

        # System Tray Setup
        self.protocol('WM_DELETE_WINDOW', self.on_closing)
        self.create_tray_icon()

    def settings_callback(self, setting_type, value):
        if setting_type == "theme":
            ctk.set_appearance_mode(value)
        elif setting_type == "tray_on_close":
            self.minimize_to_tray = value

    def on_closing(self):
        if self.minimize_to_tray:
            self.withdraw()
        else:
            self.quit_app()

    def show_window(self):
        self.deiconify()
        self.lift()
        self.focus_force()

    def quit_app(self):
        if hasattr(self, 'tray_icon'):
            self.tray_icon.stop()
        self.destroy()
        sys.exit()

    def create_tray_icon(self):
        # Create a simple icon image
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), color=(0, 102, 204))
        dc = ImageDraw.Draw(image)
        dc.rectangle([width // 4, height // 4, width * 3 // 4, height * 3 // 4], fill=(255, 255, 255))
        
        menu = pystray.Menu(
            pystray.MenuItem("Show", self.show_window, default=True),
            pystray.MenuItem("Quit", self.quit_app)
        )
        
        self.tray_icon = pystray.Icon("CoreView", image, "Core View", menu)
        
        # Run tray in a separate thread
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

if __name__ == "__main__":
    app = CoreViewApp()
    app.mainloop()
