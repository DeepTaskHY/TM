#!/bin/bash
set -e

# Setup catkin workspace
source "/opt/ros/$ROS_DISTRO/setup.sh" && catkin_make
source devel/setup.sh

# Setup ROS environment
echo "source \"/opt/ros/$ROS_DISTRO/setup.sh\"" >> /etc/bash.bashrc
echo "source /workspace/devel/setup.sh" >> /etc/bash.bashrc

# Setup executable files
chmod +x src/tm/src/scripts/launcher.py \
         src/dm_generator/src/scripts/launcher.py \
         src/vision/src/scripts/launch_vision.py \
         src/speech/src/scripts/launch_stt.py \
         src/speech/src/scripts/launch_tts.py

# Execute CMD
exec "$@"
