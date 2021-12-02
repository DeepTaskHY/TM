FROM ros:noetic

# Remove user interactive
ENV DEBIAN_FRONTEND noninteractive

# Update repo packages
RUN apt-get update --fix-missing && \
    apt-get install -y apt-utils && \
    apt-get upgrade -y

# Install python
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN apt-get install -y python3-pip
RUN pip install --upgrade pip && \
    pip install --upgrade setuptools

# Install OS packages (for modules/Vision)
RUN apt-get -y install libgirepository1.0-dev \
                       libcairo2-dev

# Install OS packages (for modules/Speech)
RUN apt-get -y install libgstreamer1.0-dev \
                       libgstreamer-plugins-base1.0-dev \
                       libgstreamer-plugins-bad1.0-dev \
                       gstreamer1.0-plugins-base \
                       gstreamer1.0-plugins-good \
                       gstreamer1.0-plugins-bad \
                       gstreamer1.0-plugins-ugly \
                       gstreamer1.0-libav \
                       gstreamer1.0-doc \
                       gstreamer1.0-tools \
                       gstreamer1.0-x \
                       gstreamer1.0-alsa \
                       gstreamer1.0-gl \
                       gstreamer1.0-gtk3 \
                       gstreamer1.0-qt5 \
                       gstreamer1.0-pulseaudio

RUN apt-get -y install libsndfile1 \
                       libportaudio2

# Install require dependencies
WORKDIR /workspace
ADD requirements.txt requirements-tm.txt
# ADD modules/PM/requirements.txt requirements-pm.txt
ADD modules/DM_Generator/requirements.txt requirements-dm.txt
ADD modules/DM_Intent/requirements.txt requirements-dm_intent.txt
ADD modules/KM/requirements.txt requirements-km.txt
ADD modules/Vision/requirements.txt requirements-vision.txt
ADD modules/Speech/requirements.txt requirements-speech.txt
RUN ls requirements-*.txt | xargs paste -sd'\n' > requirements.txt
RUN pip install -r requirements.txt

# Install ROS packages (for ROS WebSocket)
RUN apt-get install -y ros-noetic-rosbridge-suite

# Install ROS packages (for modules/Vision)
RUN apt-get install -y ros-$(rosversion -d)-cv-bridge

# Setup ROS environment
RUN rosdep update
ADD docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh
ENTRYPOINT ["/workspace/docker-entrypoint.sh"]
CMD ["roslaunch", "tm", "tm_launcher.launch"]
