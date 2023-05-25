#!/usr/bin/python3

from w1thermsensor import W1ThermSensor, Sensor
import paho.mqtt.client as mqtt
import sys
import time
import yaml
import json
import uuid
import RPi.GPIO as GPIO

Release_date = "2023-05-30"

#  Get the parameter file
with open("/opt/ThermoPI-Cottage/MYsecrets.yaml", "r") as ymlfile:
    MYs = yaml.safe_load(ymlfile)

LOOP = MYs["MAIN"]["LOOP"]
HOST = MYs["MAIN"]["HOST"]
PORT = MYs["MAIN"]["PORT"]
USER = MYs["MAIN"]["USER"]
AREA = MYs["MAIN"]["AREA"]
PWD = MYs["MAIN"]["PWD"]
STETOPIC = MYs["MAIN"]["STETOPIC"]

# GPIO Setup
SERVOGPIO = int(MYs["WHCONTROL"]["SERVOGPIO"])
TSTATGPIO = int(MYs["BINARY_SENSOR"]["TSTATGPIO"])
PULSEFREQUENCY = float(MYs["WHCONTROL"]["PULSEFREQUENCY"])
TRANGEMIN = float(MYs["WHCONTROL"]["TRANGEMIN"])
TRANGEMAX = float(MYs["WHCONTROL"]["TRANGEMAX"])
DIRECTION = MYs["WHCONTROL"]["DIRECTION"]
SERVOANGLE = float(MYs["WHCONTROL"]["SERVOANGLE"])
PWM0 = float(MYs["WHCONTROL"]["PWM0"])
GPIO_ON = GPIO.HIGH
GPIO_OFF = GPIO.LOW
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVOGPIO, GPIO.OUT)
GPIO.setup(TSTATGPIO, GPIO.IN)
srvo = GPIO.PWM(SERVOGPIO,PULSEFREQUENCY)
srvo.start(0)

# Pulling the unique MAC SN section address using uuid and getnode() function 
DEVICE_ID = (hex(uuid.getnode())[-6:]).upper()

TOPIC = "homeassistant/sensor/"
TOPICBS = "homeassistant/binary_sensor/"

NAMED = MYs["MAIN"]["DEVICE_NAME"]
D_ID = DEVICE_ID + '_' + NAMED
LWT = STETOPIC + D_ID + '/lwt'

ADDR_W101 = MYs["W1"]["ADDR_W101"]
NAME_W101 = MYs["W1"]["NAME_W101"]
W101_ID =  DEVICE_ID + '_' + MYs["W1"]["W101_ID"]
CONFIG_W101 = TOPIC + W101_ID + '/config'
W101_STATE = STETOPIC + W101_ID

ADDR_W102 = MYs["W1"]["ADDR_W102"]
NAME_W102 = MYs["W1"]["NAME_W102"]
W102_ID =  DEVICE_ID + '_' + MYs["W1"]["W102_ID"]
CONFIG_W102 = TOPIC + W102_ID + '/config'
W102_STATE = STETOPIC + W102_ID

ADDR_W103 = MYs["W1"]["ADDR_W103"]
NAME_W103 = MYs["W1"]["NAME_W103"]
W103_ID =  DEVICE_ID + '_' + MYs["W1"]["W103_ID"]
CONFIG_W103 = TOPIC + W103_ID + '/config'
W103_STATE = STETOPIC + W103_ID

ADDR_W104 = MYs["W1"]["ADDR_W104"]
NAME_W104 = MYs["W1"]["NAME_W104"]
W104_ID =  DEVICE_ID + '_' + MYs["W1"]["W104_ID"]
CONFIG_W104 = TOPIC + W104_ID + '/config'
W104_STATE = STETOPIC + W104_ID

ADDR_W105 = MYs["W1"]["ADDR_W105"]
NAME_W105 = MYs["W1"]["NAME_W105"]
W105_ID =  DEVICE_ID + '_' + MYs["W1"]["W105_ID"]
CONFIG_W105 = TOPIC + W105_ID + '/config'
W105_STATE = STETOPIC + W105_ID

ADDR_W106 = MYs["W1"]["ADDR_W106"]
NAME_W106 = MYs["W1"]["NAME_W106"]
W106_ID =  DEVICE_ID + '_' + MYs["W1"]["W106_ID"]
CONFIG_W106 = TOPIC + W106_ID + '/config'
W106_STATE = STETOPIC + W106_ID

