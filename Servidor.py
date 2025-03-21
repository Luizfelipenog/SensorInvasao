import socket
import pygame
import os
import threading
import tkinter as tk

# Inicializa o pygame para tocar o som
pygame.mixer.init()

# Variável global para verificar se o alarme está tocando
alarm_playing = False

def load_alarm_sound():
    """Carrega o som do alarme."""
    try:
        pygame.mixer.music.load("alarm-no3-14864.mp3")
        print("🔊 Som carregado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao carregar o som: {e}")

def play_alarm():
    """Toca o som do alarme em uma thread separada."""
    global alarm_playing
    if alarm_playing:
        return  # O alarme já está tocando, não faz sentido tocar novamente.

    def play():
        try:
            global alarm_playing
            alarm_playing = True
            print("🚨 Tocando o alarme...")
            pygame.mixer.music.play(-1)  # -1 faz o som tocar em loop
        except Exception as e:
            print(f"❌ Erro ao tocar o alarme: {e}")

    threading.Thread(target=play, daemon=True).start()

def stop_alarm():
    """Para o som do alarme."""
    global alarm_playing
    if not alarm_playing:
        return  # O alarme não está tocando.

    try:
        print("🔇 Parando o alarme...")
        pygame.mixer.music.stop()
        alarm_playing = False
    except Exception as e:
        print(f"❌ Erro ao parar o alarme: {e}")

def receive_image(conn):
    """Recebe a imagem e salva no servidor."""
    print("📥 Recebendo imagem...")

    image_data = b""
    
    while True:
        part = conn.recv(4096)  # Recebe os dados em partes
        if not part:
            break
        
        # Verifica se encontramos o marcador "FIM_IMAGEM"
        if b"FIM_IMAGEM" in part:
            image_data += part.split(b"FIM_IMAGEM")[0]
            break
        image_data += part
    
    # Definindo o caminho para salvar a imagem
    image_path = os.path.join(os.getcwd(), "captura.jpg")
    try:
        with open(image_path, "wb") as f:
            f.write(image_data)
        print(f"📸 Imagem salva como {image_path}")
    except Exception as e:
        print(f"❌ Erro ao salvar a imagem: {e}")


def handle_client(conn, addr):
    """Lida com um cliente conectado (recebe alertas e imagens simultaneamente)."""
    print(f"✅ Conexão estabelecida com {addr}")
    load_alarm_sound()

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            
            message = data.decode('utf-8', errors='ignore').strip()
            
            if message == "ALERTA":
                print("🚨 ALERTA RECEBIDO! Tocando som...")
                play_alarm()
            
            elif message == "IMAGEM":
                print("📸 Iniciando recebimento da imagem...")
                threading.Thread(target=receive_image, args=(conn,), daemon=True).start()

    except Exception as e:
        print(f"❌ Erro no cliente {addr}: {e}")
    finally:
        conn.close()
        print(f"🔌 Conexão encerrada com {addr}")

def start_server():
    """Inicia o servidor TCP para receber alertas e imagens de múltiplos clientes."""
    HOST = '0.0.0.0'
    PORT = 50000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"📡 Servidor escutando na porta {PORT}...")

    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        client_thread.start()

def start_server_thread():
    """Inicia o servidor TCP em uma thread separada."""
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

def create_gui():
    """Cria a interface gráfica com Tkinter."""
    root = tk.Tk()
    root.title("Servidor de Segurança")
    root.geometry("300x200")

    label = tk.Label(root, text="Clique no botão para parar o alarme", font=("Arial", 12))
    label.pack(pady=20)

    stop_button = tk.Button(root, text="Parar Alarme", command=stop_alarm, font=("Arial", 14), bg="red", fg="white")
    stop_button.pack(pady=20)

    start_server_thread()

    root.mainloop()

if __name__ == "__main__":
    create_gui()
