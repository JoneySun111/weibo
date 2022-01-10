docker run -it --rm --network host \
    --init \
    --runtime nvidia \
    -v /opt/tiger/yarn_deploy:/opt/tiger/yarn_deploy \
    -v /opt/tiger/consul_deploy:/opt/tiger/consul_deploy \
    -v /opt/tiger/jdk:/opt/tiger/jdk \
    -v /opt/tiger/ss_bin:/opt/tiger/ss_bin \
    -v /opt/tiger/ss_conf:/opt/tiger/ss_conf \
    -v /opt/tiger/pyutil:/opt/tiger/pyutil \
    -v /opt/tiger/ss_data:/opt/tiger/ss_data \
    -v /opt/tiger/ss_lib:/opt/tiger/ss_lib \
    -v /data00/home/sunzhouyi/JoneySun/demo/:/sunzhouyi \
    --shm-size=1024m \
    szy_demo bash
    # torch1.8.1_cu111 bash

# export CUDA_VISIBLE_DEVICES=2