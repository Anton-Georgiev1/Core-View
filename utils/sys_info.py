import subprocess
import psutil
import winreg
import json
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
    disk_total: float
    disk_used: float
    disk_free: float
    disk_percent: float
    ram_slots_total: int
    ram_slots_filled: int

class FanData(TypedDict):
    name: str
    reading: float
    unit: str

def get_fan_info() -> list[FanData]:
    """
    Attempts to fetch fan and thermal sensor information using WMI.
    Since this is highly system-dependent, it tries common classes.
    """
    fans = []
    # Try HP specific namespace if present (found during research)
    try:
        cmd = "Get-CimInstance -Namespace root/HP/InstrumentedBIOS -ClassName HP_BIOSNumericSensor | Select-Object Name, CurrentReading, Unit | ConvertTo-Json"
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", cmd],
            capture_output=True,
            text=True,
            check=False
        )
        if result.stdout.strip():
            try:
                data = json.loads(result.stdout)
                if isinstance(data, dict):
                    data = [data]
                for item in data:
                    fans.append({
                        "name": item.get("Name", "Unknown Sensor"),
                        "reading": float(item.get("CurrentReading", 0)),
                        "unit": item.get("Unit") or ("RPM" if "Fan" in item.get("Name", "") else "°C")
                    })
            except (json.JSONDecodeError, ValueError, TypeError):
                pass
    except Exception:
        pass
    
    # Fallback to Win32_Fan (often empty but standard)
    if not fans:
        try:
            cmd = "Get-CimInstance Win32_Fan | Select-Object Name, VariableSpeed, DesiredSpeed | ConvertTo-Json"
            result = subprocess.run(
                ["powershell", "-NoProfile", "-Command", cmd],
                capture_output=True,
                text=True,
                check=False
            )
            if result.stdout.strip():
                try:
                    data = json.loads(result.stdout)
                    if isinstance(data, dict):
                        data = [data]
                    for item in data:
                        fans.append({
                            "name": item.get("Name", "System Fan"),
                            "reading": float(item.get("DesiredSpeed", 0)),
                            "unit": "RPM"
                        })
                except (json.JSONDecodeError, ValueError, TypeError):
                    pass
        except Exception:
            pass
            
    return fans

def _get_registry_value(key_path: str, value_name: str) -> str:
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path)
        val, _ = winreg.QueryValueEx(key, value_name)
        return str(val).strip()
    except Exception:
        return "Unknown"

def _get_gpu_from_registry() -> str:
    try:
        class_key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}"
        )
        i = 0
        gpus = []
        while True:
            try:
                subkey_name = winreg.EnumKey(class_key, i)
                if subkey_name.isdigit():
                    try:
                        subkey = winreg.OpenKey(class_key, subkey_name)
                        driver_desc, _ = winreg.QueryValueEx(subkey, "DriverDesc")
                        if driver_desc:
                            gpus.append(str(driver_desc).strip())
                    except OSError:
                        pass
                i += 1
            except OSError:
                break
        if gpus:
            # Join multiple unique GPUs if present
            unique_gpus = list(dict.fromkeys(gpus))
            return ", ".join(unique_gpus)
    except Exception:
        pass
    return "Unknown"

def _run_consolidated_powershell() -> dict:
    """Consolidated single-call fallback to gather all system metrics using PowerShell."""
    cmd = (
        "$bb = Get-CimInstance Win32_BaseBoard; "
        "$bios = Get-CimInstance Win32_BIOS; "
        "$vc = Get-CimInstance Win32_VideoController; "
        "$mem_slots = Get-CimInstance Win32_PhysicalMemoryArray; "
        "$mem_devices = Get-CimInstance Win32_PhysicalMemory; "
        "[PSCustomObject]@{ "
        "mb_manufacturer = $bb.Manufacturer; "
        "mb_product = $bb.Product; "
        "mb_version = $bb.Version; "
        "bios_vendor = $bios.Manufacturer; "
        "bios_version = $bios.SMBIOSBIOSVersion; "
        "bios_date = if ($bios.ReleaseDate) { $bios.ReleaseDate.ToString('yyyy-MM-dd') } else { 'Unknown' }; "
        "gpu_name = if ($vc) { ($vc | Select-Object -First 1).Name } else { 'Unknown' }; "
        "ram_slots_total = if ($mem_slots) { $mem_slots.MemoryDevices } else { 0 }; "
        "ram_slots_filled = if ($mem_devices) { if ($mem_devices -is [array]) { $mem_devices.Count } else { 1 } } else { 0 } "
        "} | ConvertTo-Json"
    )
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", cmd],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout.strip())
    except Exception:
        return {}

