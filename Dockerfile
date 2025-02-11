FROM continuumio/miniconda3

# static, code-independent components such as env setup & conda
RUN apt-get update && \
    apt-get -y install g++ && \
    apt-get -y install cmake

RUN conda install -y python=3.6

WORKDIR /scout
COPY . .

# Enabling these caches requires Docker 18.06+ and env variable DOCKER_BUILDKIT=1
# Without these settings the commands below will work, but they won't use cache
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip pip install -e .

ENTRYPOINT [ "scout" ]