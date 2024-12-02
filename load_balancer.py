import random
import requests
from flask import Flask, request
from serfclient import SerfClient

class LoadBalancer:
    def __init__(self, serf_client):
        self.serf_client = serf_client
        self.backends = []

    def update_backends(self):
        # Obtiene miembros desde el cliente Serf
        members_result = self.serf_client.members()
        members = members_result.body["Members"]  # Extrae los datos reales

        # Filtra miembros que están 'alive' y tienen la etiqueta 'backend_addr'
        self.backends = [
            member["Tags"]["backend_addr"]
            for member in members
            if member.get("Status", "") == "alive" and "backend_addr" in member.get("Tags", {})
        ]
        print(f"Updated backends: {self.backends}")  # Debug: Imprime la lista actualizada de backends

    def get_backend(self):
        # Selecciona aleatoriamente un backend de la lista
        if not self.backends:
            return None
        return random.choice(self.backends)

app = Flask(__name__)
serf_client = SerfClient()  # Inicializa el cliente Serf
load_balancer = LoadBalancer(serf_client)

@app.route('/request', methods=['POST'])
def handle_request():
    # Actualiza la lista de backends
    load_balancer.update_backends()
    backend = load_balancer.get_backend()

    if not backend:
        return "No backends available", 503

    # Reenvía la solicitud al backend seleccionado
    try:
        print(f"Forwarding request to backend: {backend}")
        response = requests.post(f"http://{backend}/process", json=request.json)
        return response.content, response.status_code
    except requests.RequestException as e:
        print(f"Error forwarding request to backend {backend}: {e}")
        return "Error forwarding request", 500

if __name__ == "__main__":
    print("Starting load balancer...")
    load_balancer.update_backends()
    app.run(host="0.0.0.0", port=5000)
