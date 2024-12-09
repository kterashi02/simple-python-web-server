import socket
import time


def view(raw_request):
    request_lines = raw_request.split('\n')
    first_line = request_lines[0] if request_lines else ''
    path = first_line.split(' ')[1] if ' ' in first_line else '/'

    if path == '/io':
        # 2秒間のI/O待機
        time.sleep(2)
        return 'HTTP/1.1 200 OK\n\nThis is the /io endpoint after 2 seconds!'
    else:
        return 'HTTP/1.1 200 OK\n\nHello, World!'


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 8800))
        s.listen()
        print("Server is running on http://127.0.0.1:8800")
        while True:
            conn, addr = s.accept()
            with conn:
                raw_request = b''
                while True:
                    chunk = conn.recv(4096)
                    raw_request += chunk
                    if len(chunk) < 4096:
                        break
                raw_response = view(raw_request.decode('utf-8'))
                conn.sendall(raw_response.encode('utf-8'))


if __name__ == '__main__':
    main()

