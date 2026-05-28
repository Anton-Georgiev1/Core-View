import subprocess
import psutil
from typing import TypedDict

class SysData(TypedDict):
    mb_manufacturer: str
    mb_product: str
    mb_version: str
    bios_vendor: str
    bios_version: str
    bios_date: str
    total_ram: float
    gpu_name: str

def _run_powershell(command: str) -> str:
    """Helper to run PowerShell commands and return output."""
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", command],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception:
        return "Unknown"

def get_sys_info() -> SysData:
    """
    Fetches Motherboard, BIOS, RAM, and GPU information using PowerShell.
    """
    # Motherboard
    mb_manufacturer = _run_powershell("(Get-CimInstance Win32_BaseBoard).Manufacturer")
    mb_product = _run_powershell("(Get-CimInstance Win32_BaseBoard).Product")
    mb_version = _run_powershell("(Get-CimInstance Win32_BaseBoard).Version")
    
    # BIOS
    bios_vendor = _run_powershell("(Get-CimInstance Win32_BIOS).Manufacturer")
    bios_version = _run_powershell("(Get-CimInstance Win32_BIOS).SMBIOSBIOSVersion")
    bios_date_raw = _run_powershell("(Get-CimInstance Win32_BIOS).ReleaseDate.ToString('yyyy-MM-dd')")
    bios_date = bios_date_raw if bios_date_raw != "Unknown" else "Unknown"

    # RAM
    mem = psutil.virtual_memory()
    total_ram_gb = round(mem.total / (1024**3), 2)

    # GPU
    gpu_name = _run_powershell("(Get-CimInstance Win32_VideoController).Name")

    return {
        "mb_manufacturer": mb_manufacturer,
        "mb_product": mb_product,
        "mb_version": mb_version,
        "bios_vendor": bios_vendor,
        "bios_version": bios_version,
        "bios_date": bios_date,
        "total_ram": total_ram_gb,
        "gpu_name": gpu_name
    }

if __name__ == "__main__":
    import pprint
    pprint.pprint(get_sys_info())
