import io
import socket
import struct
import time
import picamera

client_socket = socket.socket()
client_socket.connect(('0.0.0.0', 1905))  # IP of server here

connection = client_socket.makefile('wb')
try:
    camera = picamera.PiCamera()
    camera.vflip = True
    camera.hflip = True
    camera.resolution = (640, 480)
    camera.framerate = 60

    camera.start_preview()
    #time.sleep(2)      # 2 secondswarm up for the camera

    # Note the start time and construct a stream to hold image data temporarily
    start = time.time()
    stream = io.BytesIO()
    for foo in camera.capture_continuous(stream, 'jpeg'):
        connection.write(struct.pack('<L', stream.tell()))
        connection.flush()

        stream.seek(0)
        connection.write(stream.read())

        stream.seek(0)
        stream.truncate()

    connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()
