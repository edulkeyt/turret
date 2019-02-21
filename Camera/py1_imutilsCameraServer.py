#!/usr/bin/python
'''
  Author: Ismael Benito Altamirano 
  
  Based on a Simple mjpg stream http server for the Raspberry Pi Camera
  inspired by https://gist.github.com/n3wtron/4624820
  by Igor Maculan - n3wtron@gmail.com
  
'''

import SimpleHTTPServer
import SocketServer
import io
import time
import picamera
import cgi
from os import curdir, sep
import logging
from __future__ import print_function
from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import imutils
import time
import cv2
 
# We need to declare the camera object empty to implement the server Handler.  
camera=None

# Dict that acts as a "mod_rewrite": 
rewrite = {"/": "/index.html",
		   "/index.html": "/index.html",
		   "/index.php": "/index.html",
		   "/index": "/index.html"}
		   
 
# Server Handler is defined as a Class.    
class CamHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_GET(self):
	# When a GET solicitude comes into the server, then execute this:
		if self.path.endswith('.mjpg'):
			# If mjpg stream is required, take image and send it. 
			self.send_response(200)
			self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
			self.end_headers()
			stream=io.BytesIO()
			try:
				# Taking images from Raspberry pi camera:
				start=time.time()
				while fps._numFrames < args["num_frames"]:
	                # grab the frame from the threaded video stream and resize it
	                # to have a maximum width of 400 pixels
	                frame = vs.read()
	                frame = imutils.resize(frame, width=400)
	                stream.write(bytearray(frame))
	                # check to see if the frame should be displayed to our screen
	                #if args["display"] > 0:
	                    #cv2.imshow("Frame", frame)
	                    #key = cv2.waitKey(1) & 0xFF
 
	                # update the FPS counter
	                fps.update()
				# for foo in camera.capture_continuous(stream,'jpeg'):
					self.wfile.write("--jpgboundary")
					self.send_header('Content-type','image/jpeg')
					self.send_header('Content-length',len(stream.getvalue()))
					self.end_headers()
					self.wfile.write(stream.getvalue())
					stream.seek(0)
					stream.truncate()
					time.sleep(.1)
			except KeyboardInterrupt:
				pass 
			return
		
			
		else:
			# If it is not mjpg stream evaluate try to read a page: 
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			try:
				if self.path in rewrite:
					htmlPage = open(curdir + sep + rewrite[self.path])
					self.wfile.write(htmlPage.read())
				else:
					errorPage = open(curdir + sep + '404.html')
					self.wfile.write(errorPage.read())
			except KeyboardInterrupt:
				pass 
			return
		  
		  
	def do_POST(self):
	# When a POST solicitude comes into the server, then execute this:
		logging.warning("======= POST STARTED =======")
		logging.warning(self.headers)
		form = cgi.FieldStorage(
			fp=self.rfile,
			headers=self.headers,
			environ={'REQUEST_METHOD':'POST',
					 'CONTENT_TYPE':self.headers['Content-Type'],
					 })
		logging.warning("======= POST VALUES =======")
		
		for item in form.list:
			logging.warning(item)
		logging.warning("\n")
		
		camera.led = '1' in form.getlist("led")
		
		SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
					

def main():
  # created a *threaded *video stream, allow the camera sensor to warmup,
  # and start the FPS counter
  print("[INFO] sampling THREADED frames from `picamera` module...")
  vs = PiVideoStream().start()
  time.sleep(2.0)
  fps = FPS().start()
    
  try:
    server = SocketServer.TCPServer(('', 8900), Handler)
    print "server started"
    server.serve_forever()
  except KeyboardInterrupt:
    fps.stop()
    #cv2.destroyAllWindows()
    vs.stop()
 
if __name__ == '__main__':
  main()