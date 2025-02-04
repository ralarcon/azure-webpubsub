import json
import sys

from http.server import HTTPServer, SimpleHTTPRequestHandler

from azure.messaging.webpubsubservice import WebPubSubServiceClient

service = WebPubSubServiceClient.from_connection_string(sys.argv[1], hub='stream')

class Resquest(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'public/index.html'
            return SimpleHTTPRequestHandler.do_GET(self)
        elif self.path == '/negotiate':
            roles = ['webpubsub.sendToGroup.stream',
                     'webpubsub.joinLeaveGroup.stream']
            token = service.get_client_access_token(roles=roles)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'url': token['url']
            }).encode())


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python server.py <connection-string>')
        exit(1)

    server = HTTPServer(('localhost', 8080), Resquest)
    print('server started')
    server.serve_forever()
