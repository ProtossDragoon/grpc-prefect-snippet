import time

import prefect


@prefect.flow
def download_dataset(url: str):
    print(f"Downloading dataset from {url} ... ")
    time.sleep(3)


@prefect.task
def preprocess():
    time.sleep(3)
