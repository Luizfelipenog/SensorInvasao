import socket
import os
from PIL import Image
from io import BytesIO
import wave
import threading
import time

# Configuração do servidor
HOST = '0.0.0.0'  # Aceitar conexões de qualquer IP
PORTA = 12345  # Porta de conexão do socket
DIRETORIO_IMAGENS = 'imagens_capturadas'  # Diretório onde as imagens serão armazenadas

# Função para criar o diretório de imagens, caso não exista
def criar_diretorio_imagens():
    if not os.path.exists(DIRETORIO_IMAGENS):
        os.makedirs(DIRETORIO_IMAGENS)

# Função para salvar a imagem recebida do cliente
def salvar_imagem(dados_imagem):
    try:
        # Gerar nome de arquivo único com base no timestamp
        timestamp = int(time.time())
        caminho_imagem = os.path.join(DIRETORIO_IMAGENS, f'intruso_{timestamp}.png')
        
        # Converter os dados de imagem recebidos em uma imagem
        imagem = Image.open(BytesIO(dados_imagem))
        imagem.save(caminho_imagem)
        print(f"Imagem salva como {caminho_imagem}")
    except Exception as e:
        print(f"Erro ao salvar imagem: {e}")

# Função para tocar um alarme sonoro (arquivo .wav)
def tocar_alarme():
    try:
        # Caminho para o arquivo de alarme
        caminho_alarme = 'alarme.wav'
        with wave.open(caminho_alarme, 'rb') as arquivo_alarme:
            # Reproduzir o som (simulando, pois a reprodução real depende de biblioteca externa)
            print("Tocando alarme sonoro!")
            # Aqui você pode usar bibliotecas como `pygame` para tocar o alarme
    except Exception as e:
        print(f"Erro ao tocar o alarme: {e}")

# Função para lidar com a conexão do cliente
def tratar_conexao_cliente(conn, addr):
    print(f"Conexão recebida de {addr}")
    
    try:
        while True:
            # Receber o sinal de alerta do cliente
            mensagem_alerta = conn.recv(1024).decode('utf-8')
            if not mensagem_alerta:
                break

            if mensagem_alerta == 'Alerta! Intruso detectado!':
                print("Alerta recebido!")
                tocar_alarme()  # Ativar alarme sonoro

                # Esperar um tempo e receber a imagem do intruso
                tamanho_imagem = int(conn.recv(1024).decode('utf-8'))  # Tamanho da imagem
                conn.send(b'OK')  # Confirmar que o tamanho da imagem foi recebido

                dados_imagem = b''
                while len(dados_imagem) < tamanho_imagem:
                    dados_imagem += conn.recv(1024)
                
                salvar_imagem(dados_imagem)  # Salvar imagem

                conn.send(b'Imagem recebida e salva')  # Confirmar recebimento da imagem

    except Exception as e:
        print(f"Erro ao processar a conexão: {e}")
    finally:
        conn.close()
        print(f"Conexão com {addr} encerrada.")

# Função principal para iniciar o servidor
def iniciar_servidor():
    criar_diretorio_imagens()  # Garantir que o diretório de imagens exista

    # Criar socket e vincular à porta
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor_socket:
        servidor_socket.bind((HOST, PORTA))
        servidor_socket.listen(5)
        print(f"Servidor ouvindo na porta {PORTA}...")

        while True:
            # Aceitar conexões de clientes
            conn, addr = servidor_socket.accept()
            thread_cliente = threading.Thread(target=tratar_conexao_cliente, args=(conn, addr))
            thread_cliente.start()  # Iniciar uma nova thread para cada cliente

if __name__ == '__main__':
    iniciar_servidor()
