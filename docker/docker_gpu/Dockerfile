FROM ros:humble

RUN apt update && apt install -y --no-install-recommends \
    nano \
    python3-pip \
    python3-tk \
    terminator \
    iputils-ping \
    wget \
    curl \
    git \
    lsb-release \
    ros-humble-rmw-cyclonedds-cpp \
    # MoveIt and dependencies
    ros-humble-moveit \
    ros-humble-moveit-ros-planning \
    ros-humble-moveit-ros-planning-interface \
    ros-humble-moveit-kinematics \
    ros-humble-moveit-planners \
    ros-humble-moveit-simple-controller-manager \
    ros-humble-moveit-plugins \
    ros-humble-moveit-ros-visualization \
    ros-humble-behaviortree-cpp-v3 \
    ros-humble-diagnostic-updater \
    ros-humble-ros2controlcli \
    # UR Robot support
    ros-humble-ur \
    ros-humble-ur-description \
    ros-humble-ur-moveit-config \
    # CURL library
    libcurl4-openssl-dev \
    locales && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
ENV WS=/ws 
COPY ../ws/ $WS/

RUN sed -i 's/#force_color_prompt=yes/force_color_prompt=yes/' /root/.bashrc

CMD ["bash", "-c", "terminator & bash"]