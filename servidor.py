import asyncio
import aiocoap.resource as resource
import aiocoap
import random

class SensorResource(resource.ObservableResource):
    def __init__(self):
        super().__init__()
        self.temperatura = 25.0
        # Inicia a rotina de gerar dados em segundo plano
        self.notify_task = asyncio.create_task(self.atualizar_sensor())

    async def atualizar_sensor(self):
        while True:
            await asyncio.sleep(2) # Tempo entre as leituras
            self.temperatura += random.uniform(-0.5, 0.5)
            print(f"Sensor gerou nova leitura: {self.temperatura:.2f} °C")
            self.updated_state() # Dispara a notificação para os clientes do modo Observe

    async def render_get(self, request):
        # Resposta padrão quando alguém faz um GET
        payload = f"Temperatura: {self.temperatura:.2f} °C".encode('utf-8')
        return aiocoap.Message(payload=payload)

async def main():
    # Cria a árvore de recursos e adiciona o /sensor
    root = resource.Site()
    root.add_resource(['sensor'], SensorResource())
    
    # Sobe o servidor CoAP na porta 5683 UDP
    await aiocoap.Context.create_server_context(root, bind=('0.0.0.0', 5683))
    print("Servidor CoAP rodando na porta 5683 (UDP)...")
    
    # Mantém o servidor rodando infinitamente
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    asyncio.run(main())