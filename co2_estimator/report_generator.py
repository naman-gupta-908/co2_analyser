import datetime

def generate_report(model_path, instance_type, runtime_hr, static_emissions,
                    dynamic_power_kw, dynamic_runtime_hr, dynamic_emissions, region, params):
    return {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "model_path": model_path,
        "instance_type": instance_type,
        "region": region,
        "static_runtime_hr": runtime_hr,
        "static_emissions_kgCO2": static_emissions,
        "dynamic_power_kw": dynamic_power_kw,
        "dynamic_runtime_hr": dynamic_runtime_hr,
        "dynamic_emissions_kgCO2": dynamic_emissions,
        "model_parameters": params
    }
