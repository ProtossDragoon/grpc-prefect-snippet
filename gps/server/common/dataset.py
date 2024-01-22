""" 플로우 내부에서 플로우나 태스크가 호출될 수 있음을 보여주기 위한 파일.
"""

import time

import prefect


@prefect.flow
def download_dataset(url: str):
    print(f"Downloading dataset from {url} ... ")
    time.sleep(5)


@prefect.task
def preprocess():
    time.sleep(3)