ADDR_W107 = MYs["W1"]["ADDR_W107"]
NAME_W107 = MYs["W1"]["NAME_W107"]
W107_ID =  DEVICE_ID + '_' + MYs["W1"]["W107_ID"]
CONFIG_W107 = TOPIC + W107_ID + '/config'
W107_STATE = STETOPIC + W107_ID

ADDR_W108 = MYs["W1"]["ADDR_W108"]
NAME_W108 = MYs["W1"]["NAME_W108"]
W108_ID =  DEVICE_ID + '_' + MYs["W1"]["W108_ID"]
CONFIG_W108 = TOPIC + W108_ID + '/config'
W108_STATE = STETOPIC + W108_ID

ADDR_W109 = MYs["W1"]["ADDR_W109"]
NAME_W109 = MYs["W1"]["NAME_W109"]
W109_ID =  DEVICE_ID + '_' + MYs["W1"]["W109_ID"]
CONFIG_W109 = TOPIC + W109_ID + '/config'
W109_STATE = STETOPIC + W109_ID

ADDR_W110 = MYs["W1"]["ADDR_W110"]
NAME_W110 = MYs["W1"]["NAME_W110"]
W110_ID =  DEVICE_ID + '_' + MYs["W1"]["W110_ID"]
CONFIG_W110 = TOPIC + W110_ID + '/config'
W110_STATE = STETOPIC + W110_ID

NAMETstat = MYs["BINARY_SENSOR"]["NAMETstat"]
Tstat_ID = DEVICE_ID + '_' + MYs["BINARY_SENSOR"]["Tstat_ID"]
CONFIGTstat = TOPICBS + Tstat_ID + '/config'
STATEBS = STETOPIC + Tstat_ID

# These are the s/n's used for the temp sensors.
list = [999, ADDR_W101, ADDR_W102, ADDR_W103, ADDR_W104, ADDR_W105, ADDR_W106, ADDR_W107, ADDR_W108, ADDR_W109, ADDR_W110, 999, 999 ]

# These are the STATE Topics
state_topic = ["", W101_STATE, W102_STATE, W103_STATE, W104_STATE, W105_STATE, W106_STATE, W107_STATE, W108_STATE, W109_STATE, W110_STATE, "", "" ]

# Device Parameters for MQTT Discovery
pl_avail = "Online"
pl_not_avail = "Offline"
name = "ThermoPI Cottage"
mf = "SirGoodenough"
mdl = "HomeAssistant Discovery for ThermoPI Cottage"
sw = Release_date
hw = "https://github.com/SirGoodenough/ThermoPI-Cottage"
cu = "https://github.com/SirGoodenough/ThermoPI-Cottage/blob/master/README.md"
unit_of_meas = "°F"
dev_cla = "temperature"

payload_W101config = {
    "name": NAME_W101,
    "stat_t": W101_STATE,
    "avty_t": LWT,
    "pl_avail": pl_avail,
    "pl_not_avail": pl_not_avail,
    "uniq_id": W101_ID,
    "dev": {
        "ids": [
        D_ID,
        DEVICE_ID
        ],
        "name": name,
        'sa': AREA,
        "mf": mf,
        "mdl": mdl,
        "sw": sw,
        "hw": hw,
        "cu": cu
    },
    "unit_of_meas": unit_of_meas,
    "dev_cla": dev_cla,
    "frc_upd": True,
    'exp_aft': 400,
    "val_tpl": "{{ value_json.temperature }}"
}

payload_W102config = {
    "name": NAME_W102,
    "stat_t": W102_STATE,
    "avty_t": LWT,
    "pl_avail": pl_avail,
    "pl_not_avail": pl_not_avail,
    "uniq_id": W102_ID,
    "dev": {
        "ids": [
        D_ID,
        DEVICE_ID
        ],
        "name": name,
        'sa': AREA,
        "mf": mf,
        "mdl": mdl,
        "sw": sw,
        "hw": hw,
        "cu": cu
    },
    "unit_of_meas": unit_of_meas,
    "dev_cla": dev_cla,
    "frc_upd": True,
    'exp_aft': 400,
    "val_tpl": "{{ value_json.temperature }}"
}

