# serf-implementation
dynamic load balancer using service discovery to manage backend nodes in a distributed system. It detects available services in real-time, updating the load balancer as nodes join or leave the network

## Run the proyect
Install libraries and serf
pip install flask requests serfclient
curl -LO https://releases.hashicorp.com/serf/0.8.2/serf_0.8.2_linux_amd64.zip
unzip serf_0.8.2_linux_amd64.zip
sudo mv serf /usr/local/bin/

Run backend node. To add more nodes, just change the node name and port on the code.
  Check the status with 
  serf members

Run load balancer.

Send a request to the load balancer using curl.
curl -X POST http://127.0.0.1:5000/request -H "Content-Type: application/json" -d '{"message": "Hello World"}'

You should see:
  -On load balancer terminal
  Forwarding request to backend: 127.0.0.1:8000
  -On backend terminal
  Processed: Hello World

