# SageMaker CO₂ Emission Estimator

## 🚀 Purpose
This project estimates CO₂ emissions for SageMaker model training/inference using both static and dynamic analysis.

## ✅ Features

- Auto-detect SageMaker instance type & region
- Region-specific carbon intensity
- CPU + GPU usage monitoring
- Model parameter count extraction
- S3 and DynamoDB report export
- Fully containerized for SageMaker Processing Jobs

## 🚀 Deployment Steps

### 1️⃣ Build Docker Image
```bash
docker build -t sagemaker-co2-estimator:latest .

aws ecr create-repository --repository-name sagemaker-co2-estimator
aws ecr get-login-password | docker login --username AWS --password-stdin <account-id>.dkr.ecr.ap-south-1.amazonaws.com
docker tag sagemaker-co2-estimator:latest <account-id>.dkr.ecr.ap-south-1.amazonaws.com/sagemaker-co2-estimator:latest
docker push <account-id>.dkr.ecr.ap-south-1.amazonaws.com/sagemaker-co2-estimator:latest

Local

python main.py --model_path dummy-model.pth --runtime 0.5 --framework pytorch


tar file:

tar -czvf co2-emissions-ui.tar.gz .
