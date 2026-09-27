import asyncio
from aiocoap import *

async def main():
    protocol = await Context.create_client_context()
    
    # Apontando para a própria máquina para o teste local
    ip_servidor = "127.0.0.1" 
    
    # Cria a requisição GET para o recurso /sensor com a flag observe=0
    request = Message(code=GET, uri=f'coap://{ip_servidor}/sensor', observe=0)
    
    print(f"Assinando o recurso /sensor em {ip_servidor} (Modo Observe)...")
    
    try:
        requester = protocol.request(request)
        
        # Recebe a primeira resposta imediata
        response = await requester.response
        print(f"Leitura inicial recebida: {response.payload.decode('utf-8')}")

        # Entra em loop aguardando as notificações do servidor
        async for response in requester.observation:
            print(f"Atualização via Observe: {response.payload.decode('utf-8')}")
            
    except Exception as e:
        print(f"Falha na conexão: {e}")

if __name__ == "__main__":
    asyncio.run(main())