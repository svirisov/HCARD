from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading

class FlaskServer:
    def __init__(self, host="192.168.22.253", port=8080):
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        self.host = host
        self.port = port

        @self.app.route("/")
        def index():
            return render_template('home3.html')

        @self.socketio.on("connect")
        def handle_connect():
            print("Client connected")

        @self.socketio.on("disconnect")
        def handle_disconnect():
            print("Client disconnected")

        @self.socketio.on("message")
        def handle_message(data):
            print("Received message:", data)

    def run(self):
        try:
            self.thread = threading.Thread(target=self._run_server, daemon=True)
            self.thread.start()
        except KeyboardInterrupt:
            print("Server stopped")
        finally:
            self.thread.join(timeout=5)

    def _run_server(self): # internal to run server as thread
        self.socketio.run(self.app, host=self.host,  port=5004, debug=False)

    def send_message(self, event, data):
        self.socketio.emit(event, data)