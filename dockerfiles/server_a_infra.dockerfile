# syntax=docker/dockerfile:1

ARG BASE_IMAGE

FROM ${BASE_IMAGE}

LABEL author="janghoo.lee"

# --- 도커파일 빌드 중 I/O 블로킹을 막기 위한 기본 세팅 ---

ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone

# --- 기본 패키지 설치 ---

# --- 애플리케이션 ---

COPY requirements-a.txt requirements.txt

RUN python3 -m pip install -r requirements.txt

COPY gps gps

CMD ["python3", "-m", "gps.server.a.flows.main_serve"]
