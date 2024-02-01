# 내장
import datetime
from typing import List

# 서드파티
import prefect

# 프로젝트
from gps.server.common.dbio import db_write
from gps.server.common.computation import heavy_computation
from gps.server.common.dataset import download_dataset, preprocess


@prefect.flow
def server_a_flow(urls: List[str]) -> dict:
    """ 서버에서 실질적으로 실행해야 하는 로직
    """
    for url in urls:
        download_dataset(url)
    db_write("content a")
    heavy_computation()
    db_write("global content")
    preprocess()
    preprocess()

    return {"latency": 5.0, "timestamp": datetime.datetime.now()}
