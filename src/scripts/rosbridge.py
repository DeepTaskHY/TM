import json
from abc import *
from flask_socketio import Namespace
from roslibpy import Ros, Topic, Message
from typing import Any
from dtroslib.helpers import timestamp
import rospy


class RosBridgeNamespace(Namespace, metaclass=ABCMeta):
    __ros: Ros = None
    __ros_host: str = None
    __ros_port: int = None

    def __init__(self, host: str, port: int, *args, **kwargs):
        super(RosBridgeNamespace, self).__init__(*args, **kwargs)
        self.__ros_host = host
        self.__ros_port = port

    @property
    def ros(self) -> Ros:
        if not self.__ros:
            self.__ros = Ros(host=self.__ros_host, port=self.__ros_port)
            self.__ros.run()

        return self.__ros


class DeepTaskBridgeNamespace(RosBridgeNamespace, metaclass=ABCMeta):
    @classmethod
    def get_header_key(cls, data: dict, key: str) -> Any:
        try:
            return data['data']['header'][key]

        except KeyError:
            return None

    @classmethod
    def header_equal(cls, data: dict, key: str, val: Any) -> bool:
        header_val = cls.get_header_key(data, key)

        if isinstance(header_val, list):
            return val in header_val

        return val == header_val

    @classmethod
    def message_source_equal(cls,
                             data: dict,
                             source: str,
                             content: str) -> bool:

        return cls.header_equal(data, 'source', source) and \
               cls.header_equal(data, 'content', content)

    @classmethod
    def message_target_equal(cls,
                             data: dict,
                             target: str,
                             content: str) -> bool:

        return cls.header_equal(data, 'target', target) and \
               cls.header_equal(data, 'content', content)

    @classmethod
    def json_to_str(cls, data: dict) -> dict:
        data['data'] = json.dumps(data['data'])
        return data

    @classmethod
    def str_to_json(cls, data: dict) -> dict:
        data['data'] = json.loads(data['data'])
        return data


class PlanningBridgeNamespace(DeepTaskBridgeNamespace):
    def __init__(self, *args, **kwargs):
        super(PlanningBridgeNamespace, self).__init__(*args, **kwargs)
        self.register_dialog_generation()

    def register_dialog_generation(self):
        subscriber = Topic(self.ros, '/taskExecution', 'std_msgs/String')
        subscriber.subscribe(self.callback_dialog_generation)

    def callback_dialog_generation(self, data: dict):
        data = self.str_to_json(data)

        if not self.message_source_equal(data, 'planning', 'dialog_generation'):
            return

        self.emit('dialog_generation', data)


class DialogBridgeNamespace(DeepTaskBridgeNamespace):
    def __init__(self, *args, **kwargs):
        super(DialogBridgeNamespace, self).__init__(*args, **kwargs)
        self.register_subscribe()

    def on_publish(self, data: dict):
        if not self.message_target_equal(data, 'dialog', 'dialog_generation'):
            return

        publisher = Topic(self.ros, '/taskExecution', 'std_msgs/String')
        message = Message(self.json_to_str(data))
        publisher.publish(message)

    def register_subscribe(self):
        subscriber = Topic(self.ros, '/taskCompletion', 'std_msgs/String')
        subscriber.subscribe(self.callback_subscribe)

    def callback_subscribe(self, data: dict):
        message = self.str_to_json(data)

        if not self.message_source_equal(message, 'dialog', 'dialog_generation'):
            return

        self.emit('subscribe', message)


class VisionBridgeNamespace(DeepTaskBridgeNamespace):
    def __init__(self, *args, **kwargs):
        super(VisionBridgeNamespace, self).__init__(*args, **kwargs)
        self.register_image_raw()

    def register_image_raw(self):
        subscriber = Topic(self.ros, '/recognition/image_raw', 'sensor_msgs/Image')
        subscriber.subscribe(self.callback_image_raw)

    def callback_image_raw(self, data: dict):
        self.emit('image_raw', data)


class SpeechBridgeNamespace(DeepTaskBridgeNamespace):
    def __init__(self, *args, **kwargs):
        super(SpeechBridgeNamespace, self).__init__(*args, **kwargs)

    def on_record(self, data: dict):
        publisher = Topic(self.ros, '/action/recorder_on', 'std_msgs/Bool')
        message = Message(data)
        publisher.publish(message)

    def on_test(self, data: dict):
        publisher = Topic(self.ros, '/recognition/speech', 'std_msgs/String')

        human_speech = data['data']

        data = {
            'data': {
                'header': {
                    'source': 'stt',
                    'target': ['planning'],
                    'content': 'human_speech',
                    'id': 1
                },
                'human_speech': {
                    'stt': human_speech,
                    'timestamp': timestamp()
                }
            }
        }

        rospy.loginfo(data)
        message = Message(self.json_to_str(data))
        publisher.publish(message)
