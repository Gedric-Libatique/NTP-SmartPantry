import picamera
import picamera.array

with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as stream:
        camera.start_recording(stream, format='rgb')
        try:
            while True:
                camera.wait_recording()
                # Now stream.array is a numpy array containing the average
                # intensity of each pixel in the image, and stream.frame is
                # the number of frames since the start of recording
                process(stream.array)
                stream.seek(0)
                stream.truncate()
        finally:
            camera.stop_recording()
