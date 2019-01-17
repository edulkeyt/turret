import Adafruit_PCA9685


SG90_MAX_ANGLE = 180;
SG90_MIN_PULSE = 130;
SG90_PULSE_DELTA = 470;
SG90_PINS_NUMBER_OFFSET = 4;

MG995_MAX_ANGLE = 180;
MG995_MIN_PULSE = 110;
MG995_PULSE_DELTA = 485;

PCA9685_FREQUENCY = 60;


class ServosController:

	pca9685 = Adafruit_PCA9685.PCA9685()
	pca9685.set_pwm_freq(PCA9685_FREQUENCY)

	def setSg90PositionsFromDegreesStrings(self, strings):
	    for i, substring in enumerate(strings):
	        angle = int(substring);
	        pulse = int(SG90_MIN_PULSE + angle * SG90_PULSE_DELTA / SG90_MAX_ANGLE);
	        self.pca9685.set_pwm(i + SG90_PINS_NUMBER_OFFSET, 0, pulse);
			
	def setMg995PositionsFromDegreesStrings(self, strings):
	    for i, substring in enumerate(strings):
	        angle = int(substring);
	        pulse = int(MG995_MIN_PULSE + angle * MG995_PULSE_DELTA / MG995_MAX_ANGLE);
	        self.pca9685.set_pwm(i, 0, pulse);
