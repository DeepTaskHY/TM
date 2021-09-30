#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import rospy
import threading
import time
from dtroslib.ros import NodeBase
from std_msgs.msg import String
from dtroslib.helpers import get_package_path

test_path = get_package_path('tm')
# test_path = '..'

_human_speech: str
_intent: str

_sc: dict
_sc_ready: bool = False
_dialog_exec_done = True


def callback_vision(message):
    received_message = json.loads(message.data)
    # rospy.loginfo('Received message: \n{}'.format(json.dumps(message, ensure_ascii=False, indent="\t")))

    header = received_message['header']

    f_id = received_message['face_recognition']['face_id']
    t_point = received_message['face_recognition']['timestamp']
    
    json_file = test_path+'/json-example/2-p-k.json'
    msg = json.load(open(json_file, 'r'))
    msg['knowledge_query']['data'][0]['face_id'] = f_id
    msg['knowledge_query']['data'][0]['timestamp'] = t_point

    pm_node.publish('/taskExecution', json.dumps(msg, ensure_ascii=False, indent='\t'))
    rospy.loginfo('Published message: \n{}'.format(json.dumps(msg, ensure_ascii=False, indent="\t")))

    return


def callback_speech(message):
    global _intent

    received_message = json.loads(message.data)
    # print(received_message)
    # rospy.loginfo('Received message: \n{}'.format(json.dumps(message, ensure_ascii=False, indent="\t")))

    header = received_message['header']
    _human_speech = received_message['human_speech']['stt']

    if '머리' in _human_speech or '아프' in _human_speech:
        _dialog_exec_done = False
        _intent = 'medical_reception'
        

    if '약' in _human_speech and '먹' in _human_speech:
        json_file = test_path+'/json-example/7-p-k.json'
        msg = json.load(open(json_file, 'r'))

        pm_node.publish('/taskExecution', json.dumps(msg, ensure_ascii=False, indent='\t'))
        rospy.loginfo('Published message: \n{}'.format(json.dumps(msg, ensure_ascii=False, indent="\t")))

    if '아까' in _human_speech and '약' in _human_speech and '아직도' in _human_speech:
        _dialog_exec_done = False
        _intent = 'medical_reception'

    return

def callback_task(message):
    global _human_speech, _sc
    
    received_message = json.loads(message.data)
    header = received_message['header']
    source = header['source']

    if 'planning' not in header['target']:
        return

    rospy.loginfo('Received message: \n{}'.format(json.dumps(message, ensure_ascii=False, indent="\t")))

    if source == 'knowledge':
        if 'knowledge_query' in header['content']:
            if received_message['knowledge_query']['type'] == 'face_recognition':
                _sc = received_message['knowledge_query']['data']['social_context']
                _sc_ready = True   

    if source == 'dialog':
        dm_id = header['id']

        content_key = received_message['header']['content'][0]
        _robot_speech = received_message[content_key]['dialog']

        tar = ['tts']
        con_name = ['robot_speech']
        con = {'text': _robot_speech}
        msg = pm_msg_generator(id, tar, con_name, con)

        pm_node.publish('/action/speech', json.dumps(msg, ensure_ascii=False, indent='\t'))
        rospy.loginfo('Published message: \n{}'.format(json.dumps(msg, ensure_ascii=False, indent="\t")))

        return

    return

def dialog_exec():
    global _intent, _human_speech, _sc_ready, _dialog_exec_done
    
    while True:
        if not _dialog_exec_done:

            if _sc_ready and _intent == 'medical_reception':
                json_file = test_path+'/json-example/4-p-d.json'
                msg = json.load(open(json_file, 'r'))
                msg['dialog_generation']['intent'] = _intent
                msg['dialog_generation']['human_speech'] = _human_speech
                msg['dialog_generation']['social_context'] = _sc

                pm_node.publish('/taskExecution', json.dumps(msg, ensure_ascii=False, indent='\t'))
                rospy.loginfo('Published message: \n{}'.format(json.dumps(msg, ensure_ascii=False, indent="\t")))
                
                _dialog_exec_done = True

        else:
            time.sleep(0.1)

    return


def pm_msg_generator(id, targets, content_names, contents):
    json_msg = {
        'header': {
            'timestamp': str(time.time()),
            'source': 'plannig',
            'target': targets,
            'content': content_names,
            'id': id,
        }
    }
    json_msg.update(contents)

    return json_msg


if __name__ == '__main__':
    pm_node = NodeBase('pm_node')

    pm_node.add_publisher("/taskExecution", String, queue_size=10)
    pm_node.add_publisher("/action/speech", String, queue_size=10)
    pm_node.add_subscriber("/recognition/speech", String, callback_speech)
    pm_node.add_subscriber("/recognition/face_id", String, callback_vision)
    pm_node.add_subscriber("/taskCompletion", String, callback_task)

    t = threading.Thread(target=dialog_exec)
    t.start()
    rospy.loginfo('Start PM')
    pm_node.spin()
