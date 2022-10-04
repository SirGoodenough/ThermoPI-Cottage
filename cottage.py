#!/usr/bin/python3

from w1thermsensor import W1ThermSensor, Unit
import paho.mqtt.client as mqtt
import sys
import time
import yaml
import json
import uuid

# Subroutine look up 1 Wire temp(s)
def W1():
    global temp
    global sensor
    global list
    global count

    temp = 0.0
    sensor = W1ThermSensor(list[count])

    # Get the temp
    tempC = sensor.get_temperature()
    # Test the result.  Make sure it is reasonable and not a glitch.
    if tempC is None or tempC > 150.0 or tempC < 1.0:
        return
    # Conversion to F & round to .1
    tF = round((9.0/5.0 * tempC + 32.0), 1)
    # Use while Troubleshooting...
    print("{:.1f}".format(tF))
    # Done
    temp = tF
# Subroutine to send results to MQTT
def mqttSend():
    global temp
    global mqttc
    global count
    global state_topic

    if temp == 0.0:
        return

    try:

        payloadOut = {
            "temperature": temp}
        OutState = state_topic[count]
        print('Updating {0} {1}'.format(OutState,json.dumps(payloadOut) ) )
        (result1,mid) = mqttc.publish(OutState, json.dumps(payloadOut), 1, True)

        currentdate = time.strftime('%Y-%m-%d %H:%M:%S')
        print('Date Time:   {0}'.format(currentdate))
        print('MQTT Update result {0}'.format(result1))

        if result1 == 1:
            raise ValueError('Result message from MQTT was not 0')

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
    print('Connecting to MQTT on {0} {1}'.format(HOST,PORT))
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
    mqttc.publish(CONFIG_W111, json.dumps(payload_W111config), 1, True)
    mqttc.publish(CONFIG_W112, json.dumps(payload_W112config), 1, True)
    mqttc.publish(CONFIG_W113, json.dumps(payload_W113config), 1, True)
    mqttc.publish(CONFIG_W114, json.dumps(payload_W114config), 1, True)
    mqttc.publish(CONFIG_W115, json.dumps(payload_W115config), 1, True)

temp = 0.0
humidity = 0.0
# set loop counter
count = 0

#  Get the parameter file
with open("/opt/ThermoPI-Cottage/MYsecrets.yaml", "r") as ymlfile:
    MYs = yaml.safe_load(ymlfile)

LOOP = MYs["MAIN"]["LOOP"]
HOST = MYs["MAIN"]["HOST"]
PORT = MYs["MAIN"]["PORT"]
USER = MYs["MAIN"]["USER"]
PWD = MYs["MAIN"]["PWD"]
AREA = MYs["MAIN"]["AREA"]

# Pulling the unique MAC SN section address using uuid and getnode() function 
DEVICE_ID = (hex(uuid.getnode())[-6:]).upper()

TOPIC = "homeassistant/sensor/"

NAMED = MYs["MAIN"]["DEVICE_NAME"]
D_ID = DEVICE_ID + '_' + NAMED
LWT = TOPIC + D_ID + '/lwt'

ADDR_W101 = MYs["W1"]["ADDR_W101"]
NAME_W101 = MYs["W1"]["NAME_W101"]
W101_ID =  DEVICE_ID + '_' + MYs["W1"]["W101_ID"]
CONFIG_W101 = TOPIC + W101_ID + '/config'
W101_STATE = TOPIC + W101_ID + '/state'

ADDR_W102 = MYs["W1"]["ADDR_W102"]
NAME_W102 = MYs["W1"]["NAME_W102"]
W102_ID =  DEVICE_ID + '_' + MYs["W1"]["W102_ID"]
CONFIG_W102 = TOPIC + W102_ID + '/config'
W102_STATE = TOPIC + W102_ID + '/state'

