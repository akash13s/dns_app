import socket
import pickle
from flask import Flask, request
import logging as log

app = Flask(__name__)
BUFFER_SIZE = 1024


@app.route('/')
def hello_fs():
    return "Hello from Fibonacci Server (FS)"


def get_fib(n):
    if n <= 0:
        raise ValueError("n should be greater than 0")
    elif n == 1:
        return 0
    elif n == 2:
        return 1

    fib_1, fib_2 = 0, 1
    result = 0

    for _ in range(3, n + 1):
        result = fib_1 + fib_2
        fib_1, fib_2 = fib_2, result

    return result


@app.route('/fibonacci')
def fibonacci():
    n = int(request.args.get('number'))
    return str(get_fib(n))


@app.route('/register', methods=['PUT'])
def register():
    try:
        body = request.json
        if body is None:
            raise ValueError("Request body is empty")

        hostname = body.get("hostname")
        fs_ip = body.get("fs_ip")
        as_ip = body.get("as_ip")
        as_port = body.get("as_port")
        ttl = body.get("ttl")

        if None in (hostname, fs_ip, as_ip, as_port, ttl):
            raise ValueError("Missing required fields in the request body")

        registration_data = (hostname, fs_ip, "A", ttl)
        msg_bytes = pickle.dumps(registration_data)

        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.sendto(msg_bytes, (as_ip, as_port))

        return "Registration Successful!"
    except Exception as e:
        log.error(f"Registration error: {str(e)}")
        return "Registration Failed!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090, debug=True)