payload_W103config = {
    "name": NAME_W103,
    "stat_t": W103_STATE,
    "avty_t": LWT,
    "pl_avail": pl_avail,
    "pl_not_avail": pl_not_avail,
    "uniq_id": W103_ID,
    "dev": {
        "ids": [
        D_ID,
        DEVICE_ID
        ],
        "name": name,
        'sa': AREA,
        "mf": mf,
        "mdl": mdl,
        "sw": sw,
        "hw": hw,
        "cu": cu
    },
    "unit_of_meas": unit_of_meas,
    "dev_cla": dev_cla,
    "frc_upd": True,
    'exp_aft': 400,
    "val_tpl": "{{ value_json.temperature }}"
}

payload_W104config = {
    "name": NAME_W104,
    "stat_t": W104_STATE,
    "avty_t": LWT,
    "pl_avail": pl_avail,
    "pl_not_avail": pl_not_avail,
    "uniq_id": W104_ID,
    "dev": {
        "ids": [
        D_ID,
        DEVICE_ID
        ],
        "name": name,
        'sa': AREA,
        "mf": mf,
        "mdl": mdl,
        "sw": sw,
        "hw": hw,
        "cu": cu
    },
    "unit_of_meas": unit_of_meas,
    "dev_cla": dev_cla,
    "frc_upd": True,
    'exp_aft': 400,
    "val_tpl": "{{ value_json.temperature }}"
}

payload_W105config = {
    "name": NAME_W105,
    "stat_t": W105_STATE,
    "avty_t": LWT,
    "pl_avail": pl_avail,
    "pl_not_avail": pl_not_avail,
    "uniq_id": W105_ID,
    "dev": {
        "ids": [
        D_ID,
        DEVICE_ID
        ],
        "name": name,
        'sa': AREA,
        "mf": mf,
        "mdl": mdl,
        "sw": sw,
        "hw": hw,
        "cu": cu
    },
    "unit_of_meas": unit_of_meas,
    "dev_cla": dev_cla,
    "frc_upd": True,
    'exp_aft': 400,
    "val_tpl": "{{ value_json.temperature }}"
}

payload_W106config = {
    "name": NAME_W106,
    "stat_t": W106_STATE,
    "avty_t": LWT,
    "pl_avail": pl_avail,
    "pl_not_avail": pl_not_avail,
    "uniq_id": W106_ID,
    "dev": {
        "ids": [
        D_ID,
        DEVICE_ID
        ],
        "name": name,
        'sa': AREA,
        "mf": mf,
        "mdl": mdl,
        "sw": sw,
        "hw": hw,
        "cu": cu
    },
    "unit_of_meas": unit_of_meas,
    "dev_cla": dev_cla,
    "frc_upd": True,
    'exp_aft': 400,
    "val_tpl": "{{ value_json.temperature }}"
}

payload_W107config = {
    "name": NAME_W107,
    "stat_t": W107_STATE,
    "avty_t": LWT,
    "pl_avail": pl_avail,
    "pl_not_avail": pl_not_avail,
    "uniq_id": W107_ID,
    "dev": {
        "ids": [
        D_ID,
        DEVICE_ID
        ],
        "name": name,
        'sa': AREA,
        "mf": mf,
        "mdl": mdl,
        "sw": sw,
        "hw": hw,
        "cu": cu
    },
    "unit_of_meas": unit_of_meas,
    "dev_cla": dev_cla,
    "frc_upd": True,
    'exp_aft': 400,
    "val_tpl": "{{ value_json.temperature }}"
}

payload_W108config = {
    "name": NAME_W108,
    "stat_t": W108_STATE,
    "avty_t": LWT,
    "pl_avail": pl_avail,
    "pl_not_avail": pl_not_avail,
    "uniq_id": W108_ID,
    "dev": {
        "ids": [
        D_ID,
        DEVICE_ID
        ],
        "name": name,
        'sa': AREA,
        "mf": mf,
        "mdl": mdl,
        "sw": sw,
        "hw": hw,
        "cu": cu
    },
    "unit_of_meas": unit_of_meas,
    "dev_cla": dev_cla,
    "frc_upd": True,
    'exp_aft': 400,
    "val_tpl": "{{ value_json.temperature }}"
}

payload_W109config = {
    "name": NAME_W109,
    "stat_t": W109_STATE,
    "avty_t": LWT,
    "pl_avail": pl_avail,
    "pl_not_avail": pl_not_avail,
    "uniq_id": W109_ID,
    "dev": {
        "ids": [
        D_ID,
        DEVICE_ID
        ],
        "name": name,
        'sa': AREA,
        "mf": mf,
        "mdl": mdl,
        "sw": sw,
        "hw": hw,
        "cu": cu
    },
    "unit_of_meas": unit_of_meas,
    "dev_cla": dev_cla,
    "frc_upd": True,
    'exp_aft': 400,
    "val_tpl": "{{ value_json.temperature }}"
}

