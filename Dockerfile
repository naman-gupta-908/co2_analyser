FROM python:3.8-slim

COPY requirements.txt /opt/ml/processing/requirements.txt

RUN pip install -r /opt/ml/processing/requirements.txt

# COPY co2_estimator/sentiment_train.py /opt/ml/processing/input/sentiment_train.py
COPY config.yaml /opt/ml/processing/config.yaml
COPY co2-analyzer.py /opt/ml/processing/co2-analyzer.py
COPY co2_estimator /opt/ml/processing/co2_estimator

ENTRYPOINT ["python3", "/opt/ml/processing/co2-analyzer.py"]
