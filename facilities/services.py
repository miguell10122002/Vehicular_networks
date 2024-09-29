#!/usr/bin/env python
# #################################################
## FUNCTIONS USED BY FACILITITES LAYER  - COMMMON SERVICES
#################################################
import time
#from in_vehicle_network.car_motor_functions import *
from gps_info.gps_reader import *

#------------------------------------------------------------------------------------------------
# create_CA_message - create a cooperative awareness message based on the vehicle's informatiom
#                    - node: node that generates the event
#                    - msg_id: identification of the event used to discard duplicated DEN messages received
#                    - coordinates: real-time position (x,y) at the instant (t) when the message is created
#                    - obd_2_interface: vehicle's dynamic information (speed, direction and heading).
#-------------------------------------------------------------------------------------------------

def create_ca_message(node, msg_id,coordinates, node_interface):
	x,y,t = position_read(coordinates)
	#s,d,h = get_vehicle_info(node_interface['speed'],node_interface['directio'],node_interface['heading'] )
	ca_msg= {'msg_type':'CA', 'node':node, 'msg_id':msg_id,'pos_x': x,'pos_y': y,'time':time.time(),
		  'speed': node_interface['speed'], 'dir':node_interface['direction'], 'heading':node_interface['heading'] }
	return ca_msg

#------------------------------------------------------------------------------------------------
# create_DEN_message - create an event message (DEN) based on information received from application layer
#                    - node: node that generates the event
#                    - msg_id: identification of the event used to discard duplicated DEN messages received
#                    - coordinates: real-time position (x,y) at the instant (t) when the message is created
#                    - event: event information received from application layer.
#-------------------------------------------------------------------------------------------------
def create_den_message(node, msg_id, coordinates, event):
	x,y,t = position_read(coordinates)
	den_msg= {'msg_type':'DEN', 'node':node, 'msg_id':msg_id,'pos_x': x,'pos_y':y, 'time':t, 'event': event}
	return den_msg
