from http.server import BaseHTTPRequestHandler, HTTPServer
import json

app_name = ''


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self._echo_response()

    def do_POST(self):
        self._echo_response()

    def _echo_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        res = {}
        res['appName'] = app_name
        res['path'] = self.path
        self.wfile.write(bytes(json.dumps(res), 'utf-8'))


def run(port):
    server_address = ('', port)
    server = HTTPServer(server_address, Handler)
    server.serve_forever()


if __name__ == '__main__':
    from sys import argv

    app_name = argv[1]
    port = int(argv[2])
    print(f"Starting mock application {app_name} at port {port}.")
    run(port)
