from __future__ import print_function
import SimpleHTTPServer
import SocketServer
import io
import time
import picamera
import cgi
from os import curdir, sep
import logging
#from imutils.video.pivideostream import PiVideoStream
from JpgVideoStream import JpgVideoStream
from imutils.video import FPS
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import imutils
import time
import cv2
from threading import Lock
import datetime
 
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
    _startTime = datetime.datetime.now()
    # When a GET solicitude comes into the server, then execute this:
    if self.path.endswith('.mjpg'):
      # If mjpg stream is required, take image and send it. 
      self.send_response(200)
      self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
      self.end_headers()
      stream=io.BytesIO()
      try:
        while True:
          # Taking images from Raspberry pi camera:
          start=time.time()
          # grab the frame from the threaded video stream and resize it
          # to have a maximum width of 400 pixels
          frame = vs.read()
          #frame = imutils.resize(frame, width=400)

          #stream.write(bytearray(frame))
          #stream.write(bytearray(frame.shape))
          #stream.write(frame.shape)
          #lock.acquire()
          resultFrame = frame.getvalue()
          #lock.release()
          #stream = frame
          
          #fps.update()
          #fps.stop()
          #print(fps.fps())
          #fps.start()
          # for foo in camera.capture_continuous(stream,'jpeg'):
          self.wfile.write("--jpgboundary")
          self.send_header('Content-type','image/jpg')
          self.send_header('Content-length',len(resultFrame))
          self.end_headers()
          self.wfile.write(resultFrame)
          print(1/(datetime.datetime.now() - _startTime).total_seconds())
          _startTime = datetime.datetime.now()
          stream.seek(0)
          stream.truncate()
          time.sleep(.1)
      except KeyboardInterrupt:
        pass 
      return
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
  global vs
  vs = JpgVideoStream().start()
  time.sleep(2.0)
  #global fps
  #fps = FPS().start()
  Handler = CamHandler
  global lock
  lock = Lock();
    
  try:
    server = SocketServer.TCPServer(('', 8900), Handler)
    print("server started")
    server.serve_forever()
  except KeyboardInterrupt:
    server.socket.close()
    fps.stop()
    #cv2.destroyAllWindows()
    vs.stop()
 
if __name__ == '__main__':
  main()
