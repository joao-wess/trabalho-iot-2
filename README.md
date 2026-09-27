# Simulador de Protocolo CoAP - IoT

Este repositório contém a implementação prática do protocolo CoAP (Constrained Application Protocol) para a disciplina de Aplicações de Cloud, IoT e Indústria 4.0.

O objetivo do laboratório é demonstrar a comunicação real entre duas máquinas na mesma rede Wi-Fi, operando no modelo requisição/resposta e publicação/assinatura (modo Observe).

## 🛠 Tecnologias Utilizadas

- **Python 3**
- **aiocoap:** Biblioteca recomendada para comunicação CoAP em Python puro.
- **matplotlib:** Geração do dashboard visual em tempo real para o cliente.
- **Wireshark:** Análise e evidência do tráfego de rede na porta 5683/UDP.

## ⚙️ Pré-requisitos e Instalação

1. Clone este repositório em sua máquina local.
2. Crie e ative um ambiente virtual (recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Linux/Mac
   venv\Scripts\activate     # No Windows
   ```
3. Instale as dependências necessárias:
   ```bash
   pip install aiocoap matplotlib
   ```

## 🚀 Roteiro de Execução (Apresentação)

A topologia do laboratório exige a divisão do sistema em dois notebooks distintos.

### Notebook A (Servidor e Evidência de Rede)

Este notebook hospeda o recurso `/sensor` e captura o tráfego.

1. Descubra o IP local da máquina na rede Wi-Fi (use `ipconfig` no Windows ou `ip a` no Linux).
2. **CRÍTICO:** Libere a porta no Firewall do sistema operacional. No Windows PowerShell (como Administrador), rode:
   ```powershell
   netsh advfirewall firewall add rule name="CoAP 5683 UDP" dir=in action=allow protocol=UDP localport=5683
   ```
3. Inicie o servidor:
   ```bash
   python servidor.py
   ```
4. Abra o Wireshark, selecione a interface Wi-Fi e aplique o filtro de captura: `udp.port == 5683`.

### Notebook B (Cliente e Dashboard)

Este notebook atua como assinante das telemetrias.

1. No arquivo `cliente_dashboard.py`, altere a variável `ip_servidor` para o IP anotado no Notebook A.
2. Inicie o cliente:
   ```bash
   python cliente_dashboard.py
   ```

Uma janela gráfica será aberta atualizando as leituras de temperatura automaticamente em tempo real.

## 🧪 Teste de Resiliência

Para comprovar a resiliência do modo Observe exigida na avaliação, interrompa a execução do `servidor.py` (Ctrl+C). O gráfico do cliente irá congelar e o tráfego no Wireshark cessará, comprovando o desacoplamento do protocolo sem causar falha crítica (crash) no cliente.
