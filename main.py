import os
import json
from co2_estimator import (
    sagemaker_metadata, carbon_intensity, static_estimator,
    dynamic_monitor, model_parser, s3_uploader, dynamo_uploader, report_generator
)

def main():
    model_path = os.environ.get("MODEL_PATH", "dummy-model.pth")
    runtime = float(os.environ.get("RUNTIME", "1.0"))
    framework = os.environ.get("FRAMEWORK", "generic")

    instance_type, region = sagemaker_metadata.get_instance_metadata()
    config = carbon_intensity.load_config()
    carbon_factor = carbon_intensity.get_carbon_intensity(region)
    s3_bucket = config['s3_bucket']
    dynamo_table = config['dynamodb_table']

    power_map = {
        'ml.m5.large': 0.1, 'ml.p3.2xlarge': 0.4,
        'ml.p3.8xlarge': 1.6, 'ml.p4d.24xlarge': 3.0,
        'ml.c5.large': 0.08, 'ml.t2.medium': 0.05
    }

    static_emissions = static_estimator.estimate_static_emission(instance_type, runtime, power_map, carbon_factor)
    params = model_parser.get_model_params(model_path, framework)

    dynamic_power_kw, dynamic_runtime_hr = dynamic_monitor.monitor(duration_sec=10)
    dynamic_emissions = dynamic_power_kw * dynamic_runtime_hr * carbon_factor

    report = report_generator.generate_report(
        model_path=model_path,
        instance_type=instance_type,
        runtime_hr=runtime,
        static_emissions=static_emissions,
        dynamic_power_kw=dynamic_power_kw,
        dynamic_runtime_hr=dynamic_runtime_hr,
        dynamic_emissions=dynamic_emissions,
        region=region,
        params=params
    )

    json_file = f"co2_report_{region}.json"
    with open(json_file, "w") as f:
        json.dump(report, f, indent=4)

    s3_uploader.upload_to_s3(json_file, s3_bucket, json_file)
    dynamo_uploader.upload_to_dynamodb(report, dynamo_table)
    print("✅ Report uploaded to S3 and DynamoDB")

if __name__ == "__main__":
    main()
