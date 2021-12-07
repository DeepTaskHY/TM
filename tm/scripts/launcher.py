#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from dtroslib.helpers import get_test_configuration, timestamp
from flask import Flask, render_template
from flask_socketio import SocketIO
from os import path
from roslibpy import Ros

from rosbridge import PlanningBridgeNamespace, DialogBridgeNamespace, VisionBridgeNamespace, SpeechBridgeNamespace


flask_configuration = get_test_configuration('tm', 'flask')
ros_configuration = get_test_configuration('tm', 'ros')

# Flask
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# ROS
ros = Ros(host=ros_configuration['host'],
          port=ros_configuration['port'])

while not ros.is_connected:
    ros.run()

# Rosbridge WebSocket
sio = SocketIO(app)

sio.on_namespace(PlanningBridgeNamespace(client=ros,
                                         namespace='/planning'))

sio.on_namespace(DialogBridgeNamespace(client=ros,
                                       namespace='/dialog'))

sio.on_namespace(VisionBridgeNamespace(client=ros,
                                       namespace='/vision'))

sio.on_namespace(SpeechBridgeNamespace(client=ros,
                                       namespace='/speech'))


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    sio.run(app=app,
            host=flask_configuration['host'],
            port=flask_configuration['port'])
