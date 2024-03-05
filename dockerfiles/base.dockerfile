# syntax=docker/dockerfile:1

ARG BASE_IMAGE

FROM ${BASE_IMAGE}

LABEL author="janghoo.lee"

# --- 도커파일 빌드 중 I/O 블로킹을 막기 위한 기본 세팅 ---

ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone

# --- 기본 패키지 설치 ---

RUN apt-get update -y && apt-get upgrade -y

RUN apt-get install -y git

ARG PY3_VERSION

RUN apt-get install -y software-properties-common &&\
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update -y && apt-get upgrade && \
    apt-get install -y python${PY3_VERSION}-full && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python${PY3_VERSION} 2 && \
    update-alternatives --set python /usr/bin/python${PY3_VERSION} && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1 && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python${PY3_VERSION} 2 && \
    update-alternatives --set python3 /usr/bin/python${PY3_VERSION}
    # ln -sf /usr/bin/python${PY3_VERSION} /usr/bin/python && \
    # ln -sf /usr/bin/python${PY3_VERSION} /usr/bin/python3
# NOTE: https://www.data-mining.co.nz/docker-for-data-scientists/tips_and_tricks/#python
# NOTE: https://blog.yue-su.dev/setup-vgpu-in-docker-container.html

RUN apt-get update -y && apt-get upgrade && \
    apt-get install -y python${PY3_VERSION}-distutils &&\
    apt-get install -y python3-pip && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3 && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python${PY3_VERSION} && \
    # ln -sf /usr/bin/pip3 /usr/bin/pip
    python3 -m pip install --upgrade pip
# NOTE: https://stackoverflow.com/questions/69503329/pip-is-not-working-for-python-3-10-on-ubuntu/69527217#69527217
# NOTE: https://bobbyhadz.com/blog/python-importerror-cannot-import-name-html5lib-from-pip-vendor

# --- python-betterproto 와 prefect 의존성 관리를 하는 섹션 ---

RUN python3 -m pip install --pre 'betterproto[compiler]'

RUN python3 -m pip install 'httpx[http2]' 'pydantic<2' 'typing-extensions==4.7.1' 'prefect>=2.14'