_cached_sys_info = None

def get_sys_info() -> SysData:
    """
    Fetches Motherboard, BIOS, RAM, and GPU information instantly using registry keys.
    Missing info will be populated by an async call later.
    """
    global _cached_sys_info
    if _cached_sys_info is not None:
        return _cached_sys_info

    # 1. Try registry first (extremely fast, sub-millisecond)
    mb_manufacturer = _get_registry_value(r"HARDWARE\DESCRIPTION\System\BIOS", "BaseBoardManufacturer")
    mb_product = _get_registry_value(r"HARDWARE\DESCRIPTION\System\BIOS", "BaseBoardProduct")
    mb_version = _get_registry_value(r"HARDWARE\DESCRIPTION\System\BIOS", "BaseBoardVersion")
    
    bios_vendor = _get_registry_value(r"HARDWARE\DESCRIPTION\System\BIOS", "BIOSVendor")
    bios_version = _get_registry_value(r"HARDWARE\DESCRIPTION\System\BIOS", "BIOSVersion")
    bios_date = _get_registry_value(r"HARDWARE\DESCRIPTION\System\BIOS", "BIOSReleaseDate")
    
    gpu_name = _get_gpu_from_registry()
    
    # RAM size querying is fast
    try:
        mem = psutil.virtual_memory()
        total_ram_gb = round(mem.total / (1024**3), 2)
    except Exception:
        total_ram_gb = 0.0

    # Disk usage querying
    try:
        disk = psutil.disk_usage('/')
        disk_total = round(disk.total / (1024**3), 2)
        disk_used = round(disk.used / (1024**3), 2)
        disk_free = round(disk.free / (1024**3), 2)
        disk_percent = disk.percent
    except Exception:
        disk_total = disk_used = disk_free = disk_percent = 0.0

    _cached_sys_info = {
        "mb_manufacturer": mb_manufacturer,
        "mb_product": mb_product,
        "mb_version": mb_version,
        "bios_vendor": bios_vendor,
        "bios_version": bios_version,
        "bios_date": bios_date,
        "total_ram": total_ram_gb,
        "gpu_name": gpu_name,
        "disk_total": disk_total,
        "disk_used": disk_used,
        "disk_free": disk_free,
        "disk_percent": disk_percent,
        "ram_slots_total": 0, # To be updated
        "ram_slots_filled": 0  # To be updated
    }
    return _cached_sys_info

def update_sys_info_async():
    """Fetches remaining system info using PowerShell in the background."""
    global _cached_sys_info
    ps_info = _run_consolidated_powershell()
    if ps_info and _cached_sys_info:
        if _cached_sys_info["mb_manufacturer"] == "Unknown": _cached_sys_info["mb_manufacturer"] = ps_info.get("mb_manufacturer", "Unknown")
        if _cached_sys_info["mb_product"] == "Unknown": _cached_sys_info["mb_product"] = ps_info.get("mb_product", "Unknown")
        if _cached_sys_info["mb_version"] == "Unknown": _cached_sys_info["mb_version"] = ps_info.get("mb_version", "Unknown")
        if _cached_sys_info["bios_vendor"] == "Unknown": _cached_sys_info["bios_vendor"] = ps_info.get("bios_vendor", "Unknown")
        if _cached_sys_info["bios_version"] == "Unknown": _cached_sys_info["bios_version"] = ps_info.get("bios_version", "Unknown")
        if _cached_sys_info["bios_date"] == "Unknown": _cached_sys_info["bios_date"] = ps_info.get("bios_date", "Unknown")
        if _cached_sys_info["gpu_name"] == "Unknown": _cached_sys_info["gpu_name"] = ps_info.get("gpu_name", "Unknown")
        _cached_sys_info["ram_slots_total"] = ps_info.get("ram_slots_total", 0)
        _cached_sys_info["ram_slots_filled"] = ps_info.get("ram_slots_filled", 0)
    return _cached_sys_info

if __name__ == "__main__":
    import pprint
    pprint.pprint(get_sys_info())