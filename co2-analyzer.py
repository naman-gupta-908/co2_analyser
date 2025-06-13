import os
import boto3
import sys
import os
import json
from decimal import Decimal
from co2_estimator import (
    sagemaker_metadata, carbon_intensity, static_estimator,
    dynamic_monitor, model_parser, dynamo_uploader, report_generator
)

"""
Docker Image Push Commands
1. docker buildx create --use
2. docker buildx inspect --bootstrap
3. docker buildx build --platform linux/amd64 \
                               -t 476287788373.dkr.ecr.us-east-1.amazonaws.com/co2-analyzer:latest \
                                                                                                . \
                                                                                            --push

"""
# Initialize DynamoDB client
region = 'us-east-1'  # Specify your AWS region
dynamo_endpoint_url = f'https://dynamodb.{region}.amazonaws.com'
dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url=dynamo_endpoint_url)
dynamo_db_co2_metric_table_name = "AIModelCo2Metrics"

def analyze_co2():
    # Define the local path where input data is available
    input_path = '/opt/ml/processing/input'

    # List files in the input directory
    input_files = os.listdir(input_path)
    print("Input files:", input_files)
    first_file = ""
    report = {}
    if input_files:
        first_file = input_files[0]
        print("First file:", first_file)
        report = main(first_file)

    print(f"Processing Job Name: {sys.argv[1]}")
    required_keys = [
        "dynamic_power_kw",
        "file_name",
        "static_emissions_kgCO2",
        "dynamic_emissions_kgCO2"
    ]

    # Build filtered dict
    filtered_dict = {key: report[key] for key in required_keys if key in report}

    filtered_dict["JobName"] = sys.argv[1]

    filtered_dict = prepare_dynamodb_item(filtered_dict)
    print("filtered_dict", filtered_dict)
    uploadCo2MetricToDynamoDb([filtered_dict])

def prepare_dynamodb_item(data_dict):
    item = {}
    for k, v in data_dict.items():
        if isinstance(v, float):
            item[k] = Decimal(str(v))
        else:
            item[k] = v
    return item

def uploadCo2MetricToDynamoDb(data_list):
    table = dynamodb.Table(dynamo_db_co2_metric_table_name)
    for item in data_list:
        table.put_item(Item=item)
    print("Co2 Metric Uploaded to Dynamodb successfully!!")

def main(file_name):
    model_path = os.environ.get("MODEL_PATH", file_name)
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

    dynamic_power_kw, dynamic_runtime_hr = dynamic_monitor.monitor(file_name=file_name, duration_sec=30)
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

    # Print key-value pairs line by line
    for key, value in report.items():
        print(f"{key}: {value}")
    json_file = f"co2_report.json"
    with open(json_file, "w") as f:
        json.dump(report, f, indent=4)

    # dynamo_uploader.upload_to_dynamodb(report, dynamo_table)
    # print("✅ Report uploaded to S3 and DynamoDB")
    return report

if __name__ == '__main__':
    analyze_co2()

