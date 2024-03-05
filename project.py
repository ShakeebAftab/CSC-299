import time
from gpiozero import MotionSensor, OutputDevice
from twilio.rest import Client

TWILIO_ACCOUNT_SID = ""
TWILIO_AUTH_TOKEN = ""
TWILIO_WHATSAPP_NUMBER = ""

RELAY_PIN_1 = 17
RELAY_PIN_2 = 18
RELAY_PIN_3 = 27
ULTRASONIC_TRIGGER_PIN = 23
ULTRASONIC_ECHO_PIN = 24

def turn_on_relays():
    relay1.on()
    relay2.on()
    relay3.on()
    print("Relays turned ON")

def turn_off_relays():
    relay1.off()
    relay2.off()
    relay3.off()
    print("Relays turned OFF")

ultrasonic_sensor = MotionSensor(ULTRASONIC_TRIGGER_PIN, ULTRASONIC_ECHO_PIN)
relay1 = OutputDevice(RELAY_PIN_1)
relay2 = OutputDevice(RELAY_PIN_2)
relay3 = OutputDevice(RELAY_PIN_3)

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def handle_whatsapp_message(message):
    if "on" in message.lower():
        turn_on_relays()
    elif "off" in message.lower():
        turn_off_relays()

try:
    while True:
        if ultrasonic_sensor.motion_detected:
            turn_on_relays()
            time.sleep(10)

        messages = client.messages.list(to=TWILIO_WHATSAPP_NUMBER)
        for message in messages:
            handle_whatsapp_message(message.body)
            message.delete() 

        time.sleep(1)

except KeyboardInterrupt:
    print("Program terminated by user")
    turn_off_relays()
