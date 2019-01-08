import json
import paho.mqtt.client as mqtt


class Mqtt():
    def __init__(self, server):
        self.__server = server

    def publish(self, data, id_client, topic_name):
        try:
            mqttc = mqtt.Client(client_id=id_client)
            mqttc.connect(self.__server, 1883)
            mqttc.publish(topic_name, data)
            mqttc.loop(2)
            print("ENVIADO: {}".format(data))
        except BaseException:
            print("Error to publish MQTT")