payload_W110config = {
    "name": NAME_W110,
    "stat_t": W110_STATE,
    "avty_t": LWT,
    "pl_avail": pl_avail,
    "pl_not_avail": pl_not_avail,
    "uniq_id": W110_ID,
    "dev": {
        "ids": [
        D_ID,
        DEVICE_ID
        ],
        "name": name,
        'sa': AREA,
        "mf": mf,
        "mdl": mdl,
        "sw": sw,
        "hw": hw,
        "cu": cu
    },
    "unit_of_meas": unit_of_meas,
    "dev_cla": dev_cla,
    "frc_upd": True,
    'exp_aft': 400,
    "val_tpl": "{{ value_json.temperature }}"
}

payloadTstatconfig1 = {
    "name": NAMETstat1,
    "stat_t": STATEBS1,
    "avty_t": LWT,
    "pl_avail": "Online",
    "pl_not_avail": "Offline",
    "uniq_id": Tstat1_ID,
    "dev": {
        "ids": [
        D_ID,
        DEVICE_ID
        ],
        "name": "ThermoPI",
        'sa': AREA,
        "mf": "SirGoodenough",
        "mdl": "HomeAssistant Discovery for ThermoPI",
        "sw": "https://github.com/SirGoodenough/ThermoPI"
    },
    "frc_upd": True,
    "dev_cla":"heat"
}

payloadTstatconfig2 = {
    "name": NAMETstat2,
    "stat_t": STATEBS2,
    "avty_t": LWT,
    "pl_avail": "Online",
    "pl_not_avail": "Offline",
    "uniq_id": Tstat2_ID,
    "dev": {
        "ids": [
        D_ID,
        DEVICE_ID
        ],
        "name": "ThermoPI",
        'sa': AREA,
        "mf": "SirGoodenough",
        "mdl": "HomeAssistant Discovery for ThermoPI",
        "sw": "https://github.com/SirGoodenough/ThermoPI"
    },
    "frc_upd": True,
    "dev_cla":"heat"
}


# Subroutine look up 1 Wire temp(s)
def W1():
    global temp
    global sensor
    global list
    global count
    temp = 0.0
    sensorSN = str(list[count])

    sensor = W1ThermSensor(sensor_type=Sensor.DS18B20, sensor_id=sensorSN)
    # Get the temp
    tempC = sensor.get_temperature()
    # Test the result.  Make sure it is reasonable and not a glitch.
    if tempC is None or tempC > 150.0 or tempC < 1.0:
        return
    # Conversion to F & round to .1
    tF = round((9.0/5.0 * tempC + 32.0), 2)
    # Use while Troubleshooting...
    # print("{:.1f}".format(tF))
    # Done
    temp = tF

# Subroutine to send results to MQTT
def mqttSend():
    global temp
    global mqttc
    global count
    global state_topic
    global TSTATGPIO
    global TStatState
    global STATEBS

    if GPIO.input(TSTATGPIO):
        TStatState = "ON"
    else:
        TStatState = "OFF"

    if temp == 0.0:
        return

    try:

        payloadOut = {
            "temperature": temp}
        OutState = state_topic[count]
        print(f"Updating {OutState} {json.dumps(payloadOut)}")
        (result1,mid) = mqttc.publish(OutState, json.dumps(payloadOut), 1, True)

        currentdate = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"Date Time:   {currentdate}")
        print(f"MQTT Update 1 result {result1}")

        if result1 != 0:
            raise ValueError('Result message from MQTT was not 0')


        print(f"Updating {STATEBS1} {TStatState1}")
        (result2,mid) = mqttc.publish(STATEBS1, TStatState1, 1, True)

        print(f"MQTT Update 2 result {result2}")

        if result2 != 0:
            raise ValueError('Result message2 from MQTT was not 0')


        print(f"Updating {STATEBS2} {TStatState2}")
        (result3,mid) = mqttc.publish(STATEBS2, TStatState2, 1, True)

        print(f"MQTT Update 3 result {result3}")

        if result3 != 0:
            raise ValueError('Result message3 from MQTT was not 0')

    except Exception as e:
        # Error appending data, most likely because credentials are stale.
        #  disconnect and re-connect...
        print('MQTT error, trying re-connect: ' + str(e))
        mqttc.publish(LWT, 'Offline', 0, True)
        time.sleep(2)
        mqttc.loop_stop()
        mqttc.disconnect()
        time.sleep(1)
        mqttConnect()
        pass

