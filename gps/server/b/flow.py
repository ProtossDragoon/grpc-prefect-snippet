# 서드파티
import prefect

# 프로젝트
from gps.proto.gps import DataInfo, Response

# 프로젝트
from gps.server.common.dbio import db_write
from gps.server.common.computation import heavy_computation
from gps.server.common.dataset import download_dataset, preprocess


@prefect.flow(log_prints=True, persist_result=True)
def server_b_flow(data_info: DataInfo) -> Response:
    """ 서버에서 실질적으로 실행해야 하는 로직
    """
    urls = data_info.object_storage_urls
    for url in urls:
        download_dataset(url)
    db_write("content b")
    heavy_computation()
    db_write("global content")
    futures = []
    futures.append(preprocess.submit())
    futures.append(preprocess.submit())
    futures.append(preprocess.submit())
    futures.append(preprocess.submit())
    futures.append(preprocess.submit())
    for future in futures:
        future.result()

    return Response(
        latency=5.0,
        accuracy=1,
        flops=False,
        n_params=2000000,
    )