ADDR_W103 = MYs["W1"]["ADDR_W103"]
NAME_W103 = MYs["W1"]["NAME_W103"]
W103_ID =  DEVICE_ID + '_' + MYs["W1"]["W103_ID"]
CONFIG_W103 = TOPIC + W103_ID + '/config'
W103_STATE = TOPIC + W103_ID + '/state'

ADDR_W104 = MYs["W1"]["ADDR_W104"]
NAME_W104 = MYs["W1"]["NAME_W104"]
W104_ID =  DEVICE_ID + '_' + MYs["W1"]["W104_ID"]
CONFIG_W104 = TOPIC + W104_ID + '/config'
W104_STATE = TOPIC + W104_ID + '/state'

ADDR_W105 = MYs["W1"]["ADDR_W105"]
NAME_W105 = MYs["W1"]["NAME_W105"]
W105_ID =  DEVICE_ID + '_' + MYs["W1"]["W105_ID"]
CONFIG_W105 = TOPIC + W105_ID + '/config'
W105_STATE = TOPIC + W105_ID + '/state'

ADDR_W106 = MYs["W1"]["ADDR_W106"]
NAME_W106 = MYs["W1"]["NAME_W106"]
W106_ID =  DEVICE_ID + '_' + MYs["W1"]["W106_ID"]
CONFIG_W106 = TOPIC + W106_ID + '/config'
W106_STATE = TOPIC + W106_ID + '/state'

ADDR_W107 = MYs["W1"]["ADDR_W107"]
NAME_W107 = MYs["W1"]["NAME_W107"]
W107_ID =  DEVICE_ID + '_' + MYs["W1"]["W107_ID"]
CONFIG_W107 = TOPIC + W107_ID + '/config'
W107_STATE = TOPIC + W107_ID + '/state'

ADDR_W108 = MYs["W1"]["ADDR_W108"]
NAME_W108 = MYs["W1"]["NAME_W108"]
W108_ID =  DEVICE_ID + '_' + MYs["W1"]["W108_ID"]
CONFIG_W108 = TOPIC + W108_ID + '/config'
W108_STATE = TOPIC + W108_ID + '/state'

ADDR_W109 = MYs["W1"]["ADDR_W109"]
NAME_W109 = MYs["W1"]["NAME_W109"]
W109_ID =  DEVICE_ID + '_' + MYs["W1"]["W109_ID"]
CONFIG_W109 = TOPIC + W109_ID + '/config'
W109_STATE = TOPIC + W109_ID + '/state'

ADDR_W110 = MYs["W1"]["ADDR_W110"]
NAME_W110 = MYs["W1"]["NAME_W110"]
W110_ID =  DEVICE_ID + '_' + MYs["W1"]["W110_ID"]
CONFIG_W110 = TOPIC + W110_ID + '/config'
W110_STATE = TOPIC + W110_ID + '/state'

ADDR_W111 = MYs["W1"]["ADDR_W111"]
NAME_W111 = MYs["W1"]["NAME_W111"]
W111_ID =  DEVICE_ID + '_' + MYs["W1"]["W111_ID"]
CONFIG_W111 = TOPIC + W111_ID + '/config'
W111_STATE = TOPIC + W111_ID + '/state'

ADDR_W112 = MYs["W1"]["ADDR_W112"]
NAME_W112 = MYs["W1"]["NAME_W112"]
W112_ID =  DEVICE_ID + '_' + MYs["W1"]["W112_ID"]
CONFIG_W112 = TOPIC + W112_ID + '/config'
W112_STATE = TOPIC + W112_ID + '/state'

ADDR_W113 = MYs["W1"]["ADDR_W113"]
NAME_W113 = MYs["W1"]["NAME_W113"]
W113_ID =  DEVICE_ID + '_' + MYs["W1"]["W113_ID"]
CONFIG_W113 = TOPIC + W113_ID + '/config'
W113_STATE = TOPIC + W113_ID + '/state'

