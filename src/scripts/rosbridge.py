from flask_socketio import Namespace
from roslibpy import Ros, Topic, Message


class RosBridgeNamespace(Namespace):
    __ros: Ros = None
    __ros_host: str = None
    __ros_port: int = None

    def __init__(self, host: str, port: int, *args, **kwargs):
        super(RosBridgeNamespace, self).__init__(*args, **kwargs)
        self.__ros_host = host
        self.__ros_port = port

    @property
    def ros(self):
        if not self.__ros:
            self.__ros = Ros(host=self.__ros_host, port=self.__ros_port)
            self.__ros.run()

        return self.__ros


class DialogBridgeNamespace(RosBridgeNamespace):
    def __init__(self, *args, **kwargs):
        super(DialogBridgeNamespace, self).__init__(*args, **kwargs)
        self.register_subscribe()

    def on_publish(self, data):
        publisher = Topic(self.ros, '/taskExecution', 'std_msgs/String')
        publisher.publish(Message(data))

    def register_subscribe(self):
        subscriber = Topic(self.ros, '/taskCompletion', 'std_msgs/String')
        subscriber.subscribe(self.callback_subscribe)

    def callback_subscribe(self, data):
        self.emit('subscribe', data)


class RecognitionBridgeNamespace(RosBridgeNamespace):
    def __init__(self, *args, **kwargs):
        super(RecognitionBridgeNamespace, self).__init__(*args, **kwargs)
        self.register_face_id()
        self.register_image_raw()

    def register_face_id(self):
        subscriber = Topic(self.ros, '/recognition/face_id', 'std_msgs/String')
        subscriber.subscribe(self.callback_face_id)

    def register_image_raw(self):
        subscriber = Topic(self.ros, '/recognition/image_raw', 'sensor_msgs/Image')
        subscriber.subscribe(self.callback_image_raw)

    def callback_face_id(self, data):
        self.emit('face_id', data)

    def callback_image_raw(self, data):
        self.emit('image_raw', data)
