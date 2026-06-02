import pytest
from unittest.mock import MagicMock, patch
import json
from utils.sys_info import get_sys_info, get_fan_info, update_sys_info_async
from utils.cpu_info import get_cpu_info
from utils.dynamic_info import get_dynamic_info

# Helper to reset caches
@pytest.fixture(autouse=True)
def reset_caches():
    import utils.sys_info
    import utils.cpu_info
    utils.sys_info._cached_sys_info = None
    utils.cpu_info._cached_cpu_static_info = None

@pytest.fixture
def mock_ps():
    with patch("subprocess.run") as mock_run:
        yield mock_run

def test_sys_info_instant_load(mock_ps):
    # Registry should provide initial data without PowerShell
    with patch("utils.sys_info._get_registry_value", return_value="MockValue"), \
         patch("utils.sys_info._get_gpu_from_registry", return_value="MockGPU"):
        
        info = get_sys_info()
        assert info["mb_manufacturer"] == "MockValue"
        assert info["gpu_name"] == "MockGPU"
        # Initial slots should be 0 (updated later async)
        assert info["ram_slots_total"] == 0

def test_sys_info_async_update(mock_ps):
    # Simulate PowerShell returning RAM slot info
    mock_ps.return_value = MagicMock(
        stdout=json.dumps({
            "mb_manufacturer": "HP",
            "ram_slots_total": 4,
            "ram_slots_filled": 2
        })
    )
    
    # Pre-populate cache with registry data
    get_sys_info()
    
    # Trigger async update
    updated_info = update_sys_info_async()
    assert updated_info["ram_slots_total"] == 4
    assert updated_info["ram_slots_filled"] == 2

def test_cpu_info_static_cache():
    with patch("cpuinfo.get_cpu_info", return_value={"brand_raw": "Test CPU", "arch": "X86", "bits": 64}), \
         patch("psutil.cpu_count", return_value=8):
        
        # First call
        info1 = get_cpu_info()
        assert info1["brand_raw"] == "Test CPU"
        
        # Second call should use cache (mock won't be called again if we check carefully, 
        # but here we just verify consistency)
        info2 = get_cpu_info()
        assert info2["brand_raw"] == "Test CPU"

def test_dynamic_info_consolidation(mock_ps):
    # Simulate the consolidated PowerShell output
    mock_ps.return_value = MagicMock(
        stdout=json.dumps({
            "gpu_usage": 15.5,
            "fans": [
                {"Name": "CPU Fan", "CurrentReading": 2500},
                {"Name": "GPU Fan", "CurrentReading": 1800}
            ]
        })
    )
    
    dynamic = get_dynamic_info()
    assert dynamic["gpu_usage"] == 15.5
    assert len(dynamic["fans"]) == 2
    assert dynamic["fans"][0]["name"] == "CPU Fan"
    assert dynamic["fans"][0]["unit"] == "RPM"

def test_dynamic_info_error_handling(mock_ps):
    # PowerShell fails
    mock_ps.side_effect = Exception("PowerShell crashed")
    
    dynamic = get_dynamic_info()
    assert dynamic["gpu_usage"] == 0.0
    assert dynamic["fans"] == []

def test_get_fan_info_fallback(mock_ps):
    # HP specific fails, but generic succeeds
    mock_ps.side_effect = [
        MagicMock(stdout=""), # HP call empty
        MagicMock(stdout=json.dumps({"Name": "Generic Fan", "DesiredSpeed": 1200})) # Generic call
    ]
    
    fans = get_fan_info()
    assert len(fans) == 1
    assert fans[0]["name"] == "Generic Fan"
