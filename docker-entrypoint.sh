#!/bin/bash
set -e

# Setup catkin workspace
source "/opt/ros/$ROS_DISTRO/setup.sh" && catkin_make
source devel/setup.sh

# Setup ROS environment
echo "source \"/opt/ros/$ROS_DISTRO/setup.sh\"" >> /etc/bash.bashrc
echo "source /workspace/devel/setup.sh" >> /etc/bash.bashrc

# Setup executable files
chmod +x src/tm/src/scripts/tm_launcher.py \
         src/tm/src/scripts/pm_launcher.py \
         src/dm_generator/src/scripts/launcher.py \
         src/km/src/scripts/launcher.py \
         src/vision/src/scripts/launcher.py \
         src/speech/src/scripts/stt_launcher.py \
         src/speech/src/scripts/tts_launcher.py

# Execute CMD
exec "$@"
