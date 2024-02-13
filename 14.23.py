from gpiozero import DistanceSensor
from time import sleep
import VL53L1X

# Initialize VL53L1X sensor
tof = VL53L1X.VL53L1X()
tof.start_ranging(VL53L1X.VL53L1X_LONG_RANGE_MODE)

# Initialize GPIO DistanceSensor
sensor = DistanceSensor(echo=18, trigger=17)

try:
    while True:
        # Read distance from HC-SR04
        cm_sr04 = sensor.distance * 100
        inch_sr04 = cm_sr04 / 2.54

        # Read distance from VL53L1X
        distance_vl53l1x = tof.get_distance()

        # Display readings
        print("HC-SR04: {:.0f} cm, {:.0f} inches | VL53L1X: {} mm".format(cm_sr04, inch_sr04, distance_vl53l1x))

        sleep(0.5)

except KeyboardInterrupt:
    pass

finally:
    # Stop VL53L1X ranging
    tof.stop_ranging()
