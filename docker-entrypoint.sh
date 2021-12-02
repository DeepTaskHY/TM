#!/bin/bash
set -e

# Setup catkin workspace
source "/opt/ros/$ROS_DISTRO/setup.sh" && catkin_make
source devel/setup.sh

# Setup ROS environment
echo "source \"/opt/ros/$ROS_DISTRO/setup.sh\"" >> /etc/bash.bashrc
echo "source /workspace/devel/setup.sh" >> /etc/bash.bashrc

# Setup executable files
chmod +x src/tm/scripts/launcher.py \
         src/dummy_tm/scripts/launcher.py \
         src/dm_generator/scripts/launcher.py \
         src/dm_intent/scripts/launcher.py \
         src/km/scripts/launcher.py \
         src/vision/scripts/launcher.py \
         src/speech/scripts/stt_launcher.py \
         src/speech/scripts/tts_launcher.py

# Execute CMD
exec "$@"
