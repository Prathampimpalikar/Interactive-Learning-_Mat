import http.server
import socketserver
import threading
import os

DEFAULT_PORT = 8001


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def start_server(port=DEFAULT_PORT):

    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)

    Handler = http.server.SimpleHTTPRequestHandler

    Handler.extensions_map.update({
        ".glb": "model/gltf-binary",
        ".gltf": "model/gltf+json",
        ".js": "application/javascript",
        ".json": "application/json",
        ".css": "text/css",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".svg": "image/svg+xml"
    })

    httpd = None
    current_port = port

    for p in [port, 8080, 8000, 5000]:

        try:
            httpd = ReusableTCPServer(("", p), Handler)
            current_port = p
            break

        except OSError:
            continue

    if httpd is None:

        print("Could not start server.")
        return None, None

    print("--------------------------------")
    print("Interactive Learning Mat")
    print("--------------------------------")
    print(f"Website: http://localhost:{current_port}")
    print("Server is running...")
    print("--------------------------------")

    thread = threading.Thread(
        target=httpd.serve_forever,
        daemon=True
    )

    thread.start()

    return httpd, current_port


if __name__ == "__main__":

    httpd, port = start_server()

    if httpd is not None:

        try:
            httpd.serve_forever()

        except KeyboardInterrupt:

            print("\nServer stopped.")

            httpd.shutdown()
            httpd.server_close()