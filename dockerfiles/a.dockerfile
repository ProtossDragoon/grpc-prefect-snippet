# syntax=docker/dockerfile:1

ARG BASE_IMAGE

FROM ${BASE_IMAGE}

LABEL author="janghoo.lee"

# --- 애플리케이션 ---

COPY server-a-requirements.txt server-a-requirements.txt

RUN python3 -m pip install -r server-a-requirements.txt

COPY gps gps

CMD ["python3", "-m", "gps.server.a.main_serve"]
