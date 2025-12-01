from paho.mqtt import client as mqtt_client
import json

class MQTTClient:
    def __init__(self, client_id="python-mqtt-client", broker="127.0.0.1", port=1883, topic="esp32/mpu6050", fft_callback=None):
        self.client = mqtt_client.Client(client_id=client_id)
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message
        self.broker = broker
        self.port = port
        self.topic = topic
        self.fft_callback = fft_callback

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

        try:
            print("Attempting to reconnect...")
            self.client.reconnect()
            print("Reconnected successfully!")
            return
        except Exception as e:
            print(f"Reconnect failed: {e}")

    def _on_message(self, client, userdata, msg):
        try:
            # 1. Decodificar e carregar o JSON
            payload_str = msg.payload.decode('utf-8')
            data_json = json.loads(payload_str)

            distance = data_json.get("distance", None)
            
            # 2. Verificar e extrair a lista de amostras
            if 'samples' not in data_json or not isinstance(data_json['samples'], list):
                print("🚨 Erro: A chave 'samples' não foi encontrada ou não é uma lista.")
                return

            samples_list = data_json['samples']
            
            # 3. Separar os dados em 3 listas (Eixos X, Y e Z)
            ax_signal = []
            ay_signal = []
            az_signal = []
            
            for sample in samples_list:
                # 💡 Assumindo que 'ax', 'ay', 'az' são as chaves float
                ax_signal.append(sample.get('ax', 0.0))
                ay_signal.append(sample.get('ay', 0.0))
                az_signal.append(sample.get('az', 0.0))
            
            # 4. Chamar o callback de processamento (FFT) para CADA EIXO
            print(f"Lote recebido. Processando {len(samples_list)} amostras por eixo.")
            
            # O callback de FFT precisa agora saber qual eixo está processando
            self.fft_callback("X", ax_signal, distance)
            self.fft_callback("Y", ay_signal, distance)
            self.fft_callback("Z", az_signal, distance)

        except json.JSONDecodeError:
            print(f"🚨 Erro ao decodificar JSON: {payload_str[:100]}...") # Limita a exibição para não poluir
        except Exception as e:
            print(f"🚨 Erro de processamento no _on_message: {e}")

# ... (restante da classe)

    def run(self):
        self.connect()
        self.subscribe()
        self.client.loop_forever()