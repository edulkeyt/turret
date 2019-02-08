from http.server import HTTPServer, CGIHTTPRequestHandler
import time
import urllib
from servos import ServosController

SERVO_COMMAND_PARAMETER_NAME = "servos=";
FIRE_COMMAND_PARAMETER_NAME = "fire=";
SALVO_COMMAND_PARAMETER_NAME = "salvo";
YES_COMMAND_PARAMETER_NAME = "yes";
NO_COMMAND_PARAMETER_NAME = "no";

SERVO_ARGUMENTS_SEPARATOR = 'a';
HEIGHT_SERVO_MIN_DEGREE = 80;
HEIGHT_SERVO_DELTA_DEGREE = 40;
FIRE_SERVO_ANGLE = 50;

SERVER_ADDRESS = ("", 8000)

class MyHandler(CGIHTTPRequestHandler):

    sightAzimutDegree = 90;
    sightHeightDegree = 90;

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
            anglesInt = [int(angleStr) for angleStr in anglesStrings[:2]];
            anglesInt[1] = HEIGHT_SERVO_MIN_DEGREE + (anglesInt[1] * HEIGHT_SERVO_DELTA_DEGREE) / 180;
            self.sightAzimutDegree = anglesInt[0];
            self.sightHeightDegree = anglesInt[1];
            servos.setMg995PositionsFromDegreesStrings(anglesInt);
            return;

        if command.startswith(FIRE_COMMAND_PARAMETER_NAME):
            self.setHeaders();
            armNuber = int(command[len(FIRE_COMMAND_PARAMETER_NAME):]);
            servos.setSg90Position(armNuber, FIRE_SERVO_ANGLE);
            time.sleep(0.2);
            servos.setSg90Position(armNuber, 0);

        if command == SALVO_COMMAND_PARAMETER_NAME:
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

        if command == YES_COMMAND_PARAMETER_NAME:
            self.setHeaders();
            servos.setMg995PositionsFromDegreesStrings([sightAzimutDegree, sightHeightDegree - 10]);
            time.sleep(0.2);
            servos.setMg995PositionsFromDegreesStrings([sightAzimutDegree, sightHeightDegree + 10]);
            time.sleep(0.2);
            servos.setMg995PositionsFromDegreesStrings([sightAzimutDegree, sightHeightDegree]);
            

        if command == NO_COMMAND_PARAMETER_NAME:
            self.setHeaders();
            servos.setMg995PositionsFromDegreesStrings([sightAzimutDegree - 10, sightHeightDegree]);
            time.sleep(0.2);
            servos.setMg995PositionsFromDegreesStrings([sightAzimutDegree + 10, sightHeightDegree]);
            time.sleep(0.2);
            servos.setMg995PositionsFromDegreesStrings([sightAzimutDegree, sightHeightDegree]);

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
