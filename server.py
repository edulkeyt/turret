from http.server import HTTPServer, CGIHTTPRequestHandler
import time
import urllib
from servos import ServosController

SERVO_COMMAND_PARAMETER_NAME = "servos=";
FIRE_COMMAND_PARAMETER_NAME = "fire=";
SALVO_COMMAND_PARAMETER_NAME = "salvo";
FIRE_SERVO_ANGLE = 50;

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
            servos.setSg90Position(armNuber, FIRE_SERVO_ANGLE);
            time.sleep(0.2);
            servos.setSg90Position(armNuber, 0);

        if command.startswith(SALVO_COMMAND_PARAMETER_NAME):
            self.setHeaders();
            servos.setSg90Position(0, FIRE_SERVO_ANGLE);
            servos.setSg90Position(1, FIRE_SERVO_ANGLE);
            servos.setSg90Position(2, FIRE_SERVO_ANGLE);
            servos.setSg90Position(3, FIRE_SERVO_ANGLE);
            time.sleep(0.3);
            servos.setSg90Position(0, 0);
            servos.setSg90Position(1, 0);
            servos.setSg90Position(2, 0);
            servos.setSg90Position(3, 0);

        super().do_GET();        
        return;

servos = ServosController();
servos.setSg90Position(0, 0);
servos.setSg90Position(1, 0);
servos.setSg90Position(2, 0);
servos.setSg90Position(3, 0);

httpd = HTTPServer(SERVER_ADDRESS, MyHandler)
print("Server started")
httpd.serve_forever()
