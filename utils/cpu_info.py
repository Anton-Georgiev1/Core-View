import cpuinfo
import psutil
from typing import TypedDict

class CPUData(TypedDict):
    brand_raw: str
    arch: str
    bits: int
    count: int
    logical_count: int
    frequency_current: float
    frequency_min: float
    frequency_max: float
    usage_percent: float

def get_cpu_info() -> CPUData:
    """
    Fetches detailed CPU information using py-cpuinfo and psutil.
    """
    info = cpuinfo.get_cpu_info()
    freq = psutil.cpu_freq()
    
    return {
        "brand_raw": info.get("brand_raw", "Unknown"),
        "arch": info.get("arch", "Unknown"),
        "bits": info.get("bits", 0),
        "count": psutil.cpu_count(logical=False) or 0,
        "logical_count": psutil.cpu_count(logical=True) or 0,
        "frequency_current": freq.current if freq else 0.0,
        "frequency_min": freq.min if freq else 0.0,
        "frequency_max": freq.max if freq else 0.0,
        "usage_percent": psutil.cpu_percent(interval=None)
    }

if __name__ == "__main__":
    import pprint
    pprint.pprint(get_cpu_info())
