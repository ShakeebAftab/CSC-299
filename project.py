import RPi.GPIO as GPIO
import time
import threading
from twilio.rest import Client

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

def send_whatsapp_message(message):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
                              body=message,
                              from_=twilio_phone_number,
                              to='whatsapp:+your_phone_number'
                          )

def process_whatsapp_messages():
    while True:
        messages = client.messages.list(to=twilio_phone_number)

        for message in messages:
            if message.direction == 'inbound':
                process_command(message.body)
                message.delete()

        time.sleep(1)

def process_command(command):
    if command.lower() == 'on':
        # Toggle the relay ON
        GPIO.output(PIN_17, GPIO.HIGH)
        GPIO.output(PIN_18, GPIO.HIGH)
        GPIO.output(PIN_27, GPIO.HIGH)
    elif command.lower() == 'off':
        # Toggle the relay OFF
        GPIO.output(PIN_17, GPIO.LOW)
        GPIO.output(PIN_18, GPIO.LOW)
        GPIO.output(PIN_27, GPIO.LOW)

try:
    # Twilio Credentials
    account_sid = 'your_account_sid'
    auth_token = 'your_auth_token'
    twilio_phone_number = 'whatsapp:your_twilio_whatsapp_number'

    # Start a separate thread for processing WhatsApp messages
    process_thread = threading.Thread(target=process_whatsapp_messages)
    process_thread.start()

    while True:
        distance = measure_distance()
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
