def estimate_static_emission(instance_type, runtime_hours, power_map, carbon_intensity):
    power_kw = power_map.get(instance_type, 0.1)
    emissions = power_kw * runtime_hours * carbon_intensity
    return emissions
