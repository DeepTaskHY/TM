#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os import path
from flask_socketio import SocketIO
from flask import Flask, render_template
from rosbridge import PlanningBridgeNamespace, DialogBridgeNamespace, VisionBridgeNamespace, SpeechBridgeNamespace
from dtroslib.helpers import get_test_configuration, timestamp


flask_configuration = get_test_configuration('tm', 'flask')
ros_configuration = get_test_configuration('tm', 'ros')

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

sio = SocketIO(app)

sio.on_namespace(PlanningBridgeNamespace(host=ros_configuration['host'],
                                         port=ros_configuration['port'],
                                         namespace='/planning'))

sio.on_namespace(DialogBridgeNamespace(host=ros_configuration['host'],
                                       port=ros_configuration['port'],
                                       namespace='/dialog'))

sio.on_namespace(VisionBridgeNamespace(host=ros_configuration['host'],
                                       port=ros_configuration['port'],
                                       namespace='/vision'))

sio.on_namespace(SpeechBridgeNamespace(host=ros_configuration['host'],
                                       port=ros_configuration['port'],
                                       namespace='/speech'))


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    sio.run(app=app,
            host=flask_configuration['host'],
            port=flask_configuration['port'])