ADDR_W114 = MYs["W1"]["ADDR_W114"]
NAME_W114 = MYs["W1"]["NAME_W114"]
W114_ID =  DEVICE_ID + '_' + MYs["W1"]["W114_ID"]
CONFIG_W114 = TOPIC + W114_ID + '/config'
W114_STATE = TOPIC + W114_ID + '/state'

ADDR_W115 = MYs["W1"]["ADDR_W115"]
NAME_W115 = MYs["W1"]["NAME_W115"]
W115_ID =  DEVICE_ID + '_' + MYs["W1"]["W115_ID"]
CONFIG_W115 = TOPIC + W115_ID + '/config'
W115_STATE = TOPIC + W115_ID + '/state'

# These are the s/n's used for the temp sensors.
list = [999, ADDR_W101, ADDR_W102, ADDR_W103, ADDR_W104, ADDR_W105, ADDR_W106, ADDR_W107, ADDR_W108, ADDR_W109, ADDR_W110, ADDR_W111, ADDR_W112, ADDR_W113, ADDR_W114, ADDR_W115, 999, 999 ]

# These are the STATE Topics
state_topic = ["", W101_STATE, W102_STATE, W103_STATE, W104_STATE, W105_STATE, W106_STATE, W107_STATE, W108_STATE, W109_STATE, W110_STATE, W111_STATE, W112_STATE, W113_STATE, W114_STATE, W115_STATE, "", "" ]

payload_W101config = {
    "name": NAME_W101,
    "stat_t": W101_STATE,
    "avty_t": LWT,
    "pl_avail": "Online",
    "pl_not_avail": "Offline",
    "uniq_id": W101_ID,
    "dev": {
        "ids": [
        D_ID,
        DEVICE_ID
        ],
        "name": "ThermoPI Cottage",
        'sa': AREA,
        "mf": "SirGoodenough",
        "mdl": "HomeAssistant Discovery for ThermoPI Cottage",
        "sw": "https://github.com/SirGoodenough/ThermoPI-Cottage",
        "cu": "https://github.com/SirGoodenough/ThermoPI-Cottage/blob/master/README.md"
    },
    "unit_of_meas":"°F",
    "dev_cla":"temperature",
    "frc_upd": True,
    'exp_aft': 400,
    "val_tpl": "{{ value_json.temperature }}"
}

payload_W102config = {
    "name": NAME_W102,
    "stat_t": W102_STATE,
    "avty_t": LWT,
    "pl_avail": "Online",
    "pl_not_avail": "Offline",
    "uniq_id": W102_ID,
    "dev": {
        "ids": [
        D_ID,
        DEVICE_ID
        ],
        "name": "ThermoPI Cottage",
        'sa': AREA,
        "mf": "SirGoodenough",
        "mdl": "HomeAssistant Discovery for ThermoPI Cottage",
        "sw": "https://github.com/SirGoodenough/ThermoPI-Cottage",
        "cu": "https://github.com/SirGoodenough/ThermoPI-Cottage/blob/main/README.md"
    },
    "unit_of_meas":"°F",
    "dev_cla":"temperature",
    "frc_upd": True,
    'exp_aft': 400,
    "val_tpl": "{{ value_json.temperature }}"
}

payload_W103config = {
    "name": NAME_W103,
    "stat_t": W103_STATE,
    "avty_t": LWT,
    "pl_avail": "Online",
    "pl_not_avail": "Offline",
    "uniq_id": W103_ID,
    "dev": {
        "ids": [
        D_ID,
        DEVICE_ID
        ],
        "name": "ThermoPI Cottage",
        'sa': AREA,
        "mf": "SirGoodenough",
        "mdl": "HomeAssistant Discovery for ThermoPI Cottage",
        "sw": "https://github.com/SirGoodenough/ThermoPI-Cottage",
        "cu": "https://github.com/SirGoodenough/ThermoPI-Cottage/blob/main/README.md"
    },
    "unit_of_meas":"°F",
    "dev_cla":"temperature",
    "frc_upd": True,
    'exp_aft': 400,
    "val_tpl": "{{ value_json.temperature }}"
}