def mqttConnect():
    mqttc.on_connect = on2connect
    mqttc.on_message = on2message
    mqttc.connect(HOST, PORT, 60)
    mqttc.loop_start()
    mqttc.publish(LWT, "Online", 1, True)
    mqttc.publish(CONFIG_W101, json.dumps(payload_W101config), 1, True)
    mqttc.publish(CONFIG_W102, json.dumps(payload_W102config), 1, True)
    mqttc.publish(CONFIG_W103, json.dumps(payload_W103config), 1, True)
    mqttc.publish(CONFIG_W104, json.dumps(payload_W104config), 1, True)
    mqttc.publish(CONFIG_W105, json.dumps(payload_W105config), 1, True)
    mqttc.publish(CONFIG_W106, json.dumps(payload_W106config), 1, True)
    mqttc.publish(CONFIG_W107, json.dumps(payload_W107config), 1, True)
    mqttc.publish(CONFIG_W108, json.dumps(payload_W108config), 1, True)
    mqttc.publish(CONFIG_W109, json.dumps(payload_W109config), 1, True)
    mqttc.publish(CONFIG_W110, json.dumps(payload_W110config), 1, True)
    mqttc.publish(CONFIGTstat1, json.dumps(payloadTstatconfig1), 1, True)
    mqttc.publish(CONFIGTstat2, json.dumps(payloadTstatconfig2), 1, True)

def on2connect(mqttc, userdata, flags, rc):
    if rc==0:
        print(f"Connecting to MQTT on {HOST} {PORT} with result code {str(rc)}.")
        mqttc.subscribe((WHTOPIC,0))
        # mqttc.subscribe("$SYS/#")
    else:
        print(f"Bad connection Returned code= {str(rc)}.")

def on2message(mqttc, userdata, msg):
    # The callback for when a PUBLISH message is received from the server.

    tRange = TRANGEMAX - TRANGEMIN    # Number of degrees in range
    try:                # MUST BE AN INTEGER
        whTSet = int(msg.payload)
    except ValueError:  # Set to mid-Range rather than error if not integer
        whTSet = int(round((tRange/2) + TRANGEMIN,0))
        print (f"WARNING!! Value set to mid-range because not an integer.")

    Topic = msg.topic

    print (f"Message: {str(whTSet)} from Topic: {Topic}")

    # Handle Message
    if ( Topic == WHTOPIC and
        int(whTSet) <= TRANGEMAX and
        int(whTSet) >= TRANGEMIN
        ):
        # Scale the Temperature range to the angle
        tScaled = whTSet - TRANGEMIN    # Temp degrees from start point
        whASet = tScaled * (SERVOANGLE/tRange) # Scaled angle
        SetAngle(whASet)

def SetAngle(angle):
    if DIRECTION != "CW":   # Reverse the direction if needed
        angle = SERVOANGLE - angle

    duty = angle / (SERVOANGLE/10) + PWM0

    GPIO.output(SERVOGPIO, GPIO_ON)
    srvo.ChangeDutyCycle(duty)
    time.sleep(2)
    GPIO.output(SERVOGPIO, GPIO_OFF)
    srvo.ChangeDutyCycle(0)
    print (f"Set angle: {angle} duty: {duty}")
#Log Message to start
print(f"Logging {D_ID} sensor measurements every {LOOP} seconds.")
print(f"Press Ctrl-C to quit.")
mqttc = mqtt.Client(D_ID, 'False', 'MQTTv311')
mqttc.disable_logger()  # Saves wear on SD card Memory.  Remove as needed for troubleshooting
mqttc.username_pw_set(USER, PWD) # deactivate if not needed
mqttConnect()

try:
    count = 0
    while count < 11:
        if count > 9:  # Reset the loop
            count = 0
        count += 1
        # print('Updating loop %s.' % count)
        # Use while Troubleshooting...
        # print('Temperature %s.' % temp)
        # Done
        temp = 0.0
        W1()
        mqttSend()
        for i in range(LOOP):
            time.sleep(1)

except KeyboardInterrupt:
    print(' Keyboard Interrupt. Closing MQTT.')
    mqttc.publish(LWT, 'Offline', 1, True)
    time.sleep(1)
    mqttc.loop_stop()
    mqttc.disconnect()
    GPIO.cleanup()
    sys.exit()
