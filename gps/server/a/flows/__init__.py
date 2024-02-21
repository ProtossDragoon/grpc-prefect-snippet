# 내장
import datetime

# 서드파티
import prefect

# 프로젝트
from gps.proto.gps import Request
from gps.server.common.computation import heavy_computation
from gps.server.common.dataset import download_dataset, download_model, preprocess


@prefect.flow(log_prints=True, persist_result=True)
def server_a_flow(request: Request) -> dict:
    """ 서버에서 실질적으로 실행해야 하는 로직
    """
    urls = request.data_info.object_storage_urls
    for url in urls:
        download_dataset(url)
    urls = request.model_info.model_registry_urls
    for url in urls:
        download_model(url)
    preprocess()
    preprocess()
    heavy_computation()

    return {"latency": 5.0, "timestamp": datetime.datetime.now()}
