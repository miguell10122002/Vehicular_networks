#!/usr/bin/env python
# #################################################
## RSU legacy system control - example traffic light systems/external sensors and actuators
#################################################
import time
from rsu_legacy_systems.rsu_control_functions import *
import application.app_config as app_conf


#-----------------------------------------------------------------------------------------
# Thread -rsu_control 
#   Esta thread pode controlar varios semaforos, desde que estejam definidas as informações no ficheiro traffic_light.py
#     move_command=rsu_control_txd_queue.get - fila onde a aplicacao de controlo dos semaforos coloca os comandos
#     controlo de semaforos efetuado atraves das funcoes disponiveis em rsu_control_functions
#-----------------------------------------------------------------------------------------
def rsu_control (node, start_flag, coordinates, rsu_interface, rsu_control_txd_queue):

# atualizar a informação de estado da RSU, se relevante
#	init_rsu_info(rsu_interface)
    
    while not start_flag.isSet():
        time.sleep (1)
    if (app_conf.debug_sys):
        print('STATUS: Ready to start - THREAD: update_location - NODE: {}\n'.format(node),'\n') 
   
    rsu_interface['rsu_status']='not_ready'
    while True:
        command=rsu_control_txd_queue.get()
        if rsu_interface['rsu_status']=='not_ready':
            if command == 's':
                rsu_interface = start_rsu(rsu_interface) 
        elif rsu_interface['rsu_status']!='not_ready':
            if command == 'x':
                rsu_interface = stop_rsu(rsu_interface)
            elif command == '1':
                rsu_interface = change_sensor_status (rsu_interface,command)
            elif command == '0': 
                rsu_interface = change_sensor_status (rsu_interface,command)
            elif command == 's_green' or 's_yellow' or 's_red':
                rsu_interface = set_tl_status(rsu_interface, command)
        #complete with other use cases, if needed
    return 