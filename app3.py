from multiprocessing import Process
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
    
def handle_client(conn):

    with conn:
        raw_request = b''
        while True:
            chunk = conn.recv(4096)
            raw_request += chunk
            if len(chunk) < 4096:
                break
        raw_response = view(raw_request.decode('utf-8'))
        conn.sendall(raw_response.encode('utf-8'))

def worker_process(server_socket):
    while True:
        conn, addr = server_socket.accept()
        handle_client(conn)



def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 8800))
        s.listen()
        print("Server is running on http://127.0.0.1:8800")
        processes = []
        num_processes = 4
        # 子プロセスを作成
        for i in range(num_processes):
            p = Process(target=worker_process, args=(s,))
            p.start()
            print(f"Worker {i + 1} has been created.")
            processes.append(p)
        # メインプロセスが子プロセスの終了を待つ
        try:
            for p in processes:
                p.join()
        except KeyboardInterrupt:
            print("Shutting down...")
            for p in processes:
                p.terminate()
                p.join()

if __name__ == '__main__':
    main()
