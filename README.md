# 🖥️ Core View

**A high-performance, real-time system monitoring tool for Windows.**

Core View is designed for power users and enthusiasts who need a fast, lightweight, and detailed overview of their system's performance and hardware health. Unlike heavy monitoring suites, Core View starts instantly and provides critical data with minimal system impact.

---

## ✨ Key Features

*   **⚡ Instant Startup:** Leverages multi-threaded asynchronous loading to display critical hardware info the moment you launch it.
*   **📊 Comprehensive Monitoring:**
    *   **CPU:** Detailed brand, architecture, core/thread counts, and real-time usage (Good/Moderate/High Load status).
    *   **Graphics:** Real-time GPU utilization and hardware name.
    *   **Memory RAM:** Total size and physical slot usage (know exactly how many sticks you have installed).
    *   **Storage:** Track capacity and usage percentage of your primary drive.
    *   **Fans & Sensors:** Real-time monitoring of fan speeds (RPM) and system temperatures (Cool/Warm/Hot status).
*   **📂 Intuitive Tabbed Interface:** Clean, organized categories for CPU, Mainboard, Memory, Graphics, and Fans.
*   **🌙 Modern UI:** Built with a beautiful dark-mode interface using `CustomTkinter`.
*   **📥 System Tray Integration:** Minimize to the system tray for unobtrusive background monitoring.

---

## 🛠️ Performance Optimization (Technical Deep Dive)

Core View has been meticulously optimized for responsiveness:
*   **Asynchronous Architecture:** Slow system calls (like PowerShell and WMI) are offloaded to dedicated background threads, ensuring the UI remains buttery smooth at 60+ FPS.
*   **Smart Caching:** Static hardware details are cached after the first retrieval, reducing unnecessary CPU overhead.
*   **Consolidated Fetching:** Multiple hardware sensor queries are combined into single, efficient system calls to minimize process-spawn latency.

---

## 🚀 Getting Started

### Prerequisites
*   Windows 10 or 11
*   Python 3.12+

### Installation
1.  Clone the repository:
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    [!NOTE]
    >Requirements include `customtkinter`, `psutil`, `py-cpuinfo`, `pystray`, and `Pillow`

3.  Run the application:
    ```bash
    python core_view.py
    ```

---

## 🧪 Testing

Core View includes a robust test suite to ensure reliability across different Windows configurations. To run the tests:
```bash
$env:PYTHONPATH='.'
pytest tests/
```

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

