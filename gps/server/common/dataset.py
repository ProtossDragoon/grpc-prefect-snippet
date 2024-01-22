import time

import prefect


@prefect.flow
def download_dataset(url: str):
    print(f"Downloading dataset from {url} ... ")
    time.sleep(20)


@prefect.task
def preprocess():
    time.sleep(3)
