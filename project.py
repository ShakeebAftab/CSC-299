import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

TRIG_PIN = 23
ECHO_PIN = 24
PIN_17 = 17
PIN_18 = 18
PIN_27 = 27

GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.setup(PIN_17, GPIO.OUT)
GPIO.setup(PIN_18, GPIO.OUT)
GPIO.setup(PIN_27, GPIO.OUT)

def measure_distance():
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    while GPIO.input(ECHO_PIN) == 0:
        pulse_start_time = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time
    distance = pulse_duration * 17150
    return round(distance, 2)

try:
    while True:
        distance = measure_distance()
        print("Distance: ", distance)
        motion_threshold = 30

        if distance < motion_threshold:
            GPIO.output(PIN_17, not GPIO.input(PIN_17))
            GPIO.output(PIN_18, not GPIO.input(PIN_18))
            GPIO.output(PIN_27, not GPIO.input(PIN_27))

        time.sleep(1) 

except KeyboardInterrupt:
    print("Exiting...")

finally:
    GPIO.cleanup()
