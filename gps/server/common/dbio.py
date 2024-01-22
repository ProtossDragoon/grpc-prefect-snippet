""" 태그를 기준으로 concurrency 제어 가능함을 보여 주기 위한 파일.
이 파일의 코드 조각처럼 `task` 에 붙이는 것을 task-level concurrency 라고 함.
`concurrency limit` 을 생성하면 곧바로 활성화됨.
web ui, cli, python api 를 이용할 것.
cli e.g. `prefect concurrency-limit create db-lock 1`
"""

import time

import prefect


@prefect.task(tags=["db-lock"], log_prints=True)
def db_write(content: str):
    print(f"Writing {content} ... ")
    time.sleep(5)
