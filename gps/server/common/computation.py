""" global concurrency 사용을 보여 주기 위한 파일
"""

import time

import prefect
from prefect.concurrency.sync import concurrency


@prefect.flow(log_prints=True)
def heavy_computation():
    with concurrency("heavy-computation", occupy=1):
        # 2024년 1월 기준 concurrency limit 을 활성화하려면 web ui 를 한번 조작해야 함.
        # Special characters, such as /, %, &, >, <, are not allowed.
        print("Computing heavy things ... ")
        time.sleep(5)
