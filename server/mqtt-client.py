from paho.mqtt import client as mqtt_client

class MQTTClient:
    def __init__(self, client_id="python-mqtt-client", broker="127.0.0.1", port=1883, topic="esp32/mpu6050"):
        self.client = mqtt_client.Client(client_id=client_id)
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message
        self.broker = broker
        self.port = port
        self.topic = topic
        self.max_reconnect_attempts = 10

    def connect(self):
        self.client.connect(self.broker, self.port)

    def disconnect(self):
        self.client.disconnect()

    def subscribe(self):
        self.client.subscribe(self.topic)
    
    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code: {rc}")

    def _on_disconnect(self, client, userdata, rc):
        print(f"Disconnected from MQTT Broker, return code: {rc}")

        reconnect_attempts = 0

        while reconnect_attempts < self.max_reconnect_attempts:
            try:
                print("Attempting to reconnect...")
                self.client.reconnect()
                print("Reconnected successfully!")
                return
            except Exception as e:
                reconnect_attempts += 1
                print(f"Reconnect attempt {reconnect_attempts} failed: {e}")

    def _on_message(self, client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    def run(self):
        self.connect()
        self.subscribe()
        self.client.loop_forever()

if __name__ == "__main__":
    mqtt_client = MQTTClient()
    mqtt_client.run()