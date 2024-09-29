#!/usr/bin/env python
# #####################################################################################################
# rsu_control comamnds: output test only with: single pin (led) and set of pind (traffic light)
#   Note: modifications required, for complex traffic light systems (with more than one semaphore)
#######################################################################################################
import application.app_config as app_conf
import base64
from io import BytesIO

def start_rsu(rsu_control_txd_queue):
    if (app_conf.debug_app) or (app_conf.debug_rsu):
        print ('rsu_application: start_rsu')

    rsu_control_msg="s"
    rsu_control_txd_queue.put(rsu_control_msg)
    return 


def exit_rsu(rsu_control_txd_queue):
    if (app_conf.debug_app) or (app_conf.debug_rsu):
        print ('rsu_application: exit_rsu')
    rsu_control_msg="x"
    rsu_control_txd_queue.put(rsu_control_msg)
    return 

def turn_on(rsu_control_txd_queue):
    if (app_conf.debug_app) or (app_conf.debug_rsu):
        print ('rsu_application: turn_on')
    rsu_control_msg="1"
    rsu_control_txd_queue.put(rsu_control_msg)
    return 

def turn_off(rsu_control_txd_queue):
    if (app_conf.debug_app) or (app_conf.debug_rsu):
        print ('rsu_application: turn_off')
    rsu_control_msg="0"
    rsu_control_txd_queue.put(rsu_control_msg)
    return 

def create_dc_message(node, value, time):
    
    data_center_msg = {'msg_type':'DC', 'node':node, 'value':value, 'time':time}
    return data_center_msg

def restore_bytes_io(encoded_data):
    
    new_data = []
    # Decode base64 to binary
    for data in encoded_data:
        if data['sensor_type'] == 'image':
            binary_data = base64.b64decode(data['sensor_reading'])
            # Create a new BytesIO object with the binary data
            restored_stream = BytesIO(binary_data)
            data['sensor_reading'] = restored_stream
        new_data.append(data)
        
    return new_data