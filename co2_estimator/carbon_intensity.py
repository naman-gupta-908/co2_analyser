import yaml

def load_config():
    with open("config.yaml", 'r') as f:
        return yaml.safe_load(f)

def get_carbon_intensity(region):
    config = load_config()
    return config['carbon_intensity'].get(region, 0.5)  # default to 0.5 kgCO2/kWh if unknown
