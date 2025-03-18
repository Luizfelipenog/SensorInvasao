import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
import socket
import threading
from kivy.clock import Clock

class AppSeguranca(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text="Modo de Segurança: DESATIVADO")
        self.button = Button(text="Ativar Segurança")
        self.button.bind(on_press=self.toggle_segurança)

        # Criar widget de câmera
        self.camera = Camera(play=True, resolution=(640, 480))  # Ativar a câmera com resolução
        self.camera.texture = None  # Iniciar sem textura

        self.layout.add_widget(self.label)
        self.layout.add_widget(self.button)
        self.layout.add_widget(self.camera)

        return self.layout

    def toggle_segurança(self, instance):
        # Alterna o modo de segurança (ativar/desativar)
        if self.label.text == "Modo de Segurança: DESATIVADO":
            self.label.text = "Modo de Segurança: ATIVADO"
            self.iniciar_monitoramento()
        else:
            self.label.text = "Modo de Segurança: DESATIVADO"
            self.parar_monitoramento()

    def iniciar_monitoramento(self):
        # Inicia a comunicação via socket e o monitoramento da câmera
        threading.Thread(target=self.monitorar_proximidade).start()

    def parar_monitoramento(self):
        # Lógica para parar o monitoramento (ex: fechando sockets)
        pass

    def monitorar_proximidade(self):
        # Simulação de detecção de proximidade (substitua com código real de sensor)
        proximidade_detectada = True  # Simulação de detecção
        if proximidade_detectada:
            self.enviar_alerta()
            # Agendar a captura de imagem no thread principal
            Clock.schedule_once(self.capturar_imagem, 0)

    def enviar_alerta(self):
        # Envia um alerta para o servidor
        try:
            cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente_socket.connect(('127.0.0.1', 12345))  # Substitua pelo IP real do servidor
            cliente_socket.send(b'ALERTA')
            cliente_socket.close()
            print("Alerta enviado!")
        except Exception as e:
            print(f"Erro ao enviar alerta: {e}")

    def capturar_imagem(self, dt):
        # Captura uma imagem (simulada)
        if self.camera.texture:
            # Salvar a imagem usando a textura da câmera
            self.camera.texture.save("intruso.png")  # Salvando a imagem capturada como PNG
            print("Imagem capturada e salva como intruso.png")
        else:
            print("Erro: Nenhuma imagem disponível na câmera.")

if __name__ == "__main__":
    AppSeguranca().run()