payload_W104config = {
    "name": NAME_W104,
    "stat_t": W104_STATE,
    "avty_t": LWT,
    "pl_avail": "Online",
    "pl_not_avail": "Offline",
    "uniq_id": W104_ID,
    "dev": {
        "ids": [
        D_ID,
        DEVICE_ID
        ],
        "name": "ThermoPI Cottage",
        'sa': AREA,
        "mf": "SirGoodenough",
        "mdl": "HomeAssistant Discovery for ThermoPI Cottage",
        "sw": "https://github.com/SirGoodenough/ThermoPI-Cottage",
        "cu": "https://github.com/SirGoodenough/ThermoPI-Cottage/blob/main/README.md"
    },
    "unit_of_meas":"°F",
    "dev_cla":"temperature",
    "frc_upd": True,
    'exp_aft': 400,
    "val_tpl": "{{ value_json.temperature }}"
}

payload_W105config = {
    "name": NAME_W105,
    "stat_t": W105_STATE,
    "avty_t": LWT,
    "pl_avail": "Online",
    "pl_not_avail": "Offline",
    "uniq_id": W105_ID,
    "dev": {
        "ids": [
        D_ID,
        DEVICE_ID
        ],
        "name": "ThermoPI Cottage",
        'sa': AREA,
        "mf": "SirGoodenough",
        "mdl": "HomeAssistant Discovery for ThermoPI Cottage",
        "sw": "https://github.com/SirGoodenough/ThermoPI-Cottage",
        "cu": "https://github.com/SirGoodenough/ThermoPI-Cottage/blob/main/README.md"
    },
    "unit_of_meas":"°F",
    "dev_cla":"temperature",
    "frc_upd": True,
    'exp_aft': 400,
    "val_tpl": "{{ value_json.temperature }}"
}

payload_W106config = {
    "name": NAME_W106,
    "stat_t": W106_STATE,
    "avty_t": LWT,
    "pl_avail": "Online",
    "pl_not_avail": "Offline",
    "uniq_id": W106_ID,
    "dev": {
        "ids": [
        D_ID,
        DEVICE_ID
        ],
        "name": "ThermoPI Cottage",
        'sa': AREA,
        "mf": "SirGoodenough",
        "mdl": "HomeAssistant Discovery for ThermoPI Cottage",
        "sw": "https://github.com/SirGoodenough/ThermoPI-Cottage",
        "cu": "https://github.com/SirGoodenough/ThermoPI-Cottage/blob/main/README.md"
    },
    "unit_of_meas":"°F",
    "dev_cla":"temperature",
    "frc_upd": True,
    'exp_aft': 400,
    "val_tpl": "{{ value_json.temperature }}"
}

payload_W107config = {
    "name": NAME_W107,
    "stat_t": W107_STATE,
    "avty_t": LWT,
    "pl_avail": "Online",
    "pl_not_avail": "Offline",
    "uniq_id": W107_ID,
    "dev": {
        "ids": [
        D_ID,
        DEVICE_ID
        ],
        "name": "ThermoPI Cottage",
        'sa': AREA,
        "mf": "SirGoodenough",
        "mdl": "HomeAssistant Discovery for ThermoPI Cottage",
        "sw": "https://github.com/SirGoodenough/ThermoPI-Cottage",
        "cu": "https://github.com/SirGoodenough/ThermoPI-Cottage/blob/main/README.md"
    },
    "unit_of_meas":"°F",
    "dev_cla":"temperature",
    "frc_upd": True,
    'exp_aft': 400,
    "val_tpl": "{{ value_json.temperature }}"
}

