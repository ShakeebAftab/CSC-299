import RPi.GPIO as GPIO
import time
import VL53L1X

TRIG_PIN = 17
ECHO_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

tof = VL53L1X.VL53L1X()
tof.start_ranging(VL53L1X.VL53L1X_LONG_RANGE_MODE)

try:
    while True:
        # Read distance from HC-SR04
        GPIO.output(TRIG_PIN, GPIO.LOW)
        time.sleep(0.2)  # Allow sensor to settle
        GPIO.output(TRIG_PIN, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(TRIG_PIN, GPIO.LOW)
        while GPIO.input(ECHO_PIN) == 0:
            pulse_start = time.time()
        while GPIO.input(ECHO_PIN) == 1:
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        distance_sr04 = pulse_duration * 17150
        distance_vl53l1x = tof.get_distance()
        print(f"HC-SR04 Distance: {distance_sr04:.2f} cm, VL53L1X Distance: {distance_vl53l1x} mm")
        time.sleep(1)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
    tof.stop_ranging()
