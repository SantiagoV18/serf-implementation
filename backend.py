import subprocess
import atexit
from flask import Flask, request

class Backend:
    def __init__(self, node_name, bind_addr, backend_addr):
        self.node_name = node_name
        self.bind_addr = bind_addr
        self.backend_addr = backend_addr
        self.serf_process = None

    def start(self):
        # Inicia el agente Serf como un proceso externo
        self.serf_process = subprocess.Popen(
            ["serf", "agent", "-node", self.node_name, "-bind", self.bind_addr],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        atexit.register(self.stop)  # Asegura detener Serf al salir
        print(f"Backend {self.node_name} started at {self.bind_addr}.")

        # Configura las etiquetas para este nodo
        subprocess.run([
            "serf", "tags",
            "-rpc-addr=127.0.0.1:7373",  # Dirección RPC por defecto
            "-set", f"backend_addr={self.backend_addr}"
        ])

    def stop(self):
        if self.serf_process:
            self.serf_process.terminate()
            self.serf_process.wait()
            print(f"Backend {self.node_name} stopped.")

app = Flask(__name__)
backend = Backend("backend1", "127.0.0.1:7946", "127.0.0.1:8000")

@app.route('/process', methods=['POST'])
def process_request():
    data = request.json
    return f"Processed: {data['message']}", 200

if __name__ == "__main__":
    backend.start()
    try:
        app.run(host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        backend.stop()