payload_W108config = {
    "name": NAME_W108,
    "stat_t": W108_STATE,
    "avty_t": LWT,
    "pl_avail": "Online",
    "pl_not_avail": "Offline",
    "uniq_id": W108_ID,
    "dev": {
        "ids": [
        D_ID,
        DEVICE_ID
        ],
        "name": "ThermoPI Cottage",
        'sa': AREA,
        "mf": "SirGoodenough",
        "mdl": "HomeAssistant Discovery for ThermoPI Cottage",
        "sw": "https://github.com/SirGoodenough/ThermoPI-Cottage",
        "cu": "https://github.com/SirGoodenough/ThermoPI-Cottage/blob/main/README.md"
    },
    "unit_of_meas":"°F",
    "dev_cla":"temperature",
    "frc_upd": True,
    'exp_aft': 400,
    "val_tpl": "{{ value_json.temperature }}"
}

payload_W109config = {
    "name": NAME_W109,
    "stat_t": W109_STATE,
    "avty_t": LWT,
    "pl_avail": "Online",
    "pl_not_avail": "Offline",
    "uniq_id": W109_ID,
    "dev": {
        "ids": [
        D_ID,
        DEVICE_ID
        ],
        "name": "ThermoPI Cottage",
        'sa': AREA,
        "mf": "SirGoodenough",
        "mdl": "HomeAssistant Discovery for ThermoPI Cottage",
        "sw": "https://github.com/SirGoodenough/ThermoPI-Cottage",
        "cu": "https://github.com/SirGoodenough/ThermoPI-Cottage/blob/main/README.md"
    },
    "unit_of_meas":"°F",
    "dev_cla":"temperature",
    "frc_upd": True,
    'exp_aft': 400,
    "val_tpl": "{{ value_json.temperature }}"
}

payload_W110config = {
    "name": NAME_W110,
    "stat_t": W110_STATE,
    "avty_t": LWT,
    "pl_avail": "Online",
    "pl_not_avail": "Offline",
    "uniq_id": W110_ID,
    "dev": {
        "ids": [
        D_ID,
        DEVICE_ID
        ],
        "name": "ThermoPI Cottage",
        'sa': AREA,
        "mf": "SirGoodenough",
        "mdl": "HomeAssistant Discovery for ThermoPI Cottage",
        "sw": "https://github.com/SirGoodenough/ThermoPI-Cottage",
        "cu": "https://github.com/SirGoodenough/ThermoPI-Cottage/blob/main/README.md"
    },
    "unit_of_meas":"°F",
    "dev_cla":"temperature",
    "frc_upd": True,
    'exp_aft': 400,
    "val_tpl": "{{ value_json.temperature }}"
}

payload_W111config = {
    "name": NAME_W111,
    "stat_t": W111_STATE,
    "avty_t": LWT,
    "pl_avail": "Online",
    "pl_not_avail": "Offline",
    "uniq_id": W111_ID,
    "dev": {
        "ids": [
        D_ID,
        DEVICE_ID
        ],
        "name": "ThermoPI Cottage",
        'sa': AREA,
        "mf": "SirGoodenough",
        "mdl": "HomeAssistant Discovery for ThermoPI Cottage",
        "sw": "https://github.com/SirGoodenough/ThermoPI-Cottage",
        "cu": "https://github.com/SirGoodenough/ThermoPI-Cottage/blob/main/README.md"
    },
    "unit_of_meas":"°F",
    "dev_cla":"temperature",
    "frc_upd": True,
    'exp_aft': 400,
    "val_tpl": "{{ value_json.temperature }}"
}

payload_W112config = {
    "name": NAME_W112,
    "stat_t": W112_STATE,
    "avty_t": LWT,
    "pl_avail": "Online",
    "pl_not_avail": "Offline",
    "uniq_id": W112_ID,
    "dev": {
        "ids": [
        D_ID,
        DEVICE_ID
        ],
        "name": "ThermoPI Cottage",
        'sa': AREA,
        "mf": "SirGoodenough",
        "mdl": "HomeAssistant Discovery for ThermoPI Cottage",
        "sw": "https://github.com/SirGoodenough/ThermoPI-Cottage",
        "cu": "https://github.com/SirGoodenough/ThermoPI-Cottage/blob/main/README.md"
    },
    "unit_of_meas":"°F",
    "dev_cla":"temperature",
    "frc_upd": True,
    'exp_aft': 400,
    "val_tpl": "{{ value_json.temperature }}"
}

