from picamera import PiCamera
from gpiozero import MotionSensor
import time

camera = PiCamera()
camera.resolution = (1024, 768)

pir_sensor = MotionSensor(18)

def capture_image():
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    image_filename = f"motion_capture_{timestamp}.jpg"
    camera.capture(image_filename)
    print(f"Image captured: {image_filename}")

try:
    while True:
        pir_sensor.wait_for_motion()
        print("Motion detected!")
        capture_image()
        time.sleep(5)

except KeyboardInterrupt:
    print("Exiting program.")
finally:
    camera.close()
    pir_sensor.close()
