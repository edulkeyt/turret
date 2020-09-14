from __future__ import print_function
from SimpleHTTPServer import SimpleHTTPRequestHandler
import socket
from SocketServer import TCPServer
import io
import time
import picamera
import cgi
from os import curdir, sep
import logging
#from imutils.video.pivideostream import PiVideoStream
#from JpgVideoStream import JpgVideoStream
from picamera.array import PiRGBArray
#from picamera import PiCamera
#import argparse
import imutils
from imutils.video import FPS
from imutils.video.pivideostream import PiVideoStream
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

#super() argument 1 must be type, not classobj
       
class _TCPServer(TCPServer):
  """def __init__(self, arg1, arg2):
    self.disable_nagle_algorithm=True
    TCPServer.__init__(self, arg1, arg2)
    #print(self.disable_nagle_algorithm)
    self.disable_nagle_algorithm=True
""
  def server_bind(self):
    print("bind")
    self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    TCPServer.server_bind(self)
""" 
  
# Server Handler is defined as a Class.    
class CamHandler(SimpleHTTPRequestHandler):

  #wbufsize = -1
  #disable_nagle_algorithm = True
  #timeout=0.05;
  
  """def __init__(self, arg1, arg2, arg3):    
    SimpleHTTPRequestHandler.__init__(self, arg1, arg2, arg3)
    self.disable_nagle_algorithm=True
    self.timeout = 0
"""
    
  def do_GET(self):
    _startTime = datetime.datetime.now()
    # When a GET solicitude comes into the server, then execute this:
    if self.path.endswith('.mjpg'):
      # If mjpg stream is required, take image and send it. 
      self.send_response(200)
      self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
      self.end_headers()
      #stream=io.BytesIO()
      try:
        while True:
          _startTime = datetime.datetime.now()
          frame = vs.read()
          #print(1/(datetime.datetime.now() - _startTime).total_seconds(), end=' ')
          #frame = imutils.resize(frame, width=640, height=480)
          ret, jpg = cv2.imencode('.jpg', frame)
          #print(1/(datetime.datetime.now() - _startTime).total_seconds(), end=' ')
          stream = jpg.tobytes()
          #print(len(stream))
         

          self.wfile.write("--jpgboundary")
          self.send_header('Content-type','image/jpg')
          self.send_header('Content-length',len(stream))
          self.end_headers()
          self.wfile.write(stream)
          #print((datetime.datetime.now() - _startTime).total_seconds())
          #print(1/(datetime.datetime.now() - _startTime).total_seconds())
          #_startTime = datetime.datetime.now()
          #stream.seek(0)
          #stream.truncate()
          #time.sleep(.1)
          #print(1/(datetime.datetime.now() - _startTime).total_seconds())
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
  vs = PiVideoStream(resolution=(640, 480), framerate=60).start()
  time.sleep(2.0)
  Handler = CamHandler
    
  try:
    server = _TCPServer(('', 8900), Handler)    
    #server.disable_nagle_algorithm=True
    print("server started")
    server.serve_forever()
  except KeyboardInterrupt:
    server.socket.close()
    fps.stop()    
    vs.stop()
 
if __name__ == '__main__':
  main()
