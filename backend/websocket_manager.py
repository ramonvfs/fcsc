import json
from typing import List, Dict, Any
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Aceita e adiciona uma nova conexão WebSocket."""
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"Novo cliente conectado. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        """Remove uma conexão que foi fechada."""
        self.active_connections.remove(websocket)
        print(f"Cliente desconectado. Total: {len(self.active_connections)}")

    async def send_fft_result(self, data: Dict[str, Any]):
        """Envia o resultado da FFT para todos os clientes conectados."""
        
        # Converte o dicionário de dados em uma string JSON
        message = json.dumps(data)
        
        # Envia a mensagem de forma assíncrona para cada cliente
        for connection in self.active_connections:
            try:
                # O send_text é o método do FastAPI para enviar dados via WebSocket
                await connection.send_text(message)
            except WebSocketDisconnect:
                # Caso a conexão caia durante o envio
                self.disconnect(connection)
            except Exception as e:
                print(f"Erro ao enviar para cliente: {e}")

# Cria uma instância global do gerenciador
manager = ConnectionManager()