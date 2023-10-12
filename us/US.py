import pickle
import socket
import requests
from flask import Flask, request
import logging as log

app = Flask(__name__)
BUFFER_SIZE = 2048

@app.route('/')
def hello_US():
    return 'Hello from the User Server (US)'

@app.route('/fibonacci', methods=["GET"])
def fibonacci():
    try:
        hostname = request.args.get('hostname').replace('"', '')
        fs_port = int(request.args.get('fs_port'))
        number = int(request.args.get('number'))
        as_ip = request.args.get('as_ip').replace('"', '')
        as_port = int(request.args.get('as_port'))

        socket_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_connection.sendto(pickle.dumps(("A", hostname)), (as_ip, as_port))
        response, _ = socket_connection.recvfrom(BUFFER_SIZE)
        response = pickle.loads(response)
        type, hostname, fs_ip, ttl = response

        if not fs_ip:
            return "Couldn't retrieve fs_ip"

        return requests.get(f"http://{fs_ip}:{fs_port}/fibonacci", params={"number": number}).content
    except Exception as e:
        log.error(f"Error: {str(e)}")
        return "An error occurred."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
