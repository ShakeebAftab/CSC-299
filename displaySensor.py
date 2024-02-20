import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
from time import sleep
from gpiozero import DistanceSensor

i2c = board.I2C()
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
small_font = ImageFont.truetype('FreeSans.ttf', 12)
disp.fill(0)
disp.show()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)

def display_sensor_reading(sensor_reading):
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    draw.text((0, 0), sensor_reading, font=small_font, fill=255)
    disp.image(image)
    disp.show()

sensor = DistanceSensor(echo=18, trigger=17)

while True:
    cm = sensor.distance * 100
    inch = cm / 2.5
    sensor_reading = "Distance: {:.0f} cm / {:.0f} inches".format(cm, inch)

    display_sensor_reading(sensor_reading)
    sleep(0.1)
