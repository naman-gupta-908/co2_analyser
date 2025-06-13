import time
import psutil
import pynvml
import torchvision.models as models
import torch
import subprocess


def monitor(file_name, duration_sec):
    """
    Monitor CPU and GPU power usage while running model_callable on sample_input.

    Returns:
        avg_power_kw: average power consumption in kW
        runtime_hr: total runtime in hours
    """

    # # ---------- LOAD MODEL (ResNet18 pretrained) ----------
    # print("Loading pretrained ResNet18...")
    #
    # model = models.googlenet(weights=models.GoogLeNet_Weights.IMAGENET1K_V1)
    # model.eval()
    #
    # # ---------- CREATE SAMPLE INPUT ----------
    # # ResNet expects (batch_size, channels, height, width): (1, 3, 224, 224)
    # sample_input = torch.randn(1, 3, 224, 224)
    #
    # # Create model_callable wrapper
    # def model_callable(model_input):
    #     with torch.no_grad():
    #         return model(model_input)


    # Try initializing GPU monitoring
    gpu_monitoring_enabled = False
    try:
        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        gpu_monitoring_enabled = True
    except Exception as e:
        print(f"[INFO] GPU monitoring not available: {e}")

    cpu_power_watts = []
    gpu_power_watts = []

    start_time = time.time()

    # Continuous monitoring loop
    while (time.time() - start_time) < duration_sec:
        cpu_usage = psutil.cpu_percent(interval=0.1)
        cpu_power = cpu_usage * 0.5  # Rough estimation: 0.5W per 1% usage (tweak as per your hardware)
        cpu_power_watts.append(cpu_power)

        if gpu_monitoring_enabled:
            try:
                power_draw = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000  # milliwatts to watts
                gpu_power_watts.append(power_draw)
            except Exception as e:
                print(f"[WARNING] Could not read GPU power: {e}")
                gpu_power_watts.append(0)

        # Actually run model inside loop to simulate realistic inference
        # _ = model_callable(sample_input)
        # Run the sentiment_train.py script (replace with actual filename)
        process = subprocess.Popen(["python3", "/opt/ml/processing/co2_estimator/" + file_name])

        # Wait until the subprocess is done
        process.wait()


    end_time = time.time()

    # Average power calculations
    avg_cpu_power = sum(cpu_power_watts) / len(cpu_power_watts) if cpu_power_watts else 0
    avg_gpu_power = sum(gpu_power_watts) / len(gpu_power_watts) if gpu_power_watts else 0
    total_power_watts = avg_cpu_power + avg_gpu_power

    runtime_sec = end_time - start_time
    runtime_hr = runtime_sec / 3600
    power_kw = total_power_watts / 1000

    print(f"Avg CPU Power: {avg_cpu_power:.2f} W")
    print(f"Avg GPU Power: {avg_gpu_power:.2f} W")
    print(f"Total Avg Power: {total_power_watts:.2f} W")
    print(f"Runtime: {runtime_sec:.2f} sec")

    # Clean up GPU
    if gpu_monitoring_enabled:
        pynvml.nvmlShutdown()

    return power_kw, runtime_hr
