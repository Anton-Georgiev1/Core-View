import customtkinter as ctk
from gui.tabs.cpu_tab import CPUTab
from gui.tabs.mainboard_tab import MainboardTab
from gui.tabs.memory_tab import MemoryTab
from gui.tabs.graphics_tab import GraphicsTab
from gui.tabs.fans_tab import FansTab
from gui.tabs.settings_tab import SettingsTab
from utils.cpu_info import get_cpu_info
from utils.sys_info import get_sys_info, update_sys_info_async
from utils.dynamic_info import get_dynamic_info
import pystray
from PIL import Image, ImageDraw
import threading
import time
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

        # Shared data
        self.latest_cpu_info = None
        self.latest_sys_info = None
        self.latest_dynamic_info = {"gpu_usage": 0.0, "fans": []}

        # Tabview
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # Tabs
        self.tabview.add("CPU")
        self.tabview.add("Mainboard")
        self.tabview.add("Memory")
        self.tabview.add("Graphics")
        self.tabview.add("Fans")
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
        
        self.fans_tab = FansTab(self.tabview.tab("Fans"))
        self.fans_tab.pack(fill="both", expand=True)
        
        self.settings_tab = SettingsTab(self.tabview.tab("Settings"), self.settings_callback)
        self.settings_tab.pack(fill="both", expand=True)

        # System Tray Setup
        self.protocol('WM_DELETE_WINDOW', self.on_closing)
        self.create_tray_icon()

        # Start fast data loading
        self.load_initial_data()
        
        # Start background threads for slow data
        threading.Thread(target=self.background_static_loader, daemon=True).start()
        threading.Thread(target=self.background_dynamic_loader, daemon=True).start()
        
        # Start UI update loops
        self.update_ui_loop()

    def load_initial_data(self):
        # Fetch only fast registry/psutil data initially
        self.latest_sys_info = get_sys_info()
        self.update_tabs_static()

    def background_static_loader(self):
        # This thread fetches slow static info (py-cpuinfo, slow WMI)
        self.latest_cpu_info = get_cpu_info() # py-cpuinfo call
        self.latest_sys_info = update_sys_info_async() # PowerShell call for RAM slots
        self.after(0, self.update_tabs_static)

    def background_dynamic_loader(self):
        # This thread periodically fetches GPU/Fan info via PowerShell
        while True:
            self.latest_dynamic_info = get_dynamic_info()
            time.sleep(2) # Refresh every 2 seconds

    def update_ui_loop(self):
        # Update fast dynamic info (CPU usage)
        self.latest_cpu_info = get_cpu_info()
        
        # Refresh all tabs with latest available data
        self.cpu_tab.update_data(self.latest_cpu_info)
        self.gpu_tab.update_data_dynamic(self.latest_dynamic_info)
        self.fans_tab.update_data_dynamic(self.latest_dynamic_info)
        
        self.after(1000, self.update_ui_loop)

    def update_tabs_static(self):
        if self.latest_sys_info:
            self.mb_tab.update_data(self.latest_sys_info)
            self.mem_tab.update_data(self.latest_sys_info)
            self.gpu_tab.update_data(self.latest_sys_info)
        if self.latest_cpu_info:
            self.cpu_tab.update_data(self.latest_cpu_info)

    def settings_callback(self, setting_type, value):
        if setting_type == "theme":
            ctk.set_appearance_mode(value)
        elif setting_type == "minimize_now":
            self.withdraw()

    def on_closing(self):
        # Exit the application when X is clicked
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
