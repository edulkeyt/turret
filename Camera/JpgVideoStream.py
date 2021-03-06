# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Lock, Thread
import cv2
import io
from imutils.video import FPS
import datetime
 
class JpgVideoStream:
	def __init__(self, resolution=(320, 240), framerate=32):
		# initialize the camera and stream
		self.camera = PiCamera()
		self.camera.resolution = resolution
		self.camera.framerate = framerate
		self.rawCapture = io.BytesIO()
		self.stream = self.camera.capture_continuous(self.rawCapture,
			format="jpeg")
		#self.stream = self.camera.capture_continuous(self.rawCapture, "jpeg");
 
		# initialize the frame and the variable used to indicate
		# if the thread should be stopped
		self.frame = None
		self.stopped = False
		#self.lock = Lock()
	def start(self):
		# start the thread to read frames from the video stream
		t = Thread(target=self.update, args=())
		t.daemon = True
		t.start()
		self._startTime = datetime.datetime.now()
		return self
 
	def update(self):
		# keep looping infinitely until the thread is stopped
		for f in self.stream:
			# grab the frame from the stream and clear the stream in
			# preparation for the next frame
			#self.frame = bytearray(self.rawCapture)
			#self.lock.acquire()
			#print self.lock.locked()
			self.frame = self.rawCapture
			#print 1/(datetime.datetime.now() - self._startTime).total_seconds()
			self._startTime = datetime.datetime.now()
			#self.lock.release()
			#self.rawCapture.truncate(0)
 
			# if the thread indicator variable is set, stop the thread
			# and resource camera resources
			if self.stopped:
				self.stream.close()
				self.rawCapture.close()
				self.camera.close()
				return
	def read(self):
		# return the frame most recently read
		return self.frame
 
	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True
