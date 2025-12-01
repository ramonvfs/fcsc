import asyncio
import numpy as np

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

from mqtt_listener import MQTTClient
from fft_calc import calculate_fft
from websocket_manager import manager

app = FastAPI()

def fft_publisher_callback(axis_name: str, signal: list, distance: int):
    """
    Função chamada pelo MQTTClient, calcula a FFT e envia para o WebSocketManager.
    Roda na thread do MQTT.
    """

    status_distance = "normal" if distance <= 100 else "alerta"

    try:
        frequencies, magnitudes = calculate_fft(signal)

        data_to_send = {
            "axis": axis_name,
            "samples": len(signal),
            "accel": signal,
            "dominant_freq": float(frequencies[np.argmax(magnitudes[1:]) + 1]),
            "frequencies": frequencies.tolist(),
            "magnitudes": magnitudes.tolist(),
            "distance": distance,
            "status_distance": status_distance,
            "status_fft": "normal" if np.max(magnitudes) < 0.040 else "alerta"
        }

        asyncio.run(manager.send_fft_result(data_to_send))
        
        print(f"✅ FFT do Eixo {axis_name} calculada e enviada via WebSocket. Distância: {distance} mm")

    except Exception as e:
        print(f"🚨 Erro no processamento/envio da FFT para o Eixo {axis_name}: {e}")

@app.websocket("/ws/fft_data")
async def websocket_endpoint(websocket: WebSocket):
    """Rota para o frontend React se conectar."""
    await manager.connect(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text("Recebi: " + data)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"Erro na conexão WebSocket: {e}")
        manager.disconnect(websocket)
        
def start_mqtt_listener():
    """Inicia e roda o listener MQTT no loop síncrono da thread."""
    mqtt_client = MQTTClient(fft_callback=fft_publisher_callback)
    print("Iniciando o listener MQTT em thread separada...")
    mqtt_client.run()

@app.on_event("startup")
async def startup_event():
    # app.state.mqtt_task = await run_in_threadpool(start_mqtt_listener)
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, start_mqtt_listener)

@app.on_event("shutdown")
def shutdown_event():
    print("Encerrando o servidor e cliente MQTT...")

if __name__ == "__main__":
    # Inicia o servidor Uvicorn (o uvicorn é um servidor ASGI)
    uvicorn.run(app, host="0.0.0.0", port=8080)