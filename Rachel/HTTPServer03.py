from http.server import BaseHTTPRequestHandler, HTTPServer
MyRequest = None
class RequestHandler_httpd( BaseHTTPRequestHandler):
    def do_GET(self):
        global MyRequest
        MyRequest = self.requestline
        MyRequest = MyRequest[5 : int(len(MyRequest) - 9) ]
        print('You recieved this request')
        print(MyRequest)
        messagetosend=bytes('Welcome to the HTTP sever',"utf")
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Content-Length', len(messagetosend))
        self.end_headers()
        self.wfile.write(messagetosend)
        return 

server_address_httpd = ('192.168.0.102',8080)
httpd = HTTPServer(server_address_httpd, RequestHandler_httpd)
print("Starting server:")
httpd.serve_forever()        