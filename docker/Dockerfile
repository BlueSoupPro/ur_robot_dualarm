ARG ROS_DISTRO=jazzy
FROM ros:${ROS_DISTRO}

SHELL ["/bin/bash", "-lc"]

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
ENV WS=/ws

RUN apt update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    iputils-ping \
    libcurl4-openssl-dev \
    locales \
    lsb-release \
    nano \
    python3-colcon-common-extensions \
    python3-pip \
    python3-rosdep \
    python3-tk \
    python3-vcstool \
    terminator \
    wget \
    ros-${ROS_DISTRO}-controller-manager \
    ros-${ROS_DISTRO}-joint-state-publisher \
    ros-${ROS_DISTRO}-joint-state-publisher-gui \
    ros-${ROS_DISTRO}-joint-trajectory-controller \
    ros-${ROS_DISTRO}-moveit \
    ros-${ROS_DISTRO}-position-controllers \
    ros-${ROS_DISTRO}-rmw-cyclonedds-cpp \
    ros-${ROS_DISTRO}-robot-state-publisher \
    ros-${ROS_DISTRO}-ros-gz \
    ros-${ROS_DISTRO}-ros2-control \
    ros-${ROS_DISTRO}-ros2-controllers \
    ros-${ROS_DISTRO}-ros2controlcli \
    ros-${ROS_DISTRO}-rviz2 \
    ros-${ROS_DISTRO}-tf2-tools \
    ros-${ROS_DISTRO}-ur \
    ros-${ROS_DISTRO}-xacro && \
    locale-gen en_US en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

COPY ../ws/ ${WS}/

RUN sed -i 's/#force_color_prompt=yes/force_color_prompt=yes/' /root/.bashrc && \

WORKDIR ${WS}

CMD ["bash", "-c", "terminator & bash"]
