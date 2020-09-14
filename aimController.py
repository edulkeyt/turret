CAMERA_X_FOV_ANGLE_DEGREES = 90;
CAMERA_X_RESOLUTION_PIXELS = 320;

SERVO_X_MIN_ANGLE_DEGREES = 10;
SERVO_X_MAX_ANGLE_DEGREES = 170;
SERVO_X_ROTATION_MULTIPLIER = 1;
SERVO_X_ROTATION_MAX_SPEED_ANGLES = 10;

class AimController:
    def calculateAngle(self, currentServoAngle, aimXAPixels, aimXBPixels):
        aimXPixels = (aimXAPixels + aimXBPixels) // 2;
        deltaPixels = CAMERA_X_RESOLUTION_PIXELS // 2 - aimXPixels;
        #print(deltaPixels);

        deltaAngles = deltaPixels * CAMERA_X_FOV_ANGLE_DEGREES // CAMERA_X_RESOLUTION_PIXELS;
        deltaAngles = deltaAngles * SERVO_X_ROTATION_MULTIPLIER;
        deltaAngles = min(-SERVO_X_ROTATION_MAX_SPEED_ANGLES, deltaAngles);
        deltaAngles = max(SERVO_X_ROTATION_MAX_SPEED_ANGLES, deltaAngles);
        #print(deltaAngles);

        result = currentServoAngle + deltaAngles;
        result = min(result, SERVO_X_MAX_ANGLE_DEGREES);
        result = max(result, SERVO_X_MIN_ANGLE_DEGREES);
        #print(result);

        return result;
