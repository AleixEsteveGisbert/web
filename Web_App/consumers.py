from channels.generic.websocket import WebsocketConsumer

from Web_App.models import ConsoleMessage


class MinecraftConsoleConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        # Obtener los mensajes existentes de la consola y enviarlos al cliente WebSocket
        console_messages = ConsoleMessage.objects.all().order_by('-created_at')[:50]
        for message in reversed(console_messages):
            self.send(message.message)

    def disconnect(self, close_code):
        # Implementa la lógica de desconexión si es necesario
        pass

    def receive(self, text_data):
        # Implementa la lógica para enviar comandos al servidor de Minecraft
        pass