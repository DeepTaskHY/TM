#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os import path
from flask_socketio import SocketIO
from flask import Flask, render_template
from rosbridge import RosBridgeNamespace
from dtroslib.helpers import get_test_configuration, timestamp


flask_configuration = get_test_configuration('tm', 'flask')
ros_configuration = get_test_configuration('tm', 'ros')

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

sio = SocketIO(app)

namespace = RosBridgeNamespace(host=ros_configuration['host'],
                               port=ros_configuration['port'],
                               namespace='/rosbridge')

sio.on_namespace(namespace)


@app.route('/scenarios/', defaults={'scenario_name': 'homecare'})
@app.route('/scenarios/<scenario_name>')
def index(scenario_name: str):
    # scenario = ScenarioParser(scenario_name).get_scenario()
    # intent_names = scenario.get_intent_names()

    args = {
        'scenario_name': scenario_name,
        # 'intent_names': intent_names,
        'intent_names': [],
        'timestamp': timestamp()
    }

    return render_template('index.html', **args)


if __name__ == '__main__':
    sio.run(app=app,
            host=flask_configuration['host'],
            port=flask_configuration['port'],
            debug=True)
