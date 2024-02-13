from gpiozero import DistanceSensor
from time import sleep
from guizero import App, Text

sensor = DistanceSensor(echo=18, trigger=17)

def update_reading():
    cm = sensor.distance * 100
    reading_text.value = str(cm)

app = App(width=500, height=100)
reading_text = Text(app, size=20)
reading_text.repeat(1000, update_reading)
app.display()
