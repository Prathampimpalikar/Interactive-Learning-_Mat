import http.server
import socketserver
import threading
import os

PORT = 8001


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def start_server():

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    Handler = http.server.SimpleHTTPRequestHandler
    Handler.extensions_map['.glb'] = 'model/gltf-binary'
    Handler.extensions_map['.gltf'] = 'model/gltf+json'

    try:
        httpd = ReusableTCPServer(("", PORT), Handler)

    except OSError:
        print(f"Server already running on port {PORT}")
        return None

    print(f"Server Started : http://localhost:{PORT}")

    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()

    return httpd


if __name__ == "__main__":

    httpd = start_server()

    if httpd is not None:
        httpd.serve_forever()