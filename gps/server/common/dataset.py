# 내장
import time

# 서드파티
import prefect


@prefect.flow
def download_model(url: str):
    print(f"Downloading model from {url} ... ")
    time.sleep(1.5)


@prefect.flow
def download_dataset(url: str):
    print(f"Downloading dataset from {url} ... ")
    time.sleep(3)


@prefect.task
def preprocess():
    time.sleep(2)
