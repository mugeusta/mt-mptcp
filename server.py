import io
import socket
import struct
from PIL import Image
import matplotlib.pyplot as pl
from subprocess import Popen, PIPE
import datetime

server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 1905))  #change the IP and port
server_socket.listen(0)

# outputfile name initialization
startdate=datetime.datetime.now()
startdate=datetime.datetime.strftime(startdate,"%H%M%S-%d%m%Y")
videofile=startdate+".mp4"
# Writing to video file using ffmpeg.
p = Popen(['ffmpeg', '-y', '-f', 'image2pipe', '-vcodec', 'mjpeg', '-r', '8', '-i', '-', '-vcodec', 'mpeg4', '-q:v', '1', '-r', '8', videofile], stdin=PIPE)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
try:
    img = None
    while True:

        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break

        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))

        image_stream.seek(0)
        image = Image.open(image_stream)
        image.save(p.stdin, 'JPEG')
        if img is None:
            img = pl.imshow(image)
        else:
            img.set_data(image)

        pl.pause(0.01)
        pl.draw()
        print('Image size %dx%d' % image.size)
        image.verify()
        print('OK')
finally:
    connection.close()
    server_socket.close()
