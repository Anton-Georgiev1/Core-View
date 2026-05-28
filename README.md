# Core View

Core View is a modern, lightweight, and visually polished system information utility for Windows, inspired by the classic CPU-Z. Built with **CustomTkinter**, it provides a sleek, high-DPI responsive interface that feels at home on modern desktop environments.

Whether you're an enthusiast monitoring your overclock or a developer needing quick hardware specs, Core View delivers essential system data with a "set it and forget it" efficiency.

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat&logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=flat&logo=windows&logoColor=white)

---

## Key Features

- **Real-time CPU Monitoring:** Live tracking of clock speeds and processor usage.
- **Deep Hardware Discovery:** Detailed metadata for your Processor, Motherboard, BIOS, RAM, and GPU.
- **Modern UI/UX:**
  - **Dark & Light Themes:** Toggle between modes to suit your workspace.
  - **Fixed Precision Layout:** A non-resizable, focused window that prevents clutter.
  - **System Tray Integration:** Minimize the app to the tray to keep your taskbar clean while it runs in the background.
- **Efficient Data Gathering:** Uses a blend of `psutil`, `py-cpuinfo`, and native Windows PowerShell (CIM) queries for accurate hardware reporting without the bloat.

## Preview

*The application features a tabbed interface:*
1. **CPU:** Architecture, Cores, Threads, and live Frequency.
2. **Mainboard:** Manufacturer, Model, and BIOS version/date.
3. **Memory:** Total physical RAM capacity.
4. **Graphics:** Integrated and Dedicated GPU identification.
5. **Settings:** Toggle themes and background behavior.

## Getting Started

### Prerequisites
- **Windows OS** (Required for hardware discovery modules)
- **Python 3.12 or higher**

### Installation

1. **Clone the repository:**
2. **Install dependencies:**
   ```bash
   pip install customtkinter psutil py-cpuinfo pystray pillow
   ```

3. **Run the application:**
   ```bash
   python core_view.py
   ```

## Built With

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern UI components for Tkinter.
- [psutil](https://github.com/giampaolo/psutil) - Cross-platform lib for process and system monitoring.
- [py-cpuinfo](https://github.com/workhorse/py-cpuinfo) - Detailed CPU info gathering.
- [Pystray](https://github.com/moses-palmer/pystray) - System tray icon support.

## License

This project is open-source and available under the [MIT License](LICENSE).

---

