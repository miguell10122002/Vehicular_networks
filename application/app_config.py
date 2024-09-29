#!/usr/bin/env python
# #####################################################################################################
# APP CONFIGURATION PARAMETERS -
#######################################################################################################
from threading import Thread, Event

# #####################################################################################################
# Other layers debug options usefull to test the application
# #####################################################################################################
# print location
debug_location = 0             #print nodes coordinates

# print application data
debug_app = 0                   #printinformation of the commands executed (rsu and obu)
debug_rsu = 0                   #printinformation of the rsu commands executed 
debug_obu = 1                   #printinformation of the obu commands executed 
debug_app_ca = 0                #print ca messages trigerred and received (application layer)
debug_app_den = 0               #print den messages sent and received (application layer)

# print control data
debug_gpio = 0                  #print gpio functions (car_motor_functions and rsu_control_functions)
debug_obu_control = 0          #print  high level obu control information (car_motor_functions)
debug_rsu_control = 0           #print rsu high level control information (car_motor_functions  rsu_control_functions)level rsu control information (rsu_control_functions)

# print sys data
debug_sys = 0                    #print SO-related information


# #####################################################################################################
# Local test (laptop) or SmartMob platform test
# local_test = 0 if code when using the raspberry pies
# #####################################################################################################
local_test = 0

# #####################################################################################################
# PROJECT CONFIGURATIONS
# #####################################################################################################
# For initial tests, apply a fixed value to X or Y position without relation to physical world's car movement. 
# delta_space is the fixed value.
fixed_spaces = 0
delta_space = 10

#------------------------------------------------------------------------------------------
#include here any specific configuration of the application
#------------------------------------------------------------------------------------------
time_interval = 10      #wait time between consecutive movements updates

danger_threshold = 100 #cm
accident_threshold = 10 #cm
read_heavy_data = Event()
# #####################################################################################################
# CA MESSAGES
# #####################################################################################################
#warm_up_time = 10
#ca_generation_interval = 10


# #####################################################################################################
# DEN MESSAGES
# #####################################################################################################
#max_latency = 10000

# EVENTS  -  flags used to coordinate threads activities
# start_den_txd - set by the application, when DEN message must be sent
#start_den_txd=Event()


# example of DEN message configuration. 
# Definition of the first event (position 0 of the array)

#safety_critical = 0
# DEN message - Event type
#event_type = ["SAFETY CRITICAL WARNING"]
# DEN message - Event status (start | update | stop)
#event_status = ['start']
#if event_status == 'start':
#DEN message - repetition interval (0 if single event)
#rep_interval = [0]
# DEN message - Maximum hop number
#n_hops = [8]
#DEN message - ROI x coordinates (0 if none)
#roi_x  = [0]
#DEN message - ROI y coordinates (0 if none)
#roi_y  = [0]
#DEN message - ROI y coordinates (0 if none)
#latency = [max_latency]


# IMPORTANT TIP: roi, latency are not implemented but can be added.
# To create a new event, name it and assign the next integer to refer to te event position in the array. 
# Example: new_event = 1
# Add an element to each vector with the descritpion of the event.
# Example: New event, with periodic transmission (100), 8 hops dissemination, and a roi, in x axis up to 1000 units distance
# event_type = ["SAFETY CRITICAL WARNING"]["NEW EVENT"]
# event_status = ['start']['start']
# rep_interval = [0][100]   
# n_hops = [1][8]
# roi_x  = [0][1000]
# roi_y  = [0][0]
# latency = [max_latency][max_latency]

# IMPORTANT TIP: update messages are not implemented but can be added.
# To create an update event, name it and assign the next integer to refer to te event position in the array. 
# Example: update_event = 2
# Add an element to each vector with the descritpion of the event.
# Example: New event, with periodic transmission (100), 8 hops dissemination, and a roi, in x axis up to 1000 units distance
# event_type = ["SAFETY CRITICAL WARNING"]["NEW EVENT"]["UPDATE EVENT"]
# event_status = ['start']['start']['update']
# rep_interval = [0][100][-1]   
# n_hops = [1][8][-1] 
# roi_x  = [0][1000][-1] 
# roi_y  = [0][0][-1] 
# latency = [max_latency][max_latency][-1] 
