from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading

class FlaskServer:
    def __init__(self, host="127.0.0.1", port=5000):
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        self.host = host
        self.port = port

        @self.app.route("/")
        def index():
            return render_template('home.html')

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
        self.thread = threading.Thread(target=self._run_server, daemon=True)
        self.thread.start()

    def _run_server(self): # internal to run server as thread
        self.socketio.run(self.app, host=self.host, port=self.port, debug=False)

    def send_message(self, event, data):
        self.socketio.emit(event, data)