payload_W113config = {
    "name": NAME_W113,
    "stat_t": W113_STATE,
    "avty_t": LWT,
    "pl_avail": "Online",
    "pl_not_avail": "Offline",
    "uniq_id": W113_ID,
    "dev": {
        "ids": [
        D_ID,
        DEVICE_ID
        ],
        "name": "ThermoPI Cottage",
        'sa': AREA,
        "mf": "SirGoodenough",
        "mdl": "HomeAssistant Discovery for ThermoPI Cottage",
        "sw": "https://github.com/SirGoodenough/ThermoPI-Cottage",
        "cu": "https://github.com/SirGoodenough/ThermoPI-Cottage/blob/main/README.md"
    },
    "unit_of_meas":"°F",
    "dev_cla":"temperature",
    "frc_upd": True,
    'exp_aft': 400,
    "val_tpl": "{{ value_json.temperature }}"
}

payload_W114config = {
    "name": NAME_W114,
    "stat_t": W114_STATE,
    "avty_t": LWT,
    "pl_avail": "Online",
    "pl_not_avail": "Offline",
    "uniq_id": W114_ID,
    "dev": {
        "ids": [
        D_ID,
        DEVICE_ID
        ],
        "name": "ThermoPI Cottage",
        'sa': AREA,
        "mf": "SirGoodenough",
        "mdl": "HomeAssistant Discovery for ThermoPI Cottage",
        "sw": "https://github.com/SirGoodenough/ThermoPI-Cottage",
        "cu": "https://github.com/SirGoodenough/ThermoPI-Cottage/blob/main/README.md"
    },
    "unit_of_meas":"°F",
    "dev_cla":"temperature",
    "frc_upd": True,
    'exp_aft': 400,
    "val_tpl": "{{ value_json.temperature }}"
}

payload_W115config = {
    "name": NAME_W115,
    "stat_t": W115_STATE,
    "avty_t": LWT,
    "pl_avail": "Online",
    "pl_not_avail": "Offline",
    "uniq_id": W115_ID,
    "dev": {
        "ids": [
        D_ID,
        DEVICE_ID
        ],
        "name": "ThermoPI Cottage",
        'sa': AREA,
        "mf": "SirGoodenough",
        "mdl": "HomeAssistant Discovery for ThermoPI Cottage",
        "sw": "https://github.com/SirGoodenough/ThermoPI-Cottage",
        "cu": "https://github.com/SirGoodenough/ThermoPI-Cottage/blob/main/README.md"
    },
    "unit_of_meas":"°F",
    "dev_cla":"temperature",
    "frc_upd": True,
    'exp_aft': 400,
    "val_tpl": "{{ value_json.temperature }}"
}

    #Log Message to start
print('Logging {0} sensor measurements every {1} seconds.'.format(D_ID, LOOP))
print('Press Ctrl-C to quit.')
mqttc = mqtt.Client(D_ID, 'False', 'MQTTv311')
mqttc.disable_logger()  # Saves wear on SD card Memory.  Remove as needed for troubleshooting
mqttc.username_pw_set(USER, PWD) # deactivate if not needed
mqttConnect()

try:
    count = 0
    while count < 16:
        if count > 14:  # Reset the loop
            count = 0
        count += 1
        print('Updating loop %s.' % count)
        print('Temperature %s.' % temp)
        temp = 0.0
        W1()
        mqttSend()
        time.sleep(LOOP)

except KeyboardInterrupt:
    print(' Keyboard Interrupt. Closing MQTT.')
    mqttc.publish(LWT, 'Offline', 1, True)
    time.sleep(1)
    mqttc.loop_stop()
    mqttc.disconnect()
    sys.exit()
