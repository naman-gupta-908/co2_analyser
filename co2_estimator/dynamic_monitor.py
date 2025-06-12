import psutil
import numpy as np
import time

try:
    import pynvml
    pynvml.nvmlInit()
    GPU_ENABLED = True
except:
    GPU_ENABLED = False

def monitor(duration_sec=10, model_callable=None, sample_input=None):
    cpu_power_list, gpu_power_list = [], []
    CPU_WATT_PER_CORE = 10
    GPU_WATT_ESTIMATE = 150

    start_time = time.time()

    while time.time() - start_time < duration_sec:
        cpu_percent = psutil.cpu_percent(interval=0.5)
        cpu_power = (cpu_percent / 100) * psutil.cpu_count() * CPU_WATT_PER_CORE
        cpu_power_list.append(cpu_power)

        gpu_power = 0
        if GPU_ENABLED:
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            gpu_power = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000
        else:
            gpu_power = GPU_WATT_ESTIMATE

        gpu_power_list.append(gpu_power)

        if model_callable and sample_input:
            _ = model_callable(sample_input)

    avg_cpu = np.mean(cpu_power_list)
    avg_gpu = np.mean(gpu_power_list)
    total_power_kw = (avg_cpu + avg_gpu) / 1000
    runtime_hr = duration_sec / 3600

    return total_power_kw, runtime_hr
