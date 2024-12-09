import asyncio


async def handle_client(reader, writer):
    data = await reader.read(4096)
    raw_request = data.decode('utf-8')
    request_lines = raw_request.split('\n')
    first_line = request_lines[0] if request_lines else ''
    path = first_line.split(' ')[1] if ' ' in first_line else '/'

    if path == '/io':
        # 非同期I/Oで2秒待機
        await asyncio.sleep(2)
        response = 'HTTP/1.1 200 OK\n\nThis is the /io endpoint after 2 seconds!'
    else:
        response = 'HTTP/1.1 200 OK\n\nHello, World!'

    writer.write(response.encode('utf-8'))
    await writer.drain()
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(handle_client, host='127.0.0.1', port=8800)
    print("Server is running on http://127.0.0.1:8800")

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
