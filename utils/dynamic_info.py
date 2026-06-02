import subprocess
import json
from typing import TypedDict

class DynamicData(TypedDict):
    gpu_usage: float
    fans: list[dict]

def get_dynamic_info() -> DynamicData:
    """
    Consolidates multiple PowerShell queries into one to reduce process spawn overhead.
    Fetches GPU usage and Fan/Thermal sensors.
    """
    # Consolidated PowerShell script
    cmd = (
        "$gpu = Get-CimInstance Win32_PerfFormattedData_GPUPerformanceCounters_GPUEngine | "
        "Where-Object { $_.Name -like '*3D' } | Measure-Object -Property UtilizationPercentage -Sum; "
        "$fans = Get-CimInstance -Namespace root/HP/InstrumentedBIOS -ClassName HP_BIOSNumericSensor | "
        "Select-Object Name, CurrentReading; "
        "if (!$fans) { $fans = Get-CimInstance Win32_Fan | Select-Object Name, DesiredSpeed }; "
        "[PSCustomObject]@{ "
        "gpu_usage = [math]::Round($gpu.Sum, 2); "
        "fans = $fans "
        "} | ConvertTo-Json"
    )
    
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", cmd],
            capture_output=True,
            text=True,
            check=False
        )
        if result.stdout.strip():
            data = json.loads(result.stdout)
            # Normalize fans
            fans_raw = data.get("fans", [])
            if isinstance(fans_raw, dict):
                fans_raw = [fans_raw]
            
            normalized_fans = []
            for f in fans_raw:
                name = f.get("Name", "Sensor")
                reading = f.get("CurrentReading") or f.get("DesiredSpeed") or 0
                unit = "RPM" if "Fan" in name else "°C"
                normalized_fans.append({"name": name, "reading": float(reading), "unit": unit})
            
            return {
                "gpu_usage": float(data.get("gpu_usage", 0.0)),
                "fans": normalized_fans
            }
    except Exception:
        pass
        
    return {"gpu_usage": 0.0, "fans": []}
