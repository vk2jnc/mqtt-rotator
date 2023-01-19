# mqtt-rotator
An antenna rotator controlled my MQTT statements. 

The antenna rotator was 3d printed using this repository https://www.thingiverse.com/thing:4664558
I will be making some edits to the model for some extra support on the EL stepper motor - once updated will attched those files. 

Pre-reqs

Adafruit motorkit - pip3 install adafruit-circuitpython-motorkit or https://github.com/adafruit/Adafruit_CircuitPython_MotorKit
Paho Mqtt - pip3 install paho.mqtt.client
apt install mosquitto-clients - for manual publishing mqtt az el



## To Run 

python3 mqtt-rotator.py

another terminal to manally move it - mosquitto_pub -h "Mosquitto Broker" -t rotator -m "'EL' 'AZ'"

format it expects to see is el dregrees then a space then az dregrees for example "27.2 148.5"
