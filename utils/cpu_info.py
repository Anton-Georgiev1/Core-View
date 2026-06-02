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
    gpu_usage: float

_cached_cpu_static_info = None

def get_cpu_info() -> CPUData:
    """
    Fetches detailed CPU information using py-cpuinfo and psutil.
    """
    global _cached_cpu_static_info
    if _cached_cpu_static_info is None:
        info = cpuinfo.get_cpu_info()
        _cached_cpu_static_info = {
            "brand_raw": info.get("brand_raw", "Unknown"),
            "arch": info.get("arch", "Unknown"),
            "bits": info.get("bits", 0),
            "count": psutil.cpu_count(logical=False) or 0,
            "logical_count": psutil.cpu_count(logical=True) or 0,
        }
    
    freq = psutil.cpu_freq()
    
    return {
        "brand_raw": _cached_cpu_static_info["brand_raw"],
        "arch": _cached_cpu_static_info["arch"],
        "bits": _cached_cpu_static_info["bits"],
        "count": _cached_cpu_static_info["count"],
        "logical_count": _cached_cpu_static_info["logical_count"],
        "frequency_current": freq.current if freq else 0.0,
        "frequency_min": freq.min if freq else 0.0,
        "frequency_max": freq.max if freq else 0.0,
        "usage_percent": psutil.cpu_percent(interval=None),
        "gpu_usage": 0.0 # Will be updated separately
    }

if __name__ == "__main__":
    import pprint
    pprint.pprint(get_cpu_info())
