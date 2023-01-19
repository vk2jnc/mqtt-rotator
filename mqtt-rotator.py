import time
import paho.mqtt.client as mqtt
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

# Set up MQTT client and connect to broker
client = mqtt.Client()
client.connect("docker.hogwarts.local", 1883, 60)

##Setup Motorkit
kit = MotorKit() # instantiate the motor kit
dt = 0.001 # delay time
steps_to_degrees_az = 1.0/30 # conversion ratio from steps to magnetic degrees for azimuth
steps_to_degrees_el = 1.0/30 # conversion ratio from steps to magnetic degrees for elevation
current_angle_az = 0 # initial angle of azimuth is set to 0
current_angle_el = 0 # initial angle of elevation is set to 0

print("MotorKit Example")

def on_message(client, userdata, msg):
    global current_angle_az, current_angle_el
    try:
        target_angle_az, target_angle_el = map(float, msg.payload.split())
    except ValueError:
        print("Invalid angle value received")
        return
    if target_angle_az < 0 or target_angle_az > 360 or target_angle_el < 0 or target_angle_el > 180:
        print("Invalid angle value received, angle should be between 0 and 360 for azimuth and 0 and 180 for elevation")
        returnsteps_az = int((target_angle_az - current_angle_az) / steps_to_degrees_az)
    steps_el = int((target_angle_el - current_angle_el) / steps_to_degrees_el)
    steps_az = int((target_angle_az - current_angle_az) / steps_to_degrees_az)
    if steps_az > 0:
        print(f"Moving to {target_angle_az} degrees azimuth, clockwise")
        for i in range(steps_az):
            time.sleep(dt)
            kit.stepper1.onestep(direction=stepper.FORWARD)
            current_angle_az += steps_to_degrees_az # increment angle by the conversion ratio
    elif steps_az < 0:
        print(f"Moving to {target_angle_az} degrees azimuth, counter-clockwise")
        for i in range(abs(steps_az)):
            time.sleep(dt)
            kit.stepper1.onestep(direction=stepper.BACKWARD)
            current_angle_az -= steps_to_degrees_az # decrement angle by the conversion ratio
    else:
        print("Already at target azimuth angle")

    if steps_el > 0:
        print(f"Moving to {target_angle_el} degrees elevation, clockwise")
        for i in range(steps_el):
            time.sleep(dt)
            kit.stepper2.onestep(direction=stepper.FORWARD)
            current_angle_el += steps_to_degrees_el # increment angle by the conversion ratio
    elif steps_el < 0:
        print(f"Moving to {target_angle_el} degrees elevation, counter-clockwise")
        for i in range(abs(steps_el)):
            time.sleep(dt)
            kit.stepper2.onestep(direction=stepper.BACKWARD)
            current_angle_el -= steps_to_degrees_el # decrement angle by the conversion ratio
    else:
        print("Already at target elevation angle")

client.on_message = on_message
client.subscribe("rotator")

while True:
    client.loop()
