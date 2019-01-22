from http.server import HTTPServer, CGIHTTPRequestHandler
import time
import urllib
from servos import ServosController

SERVO_COMMAND_PARAMETER_NAME = "servos=";
FIRE_COMMAND_PARAMETER_NAME = "fire=";

SERVO_ARGUMENTS_SEPARATOR = 'a';

SERVER_ADDRESS = ("", 8000)

class MyHandler(CGIHTTPRequestHandler):

    def setHeaders(self):
        self.send_response(200);
        self.send_header('Content-type', 'text/html');
        self.end_headers();

    def do_HEAD(self):
        self.setHeaders();
    
    def do_GET(self):

        command = self.path[1:];        

        if command.startswith(SERVO_COMMAND_PARAMETER_NAME):
            self.setHeaders();
            anglesStrings = command[len(SERVO_COMMAND_PARAMETER_NAME):].split(SERVO_ARGUMENTS_SEPARATOR);
            servos.setMg995PositionsFromDegreesStrings(anglesStrings[:2]);
            return;        

        if command.startswith(FIRE_COMMAND_PARAMETER_NAME):
            self.setHeaders();
            armNuber = int(command[len(FIRE_COMMAND_PARAMETER_NAME):]);
            print(armNuber);
            servos.setSg90Position(armNuber, 0);
            time.sleep(0.3);
            servos.setSg90Position(armNuber, 90);
            time.sleep(0.3);
            servos.setSg90Position(armNuber, 0);

        super().do_GET();        
        return;

servos = ServosController();

httpd = HTTPServer(SERVER_ADDRESS, MyHandler)
print("Server started")
httpd.serve_forever()
