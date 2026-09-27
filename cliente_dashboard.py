import asyncio
import matplotlib.pyplot as plt
from aiocoap import *

# Configuração inicial do gráfico
plt.ion() # Ativa o modo interativo
fig, ax = plt.subplots()
x_data, y_data = [], []
linha, = ax.plot(x_data, y_data, 'b-', marker='o')

ax.set_title("Dashboard CoAP - Monitoramento de Temperatura")
ax.set_ylabel("Temperatura (°C)")
ax.set_xlabel("Leituras (Tempo)")
ax.grid(True)

async def main():
    protocol = await Context.create_client_context()
    ip_servidor = "127.0.0.1" # Apontando para o localhost
    
    # Requisição GET com a flag observe=0
    request = Message(code=GET, uri=f'coap://{ip_servidor}/sensor', observe=0)
    print(f"Iniciando Dashboard Visual (Modo Observe em {ip_servidor})...")
    
    try:
        requester = protocol.request(request)
        response = await requester.response
        
        # Loop aguardando as notificações contínuas do servidor
        async for response in requester.observation:
            payload = response.payload.decode('utf-8')
            print(f"Atualização no terminal: {payload}")
            
            # Extrai apenas o valor numérico (ex: "Temperatura: 25.50 °C" -> 25.50)
            temp = float(payload.split()[1])
            
            # Alimenta os dados do gráfico
            y_data.append(temp)
            x_data.append(len(y_data))
            
            # Atualiza a linha e ajusta os eixos dinamicamente
            linha.set_xdata(x_data)
            linha.set_ydata(y_data)
            ax.relim()
            ax.autoscale_view()
            
            # Pausa breve para o matplotlib renderizar o novo quadro
            plt.draw()
            plt.pause(0.01)
            
    except Exception as e:
        print(f"Conexão interrompida ou falha: {e}")

if __name__ == "__main__":
    asyncio.run(main())